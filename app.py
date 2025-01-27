from flask import Flask,request,jsonify,render_template
from werkzeug.utils import secure_filename
import os 
import spacy
import pdfplumber
import re
from transformers import pipeline
import nltk
import mysql.connector

db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_new_password",
    database='resume_parser'
)

cursor=db.cursor()

app=Flask(__name__)
nlp=spacy.load("en_core_web_sm")

t5_pipeline=pipeline("text2text-generation",model="google/flan-t5-large",tokenizer="google/flan-t5-large")


ALLOWED_EXTENSIONS={'pdf'}

known_job_titles={"Software Engineer","Software Developer","AI Developer","Data Scientist","Project Manager","Web Developer","Business Analyst"}

def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(file_path):
    with pdfplumber.open(file_path) as pdf:
        text=""
        for page in pdf.pages:
            text+=page.extract_text()
        return text

def extract_organization(text):
    keywords=['Work History','Employment','Professional Background','Work Experience','Professional Experience','Employment History',
          'EXPERIENCE','WORK HISTORY','EMPLOYMENT','PROFESSIONAL BACKGROUND','WORK EXPERIENCE','PROFESSIONAL EXPERIENCE','EMPLOYMENT HISTORY','Experience']
    for keyword in keywords :
        if keyword in text:
            start=text.find(keyword)
        
            return text[start:start+700]
    return text

def extract_job_title_from_dict(text):
    for title in known_job_titles:
        if title.lower() in text.lower():
            return title
    return None


def parse_resume(file_path):
    text=extract_text(file_path)
    organization_section=extract_organization(text)
    # print(organization_section)
    email=None
    pattern=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.?[A-Za-z]{2,}\b"
    match=re.search(pattern,text)

    if match:
        email=match.group()
    else:
        doc=nlp(text)
        for token in doc:
            if token.like_email:
                email=token.text
                break
    email=email or "Email not found"

    job_title=extract_job_title_from_dict(text)
    if not job_title:   
        job_title_prompt=f"Extract the job title from the following resume text. Return only the job title.\n{text}"
        job_title_result=t5_pipeline(job_title_prompt,max_length=100,num_return_sequences=True)
        job_title=job_title_result[0]['generated_text']

        if job_title not in known_job_titles:
            known_job_titles.add(job_title)


    organization_prompt=f"Identify the most recently worked organization name from the following resume text. \n{organization_section}"
    organization_result=t5_pipeline(organization_prompt,max_length=100,num_return_sequences=True)
    current_organization=organization_result[0]['generated_text']

    return{
        "Email": email,
        "Job title": job_title.strip(),
        "Current organization": current_organization.strip(",")
    }
            


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/parse-resume",methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error":"No file part"}),400
    
    file=request.files['file']

    if file.filename=='':
        return jsonify({"Error":"No selected file"}),400
    
    if file and allowed_filename(file.filename):
        # filename=secure_filename(file.filename)
        # file_path=os.path.join(app.config['UPLOAD_FOLDER'],filename)
        # file.save(file_path)

        result=parse_resume(file)
        return jsonify(result),200
    return jsonify({'error':'Invalid file formats'}),400

@app.route("/submit-resume",methods=['POST'])
def submit_resume():
    data=request.json()
    print(data)
    email=data.get("Email")
    job_title=data.get("Job title")
    organization=data.get("Current organization")

    query="insert into resumes(email,job_title,organization) values(%s %s %s)"
    values=(email,job_title,organization)
    cursor.execute(query,values)
    db.commit()

    return jsonify({"message":"Resume details successfully stored in the database"})

if __name__=='__main__':
    app.run(host='192.168.10.169',port=5000,debug=True)