from skills import skills
import re

def extract_skills(text):
    extracted_skills = {category: set() for category in skills}

    for category, skill_list in skills.items():
        for skill in skill_list:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text.lower()):
                extracted_skills[category].add(skill)

    return {category: ",".join(skill_set) if skill_set else "None" for category, skill_set in extracted_skills.items()}
# from skillID import skills_dict
# import re
# def extract_skills(text):
#     skills_found=[]
#     for category,skills in skills_dict.items():
#         for skill,skill_id in skills.items():
#             if re.search(r"\b"+re.escape(skill)+r"\b",text,re.IGNORECASE):
#                 skills_found.append({
#                 'skillCategory':category,
#                 'skillCategoryID':skill_id
#             })
#     return skills_found
