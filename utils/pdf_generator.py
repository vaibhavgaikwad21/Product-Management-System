import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics

# Register a Unicode font for ₹ symbol
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

def generate_pdf(
    customer_name,
    customer_contact,
    bill_items,
    gst_percent=18,
    discount_percent=0,
    logo_path="assets/logo.png",
    shop_name="Prodexa",
    shop_address="123 Main Street, Pune, Maharashtra",
    shop_phone="+91-9876543210",
    shop_pin="411001",
    output_folder="bills"
):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    filename = f"{customer_name.replace(' ', '_')}_{now}.pdf"
    filepath = os.path.join(output_folder, filename)

    doc = SimpleDocTemplate(filepath, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Shop logo
    if os.path.exists(logo_path):
        img = Image(logo_path, width=60, height=60)
        elements.append(img)

    # Shop details
    elements.append(Paragraph(f"<b>{shop_name}</b>", styles['Title']))
    elements.append(Paragraph(f"{shop_address}", styles['Normal']))
    elements.append(Paragraph(f"Phone: {shop_phone} | PIN: {shop_pin}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Customer Info
    elements.append(Paragraph(f"<b>Customer Name:</b> {customer_name}", styles['Normal']))
    elements.append(Paragraph(f"<b>Contact:</b> {customer_contact}", styles['Normal']))
    elements.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Table headers
    data = [["Product", "Quantity", "Price (Rs)", "Total (Rs)"]]
    total_amount = 0

    for item in bill_items:
        name, qty, price, total = item
        data.append([name, str(qty), f"{price:.2f}", f"{total:.2f}"])
        total_amount += total

    # GST & Discount
    gst_amount = total_amount * gst_percent / 100
    discounted_total = total_amount + gst_amount
    discount_amount = discounted_total * discount_percent / 100
    final_amount = discounted_total - discount_amount

    # Add totals to table
    data.append(["", "", "Subtotal", f"{total_amount:.2f}"])
    data.append(["", "", f"GST ({gst_percent}%)", f"{gst_amount:.2f}"])
    if discount_percent > 0:
        data.append(["", "", f"Discount ({discount_percent}%)", f"- {discount_amount:.2f}"])
    data.append(["", "", "Total", f"Rs{final_amount:.2f}"])

    # Table styling
    table = Table(data, colWidths=[200, 100, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'HeiseiMin-W3'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 24))
    elements.append(Paragraph("<i>Thank you for shopping with us!</i>", styles['Normal']))

    # Generate the PDF
    doc.build(elements)

    return filepath  # Return path so you can use it for WhatsApp etc.
