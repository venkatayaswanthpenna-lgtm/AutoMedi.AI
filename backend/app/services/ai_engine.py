import asyncio
import json
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.vehicle import Inspection, InspectionImage
from app.models.damage import DamageRecord
from app.services.cost_engine import calculate_costs
from app.core.config import settings
import google.generativeai as genai
from PIL import Image

logger = logging.getLogger(__name__)

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

from app.core.database import AsyncSessionLocal

async def trigger_ai_analysis(inspection_id: int):
    """
    Analyzes uploaded images using Google Gemini Vision API to detect vehicle damage.
    """
    async with AsyncSessionLocal() as db:
        try:
            # 1. Fetch inspection & images
            result = await db.execute(select(Inspection).where(Inspection.id == inspection_id))
            inspection = result.scalars().first()
        
            if not inspection:
                return
            
            img_result = await db.execute(select(InspectionImage).where(InspectionImage.inspection_id == inspection_id))
            images = img_result.scalars().all()
        
            if not images:
                inspection.status = "failed"
                await db.commit()
                return

            # Prepare images for Gemini
            import requests
            from io import BytesIO
        
            loaded_images = []
            for img_record in images:
                try:
                    path = img_record.file_path
                    if path.startswith("http://") or path.startswith("https://"):
                        # Download from S3/remote URL
                        response = requests.get(path)
                        response.raise_for_status()
                        img = Image.open(BytesIO(response.content))
                    else:
                        # Open local fallback image
                        img = Image.open(path)
                    
                    loaded_images.append(img)
                except Exception as e:
                    logger.error(f"Failed to load image {img_record.file_path}: {e}")
        
            if not loaded_images:
                inspection.status = "failed"
                await db.commit()
                return

            # 2. Call Gemini API if Key exists, otherwise fallback to basic mock for local testing without key
            damages_to_add = []
            if settings.GEMINI_API_KEY:
                # We use gemini-3.5-flash as it's fast and supports multimodal inputs
                model = genai.GenerativeModel('gemini-3.5-flash')
            
                prompt = """
                You are an expert automotive mechanic and AI damage assessor.
                I am providing you with one or more images of a vehicle from various angles.
                Analyze the vehicle for any damages (e.g., Scratches, Dents, Cracks, Broken parts, Rust, Paint Damage).
            
                You must respond ONLY with a valid JSON array. Do not include Markdown blocks (like ```json), just the raw JSON.
                Each object in the array should represent a single damaged part and have the following exact keys:
                - "part_name": string (e.g., "Front Bumper", "Windshield", "Left Front Door")
                - "damage_type": string (e.g., "Scratch", "Dent", "Crack", "Broken")
                - "severity": string (must be one of: "Low", "Medium", "High", "Critical")
                - "repairability": string (must be one of: "Repairable", "Replace")
            
                If no damage is found, return an empty array: []
                """
            
                # Send prompt + images
                response = await asyncio.to_thread(model.generate_content, [prompt] + loaded_images)
            
                # Parse the JSON response
                response_text = response.text.strip()
                # Clean up markdown formatting if Gemini included it despite instructions
                if response_text.startswith("```json"):
                    response_text = response_text[7:-3].strip()
                elif response_text.startswith("```"):
                    response_text = response_text[3:-3].strip()
                
                try:
                    ai_damages = json.loads(response_text)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse Gemini JSON: {e}\nResponse: {response_text}")
                    ai_damages = []
                
                # Create Damage Records from AI output
                for d in ai_damages:
                    record = DamageRecord(
                        inspection_id=inspection_id,
                        part_name=d.get("part_name", "Unknown Part"),
                        damage_type=d.get("damage_type", "Unknown Damage"),
                        severity=d.get("severity", "Medium"),
                        confidence_score=0.90,  # Fixed confidence for now
                        repairability=d.get("repairability", "Repairable")
                    )
                    db.add(record)
                    damages_to_add.append(record)
            else:
                # Fallback mock if no API key is provided
                logger.warning("No GEMINI_API_KEY provided. Falling back to mock damage detection.")
                mock_damage = DamageRecord(
                    inspection_id=inspection_id,
                    part_name="Front Bumper",
                    damage_type="Scratch",
                    severity="Low",
                    confidence_score=0.85,
                    repairability="Repairable"
                )
                db.add(mock_damage)
                damages_to_add.append(mock_damage)

            # 4. Generate Cost Estimate based on detected damages
            if damages_to_add:
                cost = calculate_costs(damages_to_add)
                cost.inspection_id = inspection_id
                db.add(cost)
        
            # 5. Update inspection status
            inspection.status = "completed"
            await db.commit()

        except Exception as e:
            logger.error(f"AI Analysis failed for inspection {inspection_id}: {e}")
            # Mark as failed to avoid hanging the UI
            try:
                inspection.status = "failed"
                await db.commit()
            except:
                pass
