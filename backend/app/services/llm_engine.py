import asyncio
import logging
from app.core.config import settings
import google.generativeai as genai

logger = logging.getLogger(__name__)

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

async def get_ai_response(user_message: str, inspection_context: dict) -> str:
    """
    Real LLM Engine powered by Google Gemini.
    Formats the user_message, chat history, and inspection_context into a prompt.
    """
    try:
        if not settings.GEMINI_API_KEY:
            logger.warning("No GEMINI_API_KEY provided. Falling back to mock chat.")
            return _mock_chat_fallback(user_message, inspection_context)
            
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 1. Format Context
        damages = inspection_context.get("damages", [])
        cost = inspection_context.get("cost")
        history = inspection_context.get("history", [])
        
        damages_text = "\n".join([f"- {d.part_name}: {d.damage_type} (Severity: {d.severity}, Action: {d.repairability})" for d in damages]) if damages else "No damages detected."
        
        cost_text = "Not available."
        if cost:
            cost_text = f"Total Range: ${cost.total_cost_min} - ${cost.total_cost_max} (Labor: ~${cost.labor_cost}, Parts: ~${cost.parts_cost}, Paint: ~${cost.paint_cost})"
            
        history_text = ""
        if history:
            for msg in history:
                sender = "User" if msg.sender == "user" else "Assistant"
                history_text += f"{sender}: {msg.message}\n"
                
        # 2. Construct Prompt
        system_prompt = f"""
You are the AutoMedi AI Chatbot, an expert automotive mechanic and app assistant.
You help customers understand their vehicle inspection reports and repair costs.

CRITICAL INSTRUCTIONS:
- You must ONLY answer questions based on the provided Inspection Data.
- If the user asks something unrelated to cars, repairs, or the inspection, politely decline.
- Be concise, professional, and empathetic. Do NOT use markdown code blocks for normal text.
- If they ask for mechanic recommendations, tell them to use the "Garage Discovery" feature.

INSPECTION DATA:
Detected Damages:
{damages_text}

Estimated Costs:
{cost_text}
"""
        
        # We append history to give conversational context
        full_prompt = system_prompt + "\n\nCHAT HISTORY:\n" + history_text + f"\nUser: {user_message}\nAssistant:"
        
        # 3. Call Gemini
        response = await asyncio.to_thread(model.generate_content, full_prompt)
        
        return response.text.strip()
        
    except Exception as e:
        logger.error(f"Chatbot LLM failed: {e}")
        return "I apologize, but I am having trouble connecting to my AI core right now. Please try again later."


def _mock_chat_fallback(user_message: str, inspection_context: dict) -> str:
    msg_lower = user_message.lower()
    if "cost" in msg_lower or "price" in msg_lower or "expensive" in msg_lower:
        if inspection_context.get("cost"):
            return f"Based on the AI assessment, your estimated repair cost is between ${inspection_context['cost'].total_cost_min} and ${inspection_context['cost'].total_cost_max}. This includes labor, parts, and paint."
        return "I don't have the cost details for this inspection yet."
        
    if "damage" in msg_lower or "what is wrong" in msg_lower or "broken" in msg_lower:
        if inspection_context.get("damages"):
            damages = [d.part_name for d in inspection_context["damages"]]
            return f"The AI detected damage on the following parts: {', '.join(damages)}. Please review the report for severity details."
        return "The AI didn't detect any specific damages on your vehicle."
        
    if "repair" in msg_lower or "fix" in msg_lower or "mechanic" in msg_lower:
        return "You can use the 'Garage Discovery' feature on your dashboard to find top-rated mechanics near you to fix this damage."
        
    return "I am the AutoMedi.AI Assistant (Mock Mode). I can help you understand your inspection results, explain repair costs, or guide you on the next steps to fix your vehicle."
