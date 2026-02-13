import os
import pandas as pd
from fpdf import FPDF
import random
from datetime import datetime, timedelta
from pathlib import Path

# Expanded vendor pool (50+ vendors for diversity)
VENDORS = [
    "Cloud Services Inc", "Office Supplies Co", "Marketing Pros", "Legal Associates", "Clean & Green",
    "Tech Solutions LLC", "Global Logistics", "Premium Consulting", "Data Systems Corp", "Smart Analytics",
    "Creative Design Studio", "Enterprise Software", "Security Services", "HR Solutions", "Finance Partners",
    "Telecom Provider", "Energy Solutions", "Facility Management", "IT Support Plus", "Training Academy",
    "Research Institute", "Compliance Consultants", "Tax Advisory Group", "Audit Professionals", "Risk Management",
    "Insurance Brokers", "Real Estate Services", "Travel Agency", "Catering Services", "Event Planners",
    "Print & Copy Center", "Equipment Rental", "Maintenance Crew", "Construction Partners", "Engineering Firm",
    "Architecture Studio", "Quality Assurance", "Testing Labs", "Certification Body", "Standards Compliance",
    "Environmental Services", "Waste Management", "Recycling Solutions", "Green Energy", "Sustainability Experts",
    "Medical Supplies", "Safety Equipment", "Protective Gear", "Emergency Services", "Security Systems"
]

# Categories for better organization
CATEGORIES = ["IT", "Legal", "Marketing", "Operations", "HR", "Finance", 
              "Facilities", "Consulting", "R&D", "Compliance", "Travel", "Supplies"]

# Departments
DEPARTMENTS = ["Engineering", "Sales", "Finance", "Marketing", "HR", "Operations", 
               "Legal", "IT", "Executive", "Customer Service", "R&D"]

# Approval statuses
STATUSES = ["Pending", "Approved", "Rejected", "Paid", "Overdue", "On Hold", "Cancelled"]

# Payment terms
PAYMENT_TERMS = ["Net 15", "Net 30", "Net 45", "Net 60", "Net 90", "Due on Receipt", "Prepaid"]

# Expanded items pool with categories
ITEMS_POOL = {
    "IT": [
        ("Cloud Hosting Service", 500.00), ("Software License", 1200.00), 
        ("IT Support Hours", 150.00), ("Hardware Maintenance", 300.00),
        ("Network Equipment", 2500.00), ("Cybersecurity Audit", 3000.00)
    ],
    "Legal": [
        ("Legal Consultation", 350.00), ("Contract Review", 500.00),
        ("Compliance Audit", 2000.00), ("Patent Filing", 5000.00)
    ],
    "Marketing": [
        ("Digital Ad Campaign", 3500.00), ("SEO Services", 1200.00),
        ("Social Media Management", 800.00), ("Content Creation", 600.00),
        ("Market Research", 2500.00), ("Brand Design", 1800.00)
    ],
    "Operations": [
        ("Facility Cleaning", 400.00), ("Equipment Rental", 750.00),
        ("Utilities", 1200.00), ("Maintenance Service", 500.00)
    ],
    "HR": [
        ("Recruitment Services", 2000.00), ("Training Session", 1500.00),
        ("Background Check", 150.00), ("Employee Benefits", 3000.00)
    ],
    "Supplies": [
        ("Office Supplies", 250.00), ("Furniture", 1500.00),
        ("Printer Toner", 80.00), ("Paper Supplies", 120.00)
    ],
    "Consulting": [
        ("Strategy Consulting", 5000.00), ("Process Optimization", 3500.00),
        ("Business Analysis", 2500.00), ("Project Management", 3000.00)
    ]
}

