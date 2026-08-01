from fpdf import FPDF
import io
from app.models.vehicle import Vehicle, Inspection
from app.models.cost import CostEstimate
from app.models.damage import DamageRecord

def generate_pdf_report(inspection: Inspection, vehicle: Vehicle, cost: CostEstimate, damages: list[DamageRecord]) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # Header
    pdf.cell(200, 10, txt="AutoMedi.AI - Professional Inspection Report", ln=True, align='C')
    
    # Vehicle Info
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Vehicle Information", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(200, 8, txt=f"Make/Model: {vehicle.company} {vehicle.model} ({vehicle.year})", ln=True)
    pdf.cell(200, 8, txt=f"Type: {vehicle.vehicle_type} | VIN: {vehicle.vin or 'N/A'}", ln=True)
    
    # Executive Summary (Costs)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Executive Cost Summary", ln=True)
    pdf.set_font("Arial", '', 11)
    if cost:
        pdf.cell(200, 8, txt=f"Estimated Parts: ${cost.parts_cost_min} - ${cost.parts_cost_max}", ln=True)
        pdf.cell(200, 8, txt=f"Estimated Labor: ${cost.labor_cost_min} - ${cost.labor_cost_max}", ln=True)
        pdf.cell(200, 8, txt=f"Estimated Paint: ${cost.paint_cost_min} - ${cost.paint_cost_max}", ln=True)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(200, 10, txt=f"Total Estimated Cost: ${cost.total_cost_min} - ${cost.total_cost_max}", ln=True)
    else:
        pdf.cell(200, 8, txt="No damages detected. Total Cost: $0.00", ln=True)

    # Damages
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Detected Damages", ln=True)
    pdf.set_font("Arial", '', 11)
    for d in damages:
        pdf.cell(200, 8, txt=f"- {d.part_name}: {d.damage_type} ({d.severity}) -> {d.repairability}", ln=True)
    
    # Output to buffer
    return bytes(pdf.output())
