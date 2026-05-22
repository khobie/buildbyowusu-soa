"""Generate admission brochure PDF."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

out = os.path.join(os.path.dirname(__file__), '..', 'app', 'static', 'docs', 'admission_brochure.pdf')
os.makedirs(os.path.dirname(out), exist_ok=True)
c = canvas.Canvas(out, pagesize=A4)
c.setFont('Helvetica-Bold', 18)
c.drawString(50, 800, 'Ridge School of Anaesthesia')
c.setFont('Helvetica', 12)
lines = [
    'Admissions Brochure 2025/2026',
    '',
    'Programme:',
    '- BSc in Anaesthesia (4 Years)',
    '',
    'Contact: info@ridgeanaesthesia.edu',
    'Apply online at ridgeanaesthesia.edu/admissions',
]
y = 760
for line in lines:
    c.drawString(50, y, line)
    y -= 20
c.save()
print(f'Created {out}')
