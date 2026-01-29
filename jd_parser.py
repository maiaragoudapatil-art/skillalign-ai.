from utils.skill_dictionary import SKILLS
import re

def extract_jd_skills(text):
    text = text.lower()
    return list(set(skill for skill in SKILLS if skill in text))

def extract_required_experience(text):
    matches = re.findall(r'(\d+)\+?\s+years', text.lower())
    return int(matches[0]) if matches else 0
