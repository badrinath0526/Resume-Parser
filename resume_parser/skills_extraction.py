from skills import skills
import re

def extract_skills(text):
    extracted_skills = {category: set() for category in skills}

    for category, skill_list in skills.items():
        for skill in skill_list:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text.lower()):
                extracted_skills[category].add(skill)

    return {category: list(skill_set) for category, skill_set in extracted_skills.items()}
