# -*- coding: utf-8 -*-
# http://www.devshed.com/c/a/Python/Python-for-PDF-Generation/

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A4
# pdf = Canvas("test.pdf")
pdf = Canvas("test.pdf", pagesize = A4)
pdf.setFont("Courier", 12)
pdf.setStrokeColorRGB(1, 0, 0)
pdf.drawString(300, 300, "CLASSIFIED Cet été")
from reportlab.lib.units import cm, mm, inch, pica
pdf.drawString(2 * inch, inch, "For Your Eyes Only")
pdf.showPage()
pdf.save()
