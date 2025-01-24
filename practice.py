import pdfplumber
import nltk
import re

def extract_text(path):
    with pdfplumber.open(path) as pdf:
        text=""
        for page in pdf.pages:
            text+=page.extract_text()
        return text

def extract_lines(text):
    lines=[el.strip() for el in text.split("\n") if len(el)>0]
    lines=[nltk.word_tokenize(el) for el in lines]
    lines=[nltk.pos_tag(el) for el in lines]

    return lines

def extract_sentences(text):
    sentences=nltk.sent_tokenize(text)
    sentences=[nltk.word_tokenize(sent) for sent in sentences]
    tokens=sentences
    sentences=[nltk.pos_tag(sent) for sent in sentences]
    dummy=[]
    for el in tokens:
        dummy+=el
    tokens=dummy
    return tokens

def extract_experience(lines):
    for sentence in lines:
        sen=" ".join([words[0].lower()for words in sentence])
        if re.search('experience',sen):
            sen_tokenized=nltk.word_tokenize(sen)
            tagged=nltk.pos_tag(sen_tokenized)
            entities=nltk.chunk.ne_chunk(tagged)
            print(entities)
            for subtree in entities.subtrees():
               
                for leaf in subtree.leaves():
                    print(leaf)
                    if(leaf[1])=='CD':
                        experience=leaf[0]
                        return experience
def extract_education(text):
    education=[]

    education_keywords=[
        'BE', 'B.E.', 'B.E', 'BS', 'B.S', 'C.A.', 'c.a.', 'B.Com', 'B. Com', 'M. Com', 'M.Com', 'M. Com .',
        'ME', 'M.E', 'M.E.', 'MS', 'M.S', 'Bsc', 'Msc', 'B. Pharmacy', 'B Pharmacy', 'M. Pharmacy',
        'BTECH', 'B.TECH', 'M.TECH', 'MTECH',
        'PHD', 'phd', 'ph.d', 'Ph.D.', 'MBA', 'mba', 'graduate', 'post-graduate', '5 year integrated masters', 'masters',
        'Bachelor of Technology', 'Master of Technology', 'CSE', 'ECE', 'EEE', 'Information Technology',
        'Mechanical Engineering', 'Computer Science and Engineering',
        'Electronics and Communication Engineering', 'Electrical and Electronics Engineering'
    ]

    for keyword in education_keywords:
        pattern=r"(?i)\b{}\b".format(re.escape(keyword))
        match=re.search(pattern,text)
        if match:
            education.append(match.group())
    
    education=[edu for edu in education if edu.upper()!='BE' and edu.upper()!='ME']
    education_string=', '.join(education)

    return education_string if education_string else "Not Found"


path="/home/user/Downloads/sample.pdf"
text=extract_text(path)
lines=extract_lines(text)
print(len(lines))

sentences=extract_sentences(text)
# print(sentences)
# exp=extract_experience(lines)
# print(exp)

education=extract_education(text)
print(education)

from transformers import pipeline

model =pipeline("text2text-generation",model="google/flan-t5-large")

instruction="""
Extract the education qualification from the below text of a resume:"""

input_text=f"{instruction}\n {text}"
print(input_text)
response=model(input_text,max_length=50,do_sample=False)
print(response)
current_org=response[0]['generated_text'].strip()
print("Current organization: ",current_org)