def generate_invoice_pdf(invoice_data, items, output_path):
    """Generate detailed invoice PDF with rich metadata."""
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(200, 10, txt="INVOICE", ln=True, align='C')
    pdf.ln(5)
    
    # Invoice details
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 8, txt=f"Invoice ID: {invoice_data['invoice_id']}", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 6, txt=f"Vendor: {invoice_data['vendor']}", ln=True)
    pdf.cell(200, 6, txt=f"Date: {invoice_data['date']}", ln=True)
    pdf.cell(200, 6, txt=f"Due Date: {invoice_data['due_date']}", ln=True)
    pdf.cell(200, 6, txt=f"Payment Terms: {invoice_data['payment_terms']}", ln=True)
    if invoice_data.get('po_number'):
        pdf.cell(200, 6, txt=f"PO Number: {invoice_data['po_number']}", ln=True)
    pdf.cell(200, 6, txt=f"Category: {invoice_data['category']}", ln=True)
    pdf.cell(200, 6, txt=f"Department: {invoice_data['department']}", ln=True)
    pdf.ln(5)
    
    # Items table
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(100, 8, txt="Item Description", border=1, align='C')
    pdf.cell(30, 8, txt="Quantity", border=1, align='C')
    pdf.cell(30, 8, txt="Unit Price", border=1, align='C')
    pdf.cell(30, 8, txt="Amount", border=1, align='C')
    pdf.ln()
    
    pdf.set_font("Arial", size=10)
    for item, qty, price in items:
        pdf.cell(100, 7, txt=item, border=1)
        pdf.cell(30, 7, txt=str(qty), border=1, align='C')
        pdf.cell(30, 7, txt=f"${price:.2f}", border=1, align='R')
        pdf.cell(30, 7, txt=f"${qty * price:.2f}", border=1, align='R')
        pdf.ln()
    
    # Totals
    pdf.ln(5)
    subtotal = invoice_data['subtotal']
    tax_amount = invoice_data['tax_amount']
    total = invoice_data['amount']
    
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(130, 7, txt="", border=0)
    pdf.cell(30, 7, txt="Subtotal:", border=0, align='R')
    pdf.cell(30, 7, txt=f"${subtotal:.2f}", border=0, align='R')
    pdf.ln()
    
    pdf.set_font("Arial", size=10)
    pdf.cell(130, 7, txt="", border=0)
    pdf.cell(30, 7, txt=f"Tax ({invoice_data['tax_rate']*100:.1f}%):", border=0, align='R')
    pdf.cell(30, 7, txt=f"${tax_amount:.2f}", border=0, align='R')
    pdf.ln()
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(130, 8, txt="", border=0)
    pdf.cell(30, 8, txt="TOTAL DUE:", border=0, align='R')
    pdf.cell(30, 8, txt=f"${total:.2f}", border=0, align='R')
    pdf.ln(10)
    
    # Status and notes
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(200, 6, txt=f"Status: {invoice_data['approval_status']}", ln=True)
    if invoice_data.get('notes'):
        pdf.set_font("Arial", 'I', 9)
        pdf.multi_cell(0, 5, txt=f"Notes: {invoice_data['notes']}")
    
    pdf.output(output_path)

def generate_po_number():
    """Generate realistic PO number (80% of invoices have one)."""
    if random.random() < 0.8:
        return f"PO-{random.randint(10000, 99999)}"
    return None

