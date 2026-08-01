import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from uuid import uuid4

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.vehicle import Vehicle, Inspection, InspectionImage
from app.schemas.vehicle import VehicleResponse, InspectionResponse
from app.services.ai_engine import trigger_ai_analysis

from app.services.s3_service import upload_file

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/inspections", response_model=InspectionResponse)
async def create_inspection(
    company: str = Form(...),
    model: str = Form(...),
    year: int = Form(...),
    vehicle_type: str = Form(...),
    fuel_type: str = Form(None),
    transmission: str = Form(None),
    color: str = Form(None),
    mileage: int = Form(None),
    vin: str = Form(None),
    files: List[UploadFile] = File(...),
    angles: List[str] = Form(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if len(files) != len(angles):
        raise HTTPException(status_code=400, detail="Files and angles count mismatch")

    # 1. Create Vehicle
    db_vehicle = Vehicle(
        user_id=current_user.id,
        company=company,
        model=model,
        year=year,
        vehicle_type=vehicle_type,
        fuel_type=fuel_type,
        transmission=transmission,
        color=color,
        mileage=mileage,
        vin=vin
    )
    db.add(db_vehicle)
    await db.commit()
    await db.refresh(db_vehicle)

    # 2. Create Inspection
    db_inspection = Inspection(vehicle_id=db_vehicle.id, status="analyzing")
    db.add(db_inspection)
    await db.commit()
    await db.refresh(db_inspection)

    # 3. Save Files and Create InspectionImages
    image_records = []
    for file, angle in zip(files, angles):
        # MOCK VIRUS SCAN HOOK HERE
        # if virus_detected(file): raise Exception("Malware detected")
        
        # Upload using the S3 service (falls back to local if no credentials)
        file_path_or_url = await upload_file(file.file, file.filename, file.content_type)
            
        db_image = InspectionImage(
            inspection_id=db_inspection.id,
            angle=angle,
            file_path=file_path_or_url
        )
        db.add(db_image)
        image_records.append(db_image)
        
    await db.commit()
    
    # Trigger the AI engine background task
    background_tasks.add_task(trigger_ai_analysis, db_inspection.id)
    
    # Eagerly load images to prevent MissingGreenlet error during Pydantic serialization
    result = await db.execute(
        select(Inspection)
        .options(selectinload(Inspection.images))
        .where(Inspection.id == db_inspection.id)
    )
    final_inspection = result.scalars().first()
    
    return final_inspection
