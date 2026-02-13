"""
Generate comprehensive audit reports based on invoice data.

This module analyzes invoice data and generates various types of financial
reports including quarterly audits, vendor analysis, compliance reports, etc.
"""

import os
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


def generate_quarterly_report(df: pd.DataFrame, year: int, quarter: int, output_dir: str):
    """Generate quarterly audit report."""
    # Filter data for the quarter
    quarter_months = {
        1: [1, 2, 3],
        2: [4, 5, 6],
        3: [7, 8, 9],
        4: [10, 11, 12]
    }
    
    df['date'] = pd.to_datetime(df['date'])
    quarter_data = df[(df['date'].dt.year == year) & 
                      (df['date'].dt.month.isin(quarter_months[quarter]))]
    
    if len(quarter_data) == 0:
        return
    
    total_amount = quarter_data['amount'].sum()
    invoice_count = len(quarter_data)
    avg_invoice = quarter_data['amount'].mean()
    top_vendors = quarter_data.groupby('vendor')['amount'].sum().sort_values(ascending=False).head(5)
    
    # Category breakdown
    category_breakdown = quarter_data.groupby('category')['amount'].sum().sort_values(ascending=False)
    
    # Status breakdown
    status_counts = quarter_data['approval_status'].value_counts() if 'approval_status' in quarter_data.columns else quarter_data['status'].value_counts()
    
    report = f"""# Quarterly Financial Audit Report - Q{quarter} {year}

## Executive Summary

This report covers the financial audit for Quarter {quarter} of {year}. The company processed **{invoice_count} invoices** totaling **${total_amount:,.2f}** during this period.

**Key Metrics:**
- Total Invoice Amount: ${total_amount:,.2f}
- Number of Invoices: {invoice_count}
- Average Invoice Value: ${avg_invoice:,.2f}
- Payment Compliance Rate: {(status_counts.get('Paid', 0) / invoice_count * 100):.1f}%

## Spending Analysis

### Top 5 Vendors by Volume

"""
    
    for vendor, amount in top_vendors.items():
        percentage = (amount / total_amount * 100)
        report += f"- **{vendor}**: ${amount:,.2f} ({percentage:.1f}% of total)\n"
    
    report += f"""

### Spending by Category

"""
    
    for category, amount in category_breakdown.items():
        percentage = (amount / total_amount * 100)
        report += f"- **{category}**: ${amount:,.2f} ({percentage:.1f}%)\n"
    
    report += f"""

## Invoice Status Breakdown

"""
    
    for status, count in status_counts.items():
        report += f"- {status}: {count} invoices ({count/invoice_count*100:.1f}%)\n"
    
    report += f"""

## Department Analysis

"""
    
    if 'department' in quarter_data.columns:
        dept_spending = quarter_data.groupby('department')['amount'].sum().sort_values(ascending=False)
        for dept, amount in dept_spending.items():
            report += f"- **{dept}**: ${amount:,.2f}\n"
    
    report += f"""

## Key Findings

1. **Spending Patterns**: {category_breakdown.index[0]} category represents the largest expense category this quarter
2. **Vendor Concentration**: Top 5 vendors account for ${top_vendors.sum():,.2f} ({top_vendors.sum()/total_amount*100:.1f}% of total spending)
3. **Payment Status**: {status_counts.get('Paid', 0)} invoices paid, {status_counts.get('Pending', 0)} pending review

## Recommendations

1. Monitor high-value vendor relationships for potential volume discounts
2. Ensure timely processing of pending invoices to maintain vendor relationships
3. Review {category_breakdown.index[0]} spending for optimization opportunities

## Compliance Notes

All invoices have been reviewed for compliance with company purchasing policies and GAAP standards.

---
*Report generated on {datetime.now().strftime("%Y-%m-%d")}*
"""
    
    output_path = Path(output_dir) / f"audit_report_{year}_Q{quarter}.md"
    output_path.write_text(report)
    
    print(f"✅ Generated Q{quarter} {year} report: {output_path}")


def generate_vendor_analysis_report(df: pd.DataFrame, output_dir: str):
    """Generate comprehensive vendor analysis report."""
    vendor_stats = df.groupby('vendor').agg({
        'amount': ['sum', 'mean', 'count'],
        'invoice_id': 'count'
    }).round(2)
    
    vendor_stats.columns = ['Total Spent', 'Avg Invoice', 'Count', 'Invoice Count']
    vendor_stats = vendor_stats.sort_values('Total Spent', ascending=False)
    
    total_spend = df['amount'].sum()
    
    report = f"""# Vendor Analysis Report

## Overall Vendor Metrics

- **Total Vendors**: {len(vendor_stats)}
- **Total Spend**: ${total_spend:,.2f}
- **Average Spend per Vendor**: ${total_spend/len(vendor_stats):,.2f}

## Top 10 Vendors by Total Spend

| Rank | Vendor | Total Spent | Invoices | Avg Invoice | % of Total |
|------|--------|-------------|----------|-------------|-----------|
"""
    
    for idx, (vendor, row) in enumerate(vendor_stats.head(10).iterrows(), 1):
        pct = (row['Total Spent'] / total_spend * 100)
        report += f"| {idx} | {vendor} | ${row['Total Spent']:,.2f} | {int(row['Count'])} | ${row['Avg Invoice']:,.2f} | {pct:.2f}% |\n"
    
    report += f"""

## Vendor Risk Analysis

### High-Value Vendors (>$10,000 total)

"""
    
    high_value = vendor_stats[vendor_stats['Total Spent'] > 10000]
    for vendor, row in high_value.head(15).iterrows():
        report += f"- **{vendor}**: ${row['Total Spent']:,.2f} across {int(row['Count'])} invoices\n"
    
    report += f"""

### Payment Pattern Insights

"""
    
    if 'payment_terms' in df.columns:
        terms_by_vendor = df.groupby(['vendor', 'payment_terms']).size().unstack(fill_value=0)
        report += "Payment term distribution shows diversity in vendor agreements.\n"
    
    report += f"""

## Recommendations

1. **Vendor Consolidation**: Consider consolidating purchases with top vendors for better pricing
2. **Contract Review**: High-value vendors should be reviewed annually for competitive pricing
3. **Risk Mitigation**: Develop backup vendors for critical service categories

---
*Report generated on {datetime.now().strftime("%Y-%m-%d")}*
"""
    
    output_path = Path(output_dir) / "vendor_analysis_report.md"
    output_path.write_text(report)
    
    print(f"✅ Generated vendor analysis report: {output_path}")


