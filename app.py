from flask import Flask,request,jsonify,render_template
from werkzeug.utils import secure_filename
import os 
import spacy
import pdfplumber
import re
from transformers import pipeline
app=Flask(__name__)
# UPLOAD_FOLDER="./uploads"
# app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
# os.makedirs(UPLOAD_FOLDER,exist_ok=True)
nlp=spacy.load("en_core_web_sm")

t5_pipeline=pipeline("text2text-generation",model="google/flan-t5-large",tokenizer="google/flan-t5-large")


ALLOWED_EXTENSIONS={'pdf','docx'}

def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(file_path):
    with pdfplumber.open(file_path) as pdf:
        text=""
        for page in pdf.pages:
            text+=page.extract_text()
        return text

def parse_resume(file_path):
    text=extract_text(file_path)
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

            
    job_title_prompt=f"Extract the job title from the following resume text: \n{text[:150]}"
    job_title_result=t5_pipeline(job_title_prompt,max_length=100,num_return_sequences=True)
    job_title=job_title_result[0]['generated_text']

    organization_prompt=f"Extract the current organization name from the following resume text: \n{text}"
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

if __name__=='__main__':
    app.run(host='192.168.10.169',port=5000,debug=True)