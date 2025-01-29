import pdfplumber
import re
import spacy
from transformers import pipeline
from resume_parser.job_title_extraction import extract_job_title_from_dict
from resume_parser.skills_extraction import extract_skills

nlp = spacy.load("en_core_web_sm")
t5_pipeline=pipeline("text2text-generation",model="google/flan-t5-large",tokenizer="google/flan-t5-large")

def extract_text(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text

def extract_organization(text):
    keywords = ['Work History', 'Employment', 'Professional Background', 'Work Experience', 'Professional Experience', 'Employment History']
    for keyword in keywords:
        if keyword in text:
            start = text.find(keyword)
            return text[start:start + 700]
    return text

def parse_resume(file_path):
    text = extract_text(file_path)
    organization_section = extract_organization(text)

    email = None
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.?[A-Za-z]{2,}\b"
    match = re.search(pattern, text)

    if match:
        email = match.group()
    else:
        doc = nlp(text)
        for token in doc:
            if token.like_email:
                email = token.text
                break
    email = email or "Email not found"

    job_title = extract_job_title_from_dict(text)
    if not job_title:
        job_title_prompt = f"Extract the job title from the following resume text. Return only the job title.\n{text}"
        job_title_result = t5_pipeline(job_title_prompt, max_length=100, num_return_sequences=True)
        job_title = job_title_result[0]['generated_text']

    organization_prompt = f"From the following resume text, extract the name of the most recent organization the candidate has worked for. Focus only on work history and return the organization name: \n{organization_section}"
    organization_result = t5_pipeline(organization_prompt, max_length=100, num_return_sequences=True)
    current_organization = organization_result[0]['generated_text']

    return {
        "Email": email,
        "Job title": job_title.strip(),
        "Current organization": current_organization.strip(","),
    }
