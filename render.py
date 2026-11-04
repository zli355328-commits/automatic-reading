import argparse
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph

parser = argparse.ArgumentParser()
parser.add_argument("source", type=Path)
parser.add_argument("destination", type=Path)
parser.add_argument("--font", required=True)
args = parser.parse_args()
pdfmetrics.registerFont(TTFont("Reading", args.font))
styles = [
    ParagraphStyle(str(size), fontName="Reading", fontSize=size,
                   leading=size + 7, wordWrap="CJK", spaceAfter=10,
                   keepWithNext=size != 11)
    for size in (24, 17, 13, 11)
]
story = []
for line in args.source.read_text(encoding="utf-8-sig").splitlines():
    if not line.strip():
        continue
    prefix, _, value = line.partition(" ")
    level = {"#": 0, "##": 1, "###": 2}.get(prefix, 3)
    story.append(Paragraph(escape((value if level < 3 else line).replace("**", "")), styles[level]))
with args.destination.open("xb") as output:
    SimpleDocTemplate(output).build(story)
