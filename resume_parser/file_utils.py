import json
import os

# File handling
ALLOWED_EXTENSIONS = {'pdf','docx'}

def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_known_job_titles(known_job_titles, KNOWN_TITLES_FILE="known_job_titles.json"):
    """Save the updated set of job titles to the JSON file."""
    with open(KNOWN_TITLES_FILE, "w") as file:
        json.dump(list(known_job_titles), file)