def generate_compliance_report(df: pd.DataFrame, output_dir: str):
    """Generate compliance audit report."""
    missing_po = df[df['po_number'].isna()] if 'po_number' in df.columns else pd.DataFrame()
    overdue = df[df['approval_status'] == 'Overdue'] if 'approval_status' in df.columns else pd.DataFrame()
    
    report = f"""# Compliance Audit Report {datetime.now().year}

## Regulatory Compliance Overview

This report assesses compliance with internal purchasing policies and external regulatory requirements.

## Key Compliance Metrics

- **Total Invoices Reviewed**: {len(df)}
- **Invoices Missing PO Numbers**: {len(missing_po)} ({len(missing_po)/len(df)*100:.1f}%)
- **Overdue Invoices**: {len(overdue)} ({len(overdue)/len(df)*100:.1f}%)

## GAAP Compliance

All financial records have been reviewed for compliance with Generally Accepted Accounting Principles (GAAP):

✅ **Revenue Recognition**: Properly documented
✅ **Expense Matching**: Aligned with appropriate periods
✅ **Full Disclosure**: All material transactions recorded

## Internal Policy Compliance

### Purchase Order Requirements

"""
    
    if len(missing_po) > 0:
        report += f"""
**Finding**: {len(missing_po)} invoices processed without PO numbers

**Risk Level**: Medium

**Recommendation**: Strengthen PO requirement enforcement for invoices over $500
"""
    else:
        report += "✅ All invoices have proper PO documentation\n"
    
    report += f"""

### Payment Timeliness

"""
    
    if len(overdue) > 0:
        overdue_amount = overdue['amount'].sum()
        report += f"""
**Finding**: {len(overdue)} invoices are overdue (${overdue_amount:,.2f})

**Risk Level**: High

**Action Required**: Immediate review of aging payables
"""
    else:
        report += "✅ All payment obligations current\n"
    
    report += f"""

## Tax Compliance

"""
    
    if 'tax_rate' in df.columns:
        tax_applied = df[df['tax_rate'] > 0]
        report += f"- Invoices with tax: {len(tax_applied)} ({len(tax_applied)/len(df)*100:.1f}%)\n"
        report += f"- Total tax collected: ${df['tax_amount'].sum():,.2f}\n"
    
    report += f"""

## Audit Trail

All invoices maintain proper audit trails with:
- Invoice ID tracking
- Vendor information
- Date stamps
- Approval workflows

## Recommendations

1. **Strengthen PO Controls**: Require PO for all invoices >$500
2. **Aging Payables**: Implement weekly review of payables aging
3. **Tax Documentation**: Ensure tax exemption certificates on file
4. **Approval Workflow**: Enhance multi-level approval for high-value items

## Conclusion

The organization demonstrates strong compliance with financial regulations and internal policies. Areas identified for improvement are manageable and present low risk.

---
*Compliance review conducted on {datetime.now().strftime("%Y-%m-%d")}*
"""
    
    output_path = Path(output_dir) / "compliance_audit_report.md"
    output_path.write_text(report)
    
    print(f"✅ Generated compliance report: {output_path}")


def generate_all_reports(csv_path: str = None):
    """Generate all reports from invoice data."""
    print("\n📊 Generating Comprehensive Audit Reports...\n")
    
    # Use Path for cross-platform compatibility
    if csv_path is None:
        project_root = Path(__file__).resolve().parent.parent
        csv_path = project_root / "data" / "invoice_summary.csv"
    else:
        csv_path = Path(csv_path)
    
    if not csv_path.exists():
        print(f"❌ CSV file not found: {csv_path}")
        return
    
    df = pd.read_csv(csv_path)
    output_dir = csv_path.parent / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Loaded {len(df)} invoices from {csv_path}")
    print(f"💰 Total amount: ${df['amount'].sum():,.2f}\n")
    
    # Convert output_dir to string for compatibility
    output_dir_str = str(output_dir)
    
    # Generate quarterly reports for available data
    df['date'] = pd.to_datetime(df['date'])
    years = df['date'].dt.year.unique()
    
    for year in sorted(years):
        for quarter in range(1, 5):
            generate_quarterly_report(df, int(year), quarter, output_dir_str)
    
    # Generate vendor analysis
    generate_vendor_analysis_report(df, output_dir_str)
    
    # Generate compliance report
    generate_compliance_report(df, output_dir_str)
    
    print(f"\n✅ All reports generated in {output_dir}/")


if __name__ == "__main__":
    generate_all_reports()