def generate_invoice_data(invoice_num, year):
    """Generate comprehensive invoice data with rich metadata."""
    vendor = random.choice(VENDORS)
    category = random.choice(CATEGORIES)
    department = random.choice(DEPARTMENTS)
    
    # Date within the year
    days_in_year = 365 if year != 2024 else 366
    days_offset = random.randint(0, days_in_year - 1)
    invoice_date = datetime(year, 1, 1) + timedelta(days=days_offset)
    
    # Payment terms and due date
    payment_terms = random.choice(PAYMENT_TERMS)
    days_until_due = int(payment_terms.split()[1]) if "Net" in payment_terms else 0
    due_date = invoice_date + timedelta(days=days_until_due)
    
    # Select items from category or random
    category_items = ITEMS_POOL.get(category, ITEMS_POOL["Supplies"])
    num_items = random.randint(1, 4)
    selected_items = random.choices(category_items, k=num_items)
    
    # Build line items with quantities
    items = []
    subtotal = 0
    for item_name, unit_price in selected_items:
        qty = random.randint(1, 10)
        items.append((item_name, qty, unit_price))
        subtotal += qty * unit_price
    
    # Tax calculation
    tax_rate = 0.08 if random.random() < 0.9 else 0.0  # 90% have tax
    tax_amount = subtotal * tax_rate
    total_amount = subtotal + tax_amount
    
    # Status assignment based on date
    days_old = (datetime.now() - invoice_date).days
    if days_old < 0:  # Future date (shouldn't happen but safeguard)
        status = "Pending"
    elif days_old > (days_until_due + 30):
        status = random.choice(["Paid", "Overdue", "Cancelled"])
    elif days_old > days_until_due:
        status = random.choice(["Paid", "Overdue", "Pending"])
    else:
        status = random.choice(["Pending", "Approved", "Paid"])
    
    # Generate notes for some invoices
    notes = None
    if random.random() < 0.15:  # 15% have notes
        notes_options = [
            "Approved by CFO", "Waiting for PO confirmation", "Rush order",
            "Recurring monthly charge", "Annual contract renewal",
            "Volume discount applied", "Pending budget approval"
        ]
        notes = random.choice(notes_options)
    
    inv_id = f"INV-{year}-{invoice_num:04d}"
    
    return {
        "invoice_id": inv_id,
        "vendor": vendor,
        "amount": round(total_amount, 2),
        "date": invoice_date.strftime("%Y-%m-%d"),
        "due_date": due_date.strftime("%Y-%m-%d"),
        "status": status,  # Keep for backward compatibility
        "approval_status": status,
        "payment_terms": payment_terms,
        "po_number": generate_po_number(),
        "category": category,
        "department": department,
        "subtotal": round(subtotal, 2),
        "tax_rate": tax_rate,
        "tax_amount": round(tax_amount, 2),
        "notes": notes
    }, items

def main():
    """Generate 250 invoices across 2022-2026 with rich metadata."""
    # Use Path for cross-platform compatibility
    project_root = Path(__file__).resolve().parent.parent
    invoices_dir = project_root / "data" / "invoices"
    reports_dir = project_root / "data" / "reports"
    
    invoices_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    invoice_data_list = []
    
    # Generate invoices across multiple years for historical depth
    years_distribution = {
        2022: 40,   # 40 invoices from 2022
        2023: 60,   # 60 invoices from 2023
        2024: 80,   # 80 invoices from 2024
        2025: 50,   # 50 invoices from 2025
        2026: 20    # 20 invoices from 2026 (YTD)
    }
    
    invoice_counter = 1
    for year, count in years_distribution.items():
        print(f"Generating {count} invoices for {year}...")
        for i in range(1, count + 1):
            invoice_data, items = generate_invoice_data(i, year)
            
            # Generate PDF
            output_path = invoices_dir / f"{invoice_data['invoice_id']}.pdf"
            generate_invoice_pdf(invoice_data, items, str(output_path))
            
            invoice_data_list.append(invoice_data)
            invoice_counter += 1
    
    # Save comprehensive CSV
    df = pd.DataFrame(invoice_data_list)
    csv_path = project_root / "data" / "invoice_summary.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n✅ Generated {len(invoice_data_list)} invoices")
    print(f"📊 Total amount: ${df['amount'].sum():,.2f}")
    print(f"📁 Saved to: {csv_path}")
    
    # Generate comprehensive reports
    print("\n📄 Generating audit reports...")
    from generate_reports import generate_all_reports
    generate_all_reports(str(csv_path))
    
    return df

if __name__ == "__main__":
    main()
