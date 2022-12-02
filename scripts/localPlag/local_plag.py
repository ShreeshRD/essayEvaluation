'''
Dependencies:
pip install openpyxl
'''

import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .text_preprocess import txt_prep
import pandas as pd

def vectorize(Text): return TfidfVectorizer().fit_transform(Text).toarray()
def similarity(doc1, doc2): return cosine_similarity([doc1, doc2])

def check_plagiarism(path):
    user_files = os.listdir(path)
    user_notes = []
    flag = 0
    for filename in user_files:
        with open(path+'\\'+filename, 'r') as file:
            user_notes.append(txt_prep(file.read()))
    # user_notes = [txt_prep(n) for n in user_notes]
    vectors = vectorize(user_notes)
    s_vectors = list(zip(user_files, vectors))
    plagiarism_results = []
    n = len(s_vectors)
    for i in range(n-1):
        for j in range(i+1, n):
            sim_score = similarity(s_vectors[i][1], s_vectors[j][1])[0][1]
            if sim_score < 0.3:
                continue
            student_pair = (s_vectors[i][0], s_vectors[j][0])
            if(sim_score == 1):
                if(s_vectors[i][0] == "source.txt" or s_vectors[j][0] == "source.txt"):
                    flag = 1
            score = [round(sim_score * 100,2),"% similarity between students",student_pair]
            plagiarism_results.append(score)
    return plagiarism_results, flag

def get_local_score(path, name, n):
    os.chdir(path)
    df = pd.read_excel(name)
    essays = df['essay'].head(n)
    user_files = [i for i in range(50)]
    user_notes = list(essays)
    
    return check_plagiarism(user_notes, user_files)

if __name__ == '__main__':
    n = 50 # Number of essays
    path = 'D:\\capstone project\\CODE\\data'
    file_name = 'training_set_rel3.xlsx'

    for data in get_local_score(path, file_name, n):
        for ele in data:
            print(ele, end = " ")
        print()