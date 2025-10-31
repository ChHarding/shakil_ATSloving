# resume_reader.py
import os
from PyPDF2 import PdfReader
from docx import Document

def read_resume_text(file_path: str) -> str:
    """Extract text from PDF, DOCX, or TXT resume files."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = ""
        try:
            with open(file_path, "rb") as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            raise ValueError(f"Error reading PDF: {e}")
        return text.strip()

    elif ext == ".docx":
        text = ""
        try:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            raise ValueError(f"Error reading DOCX: {e}")
        return text.strip()

    elif ext == ".txt":
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            raise ValueError(f"Error reading TXT: {e}")

    else:
        raise ValueError("Unsupported file type. Please use PDF, DOCX, or TXT.")