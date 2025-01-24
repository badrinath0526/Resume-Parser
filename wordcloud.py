from wordcloud import WordCloud
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

text="The dog jumped over the fence. The dog is happy"

wordloud=WordCloud(height=400,width=800,background_color='white').generate(text)

plt.figure(figsize=(10,6))
plt.imshow(wordloud,interpolation='bilinear')
plt.axis('off')
plt.show()
import nltk
import numpy as np

# Example corpus with varying document lengths (word count)
corpus = [
    "The dog jumped over the fence.",
    "The dog is happy.",
    "The quick brown fox jumped over the lazy dog.",
    "Dogs are loyal and friendly animals. They make great pets.",
]

# Calculate word counts for each document
word_counts = [len(nltk.word_tokenize(doc)) for doc in corpus]

# Plot histogram of word counts
plt.hist(word_counts, bins=range(0, max(word_counts) + 1, 1), alpha=0.75, color='blue')
plt.title("Word Count Distribution")
plt.xlabel("Word Count")
plt.ylabel("Frequency")
plt.show()
def load_glove_embeddings(glove_file_path):
    embeddings={}
    with open(glove_file_path,'r',encoding='utf=8') as f:
        for line in f:
            tokens=line.strip().split()
            word=tokens[0]
            vector=np.array([float(val) for val in tokens[1:]])
            embeddings[word]=vector
    return embeddings

glove_file_path="/home/user/Downloads/glove.6B/glove.6B.100d.txt"

def cosine_similarity_chunks(chunk,glove_embeddings):
    chunk_vector= np.mean([glove_embeddings.get(word.text.lower(), np.zeros(100)) for word in chunk], axis=0)
    return chunk_vector
# def extract_job_title(text,glove_embeddings):

#     doc=nlp(text)
#     job_title_keywords = [
#             'manager', 'director', 'leader', 'executive', 'officer', 'specialist', 
#             'analyst', 'consultant', 'coordinator', 'engineer', 'developer', 'scientist', 
#             'technician', 'assistant', 'architect', 'planner', 'designer', 'advisor', 
#             'consultant', 'strategist', 'entrepreneur', 'chief', 'president', 'principal','instructor','professional'
#         ]
#     job_title_vectors={word:glove_embeddings.get(word,np.zeros(100)) for word in job_title_keywords}
#     potential_titles=[]

#     for chunk in doc.noun_chunks:
#         chunk_vector=cosine_similarity_chunks(chunk,glove_embeddings)
#         similarities={title:cosine_similarity([chunk_vector],[vector])[0][0] for title,vector in job_title_vectors.items()}

#         best_match=max(similarities,key=similarities.get)
#         if similarities[best_match]>0.5:
#             potential_titles.append(chunk.text.strip())

#     return potential_titles[0] if potential_titles else None

# glove_embeddings=load_glove_embeddings(glove_file_path)
# EDUCATION = [
#             'BE','B.E.', 'B.E', 'BS', 'B.S', 
#             'ME', 'M.E', 'M.E.', 'M.B.A', 'MBA', 'MS', 'M.S', 
#             'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
#             'SSLC', 'SSC' 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
#         ]
# def extract_education(text):
#     nlp_text=nlp(text)
#     nlp_text=[sent.text.strip() for sent in nlp_text.sents]

#     edu={}
#     for index,text in enumerate(nlp_text):
#         for tex in text.split():
#             tex=re.sub(r'[?|$|.|!|,]',r'',tex)
#             if tex.upper() in EDUCATION and tex not in STOPWORDS:
#                 edu[tex]=text+nlp_text[index+1]
    
#     education=[]
#     for key in edu.keys():
#         year=re.search(re.compile(r'(((20|19)(\d{})))'),edu[key])
#         if year:
#             education.append((key,''.join(year[0])))
#         else:
#             education.append(key)
#     return education

# from nltk.corpus import stopwords
# STOPWORDS = set(stopwords.words('english'))

# # Education Degrees
# def extract_job_title(text):
#     doc=nlp(text)
#     potential_titles=[]
#     for ent in doc.ents:
#         if ent.label_=='ORG' or ent.label_=='GPE' or ent.label=='PERSON' or ent.label_=='WORK_OF_ART':
            
#             job_title_keywords = [
#             'manager', 'director', 'leader', 'executive', 'officer', 'specialist', 
#             'analyst', 'consultant', 'coordinator', 'engineer', 'developer', 'scientist', 
#             'technician', 'assistant', 'architect', 'planner', 'designer', 'advisor', 
#             'consultant', 'strategist', 'entrepreneur', 'chief', 'president', 'principal','instructor','marketing'
#         ]
#             if any(keyword in ent.text.lower() for keyword in job_title_keywords):
#                 potential_titles.append(ent.text.strip())
#     return potential_titles[0] if potential_titles else None
#  job_title_prompt=f"Extract the job title from the following resume text: \n{text[:150]}"
#     job_title_inputs=tokenizer(job_title_prompt,return_tensors="pt",max_length=512,truncation=True)
#     job_title_outputs=model.generate(**job_title_inputs,max_length=30)
#     job_title=tokenizer.decode(job_title_outputs[0],skip_special_tokens=True)

#     organization_prompt=f"Extract the current organization from the following resume text: \n{text}"
#     organization_inputs=tokenizer(organization_prompt,return_tensors="pt",max_length=512,truncation=True)
#     organization_outputs=model.generate(**organization_inputs,max_length=30)
#     current_organization=tokenizer.decode(organization_outputs[0],skio_special_tokens=True)