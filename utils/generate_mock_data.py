import os
import pandas as pd
from fpdf import FPDF
import random
from datetime import datetime, timedelta

def generate_invoice_pdf(invoice_id, vendor, amount, date, items, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="INVOICE", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Invoice ID: {invoice_id}", ln=True)
    pdf.cell(200, 10, txt=f"Vendor: {vendor}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {date}", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(100, 10, txt="Item Description", border=1)
    pdf.cell(50, 10, txt="Quantity", border=1)
    pdf.cell(40, 10, txt="Price", border=1)
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    for item, qty, price in items:
        pdf.cell(100, 10, txt=item, border=1)
        pdf.cell(50, 10, txt=str(qty), border=1)
        pdf.cell(40, 10, txt=f"${price:.2f}", border=1)
        pdf.ln(10)
        
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Total Amount Due: ${amount:.2f}", ln=True)
    
    pdf.output(output_path)

def main():
    os.makedirs("accounting_rag_app/data/invoices", exist_ok=True)
    os.makedirs("accounting_rag_app/data/reports", exist_ok=True)
    
    vendors = ["Cloud Services Inc", "Office Supplies Co", "Marketing Pros", "Legal Associates", "Clean & Green"]
    items_pool = [
        ("Monthly Subscription", 1, 500.00),
        ("Paper Packs", 10, 5.00),
        ("Ad Campaign", 1, 2500.00),
        ("Consultation Fee", 5, 200.00),
        ("Office Cleaning", 1, 150.00)
    ]
    
    invoice_data = []
    for i in range(1, 6):
        vendor = random.choice(vendors)
        date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
        inv_id = f"INV-2024-{i:03d}"
        
        # Pick 1-3 random items
        num_items = random.randint(1, 3)
        selected_items = random.sample(items_pool, num_items)
        total_amount = sum(item[1] * item[2] for item in selected_items)
        
        output_path = f"accounting_rag_app/data/invoices/{inv_id}.pdf"
        generate_invoice_pdf(inv_id, vendor, total_amount, date, selected_items, output_path)
        
        invoice_data.append({
            "invoice_id": inv_id,
            "vendor": vendor,
            "amount": total_amount,
            "date": date,
            "status": "Pending"
        })
    
    # Save a CSV summary for structured data testing
    df = pd.DataFrame(invoice_data)
    df.to_csv("accounting_rag_app/data/invoice_summary.csv", index=False)
    
    # Generate a mock financial report
    report_content = """
    # Annual Financial Audit Report 2024
    
    ## Executive Summary
    The company has maintained a steady growth of 15% in the last fiscal year. 
    Operational expenses have increased by 5% due to expansion in the marketing department.
    
    ## Revenue Analysis
    - Q1: $1,200,000
    - Q2: $1,350,000
    - Q3: $1,100,000
    - Q4: $1,500,000
    
    ## Expense Audit
    The audit team reviewed 500+ invoices. Most vendors are compliant with the payment terms.
    Notable mention: Cloud Services Inc remains the largest vendor by volume.
    
    ## Compliance
    All financial statements are in accordance with GAAP standards.
    """
    with open("accounting_rag_app/data/reports/audit_report_2024.md", "w") as f:
        f.write(report_content)

if __name__ == "__main__":
    main()
