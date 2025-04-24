import fitz  # PyMuPDF
import re

def extract_sections_from_pdf(pdf_path: str) -> dict:
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()

    sections = {}
    matches = re.findall(r"\n(\d+\. .*?)(?=\n\d+\. |\Z)", text, re.DOTALL)
    if not matches:  # fallback if regex fails
        return {"Full Document": text.strip()}

    for match in matches:
        title = match.strip().split("\n")[0][:80]
        sections[title] = match.strip()

    return sections
