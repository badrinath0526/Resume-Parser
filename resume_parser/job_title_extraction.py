import json
import os
from resume_parser.file_utils import save_known_job_titles
KNOWN_TITLES_FILE = "known_job_titles.json"

# Load known job titles
if os.path.exists(KNOWN_TITLES_FILE):
    try:
        with open(KNOWN_TITLES_FILE, "r") as file:
            known_job_titles= set(json.load(file))  # Load as a set for quick lookup
    except (json.JSONDecodeError, ValueError):
        print(f"Warning: {KNOWN_TITLES_FILE} contains invalid JSON. Initializing an empty set.")
        known_job_titles= set()
else:
    known_job_titles= {"Software Engineer", "Software Developer", "AI Developer", "Data Scientist", "Project Manager", "Web Developer", "Business Analyst"}

# Extract job title from known titles
def extract_job_title_from_dict(text):
    for title in known_job_titles:
        if title.lower() in text.lower():
            return title
    return None


# Add a new job title to the known job titles
def add_job_title(job_title):
    if job_title not in known_job_titles:
        known_job_titles.add(job_title)
        save_known_job_titles(known_job_titles)
