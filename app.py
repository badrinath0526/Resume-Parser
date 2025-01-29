from flask import Flask, request, jsonify, render_template
from resume_parser.file_utils import allowed_filename
from resume_parser.text_extraction import extract_text, extract_organization, parse_resume
from resume_parser.skills_extraction import extract_skills
from resume_parser.job_title_extraction import extract_job_title_from_dict, add_job_title

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/parse-resume", methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"Error": "No selected file"}), 400
    if file and allowed_filename(file.filename):
        result = parse_resume(file)
        return jsonify(result), 200
    return jsonify({'error': 'Invalid file formats'}), 400

@app.route("/add-job-title", methods=['POST'])
def handle_job_title():
    data = request.json
    job_title = data.get("jobTitle")

    if not job_title:
        return jsonify({"error": "Missing job title"})
    try:
        add_job_title(job_title)
        return jsonify({"message": "Job title stored in json file"})
    except Exception as e:
        print(f'{e}')
        return jsonify({"error": "Failed to save in json file"})

if __name__ == '__main__':
    app.run(host='192.168.10.169', port=5000, debug=True)
