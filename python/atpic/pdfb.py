import sys

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate,Spacer

if len(sys.argv) < 3:
    print "Usage: <script> textfile pdffile"
    sys.exit()
else:
    pdf = SimpleDocTemplate(sys.argv[2], pagesize = letter)
    story = []
    style = getSampleStyleSheet()
    text = file(sys.argv[1]).read()
    paragraphs = text.split("\n")
    for para in paragraphs:
        story.append(Paragraph(para, style["Normal"]))
        story.append(Spacer(0, inch * .1))
    pdf.build(story)
