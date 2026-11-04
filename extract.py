import argparse
from pathlib import Path
from pypdf import PdfReader

parser = argparse.ArgumentParser()
parser.add_argument("source", type=Path)
parser.add_argument("destination", type=Path)
args = parser.parse_args()
reader = PdfReader(args.source)
blank = []
with args.destination.open("x", encoding="utf-8") as output:
    for number, page in enumerate(reader.pages, 1):
        content = page.extract_text()
        if not content.strip():
            blank.append(number)
        output.write(f"\n@@ {number}\n{content}\n")
print(f"Pages: {len(reader.pages)}; no extractable text: {blank}")
