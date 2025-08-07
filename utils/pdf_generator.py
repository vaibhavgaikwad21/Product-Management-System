# pdf_generator.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf(filename, items, total_amount):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 50, "🛍️ My Shop - Customer Bill")

    c.setFont("Helvetica", 10)
    c.drawRightString(width - 50, height - 70, f"Date: {datetime.now().strftime('%d-%m-%Y')}")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 100, "Product")
    c.drawString(200, height - 100, "Quantity")
    c.drawString(300, height - 100, "Price (₹)")
    c.drawString(400, height - 100, "Total (₹)")
    c.line(45, height - 105, width - 45, height - 105)

    c.setFont("Helvetica", 11)
    y = height - 130
    for item in items:
        c.drawString(50, y, str(item['name']))
        c.drawString(200, y, str(item['quantity']))
        c.drawString(300, y, f"₹{item['price']}")
        c.drawString(400, y, f"₹{item['total']}")
        y -= 20
        if y < 100:
            c.showPage()
            y = height - 50

    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(width - 50, y - 20, f"Grand Total: ₹{total_amount}")

    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width / 2, 40, "Thank you for shopping with us! 🙏")
    c.save()
