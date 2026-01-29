import PyPDF2
from utils.skill_dictionary import SKILLS
import re

def extract_resume_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_skills(text):
    text = text.lower()
    return list(set(skill for skill in SKILLS if skill in text))

def extract_experience(text):
    matches = re.findall(r'(\d+)\+?\s+years', text.lower())
    return max(map(int, matches)) if matches else 0
