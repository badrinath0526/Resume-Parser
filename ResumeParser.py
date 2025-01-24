import pdfplumber
import spacy
import re
import numpy as np

from spacy.matcher import Matcher

def extract_text(path):
    with pdfplumber.open(path) as pdf:
        text=""

        for page in pdf.pages:
            text+=page.extract_text()
        return text

path="/home/user/Downloads/Azhar khan.pdf"

# print(extracted_text)

def extract_email_from_resume(text):
    email=None
    pattern=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.?[A-Za-z]{2,}\b"
    match=re.search(pattern,text)
    if match:
        email=match.group()
    return email




nlp=spacy.load("en_core_web_lg")



def extract_education(text):
    education=[]    
    pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.\w+|\bBachelor(?:'s)?|\bMaster(?:'s)?|Degree(?:'s)?|\bPh\.D)\s(?:\w+\s)*\w+"

    matches=re.findall(pattern,text)
    for match in matches:
        education.append(match.strip())
    return education



def extract_name(text):
    nlp=spacy.load("en_core_web_sm")
    matcher=Matcher(nlp.vocab)

    patterns=[
        [{'POS':'PROPN'},{'POS':'PROPN'}],
        [{'POS':'PROPN'},{'POS':'PROPN'},{'POS':'PROPN'}],
        [{'POS':'PROPN'},{'POS':'PROPN'},{'POS':'PROPN'},{'POS':'PROPN'}]
    ]

    for pattern in patterns:
        matcher.add('NAME',patterns=[pattern])
    doc=nlp(text)
    matches=matcher(doc)
    for match_id,start,end in matches:
        span=doc[start:end]
        return span

        
    return None

def previous_organization(text):
    if 'experience' in text.lower():
        
        return 
        
    return "No prior experience"

text=extract_text(path)
email=extract_email_from_resume(text)
print("Email:",email)
education=extract_education(text)
print("Qualification: ",education)
name=extract_name(text)
print("Name: ",name)



