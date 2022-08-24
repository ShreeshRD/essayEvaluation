'''
Dependencies:
pip install openpyxl
'''

import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from text_preprocess import txt_prep
import pandas as pd

def vectorize(Text): return TfidfVectorizer().fit_transform(Text).toarray()
def similarity(doc1, doc2): return cosine_similarity([doc1, doc2])

def check_plagiarism(user_notes, user_files):
    user_notes = [txt_prep(n) for n in user_notes]
    #print(user_notes)
    vectors = vectorize(user_notes)
    s_vectors = list(zip(user_files, vectors))
    plagiarism_results = set()
    for student_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((student_a, text_vector_a))
        del new_vectors[current_index]
        for student_b, text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            student_pair = sorted((student_a, student_b))
            score = (student_pair[0], student_pair[1], sim_score * 100)
            if sim_score > 0.3:
                plagiarism_results.add(score)
    return plagiarism_results

def get_local_score(path, name, n):
    '''
    ORIGINAL CODE
    user_files = [doc for doc in os.listdir(path) if doc.endswith('.txt')]
    user_notes = [open(path + _file, encoding='utf-8').read() for _file in user_files]
    for data in check_plagiarism(user_notes, user_files):
        print(data)
    '''
    os.chdir(path)
    df = pd.read_excel(name)
    essays = df['essay'].head(n)
    user_files = [i for i in range(50)]
    user_notes = list(essays)
    
    return check_plagiarism(user_notes, user_files)

if __name__ == '__main__':
    n = 50 # Number of essays
    path = 'E:\\Study\\Capstone\\PROJECT (code)\\DATAAAA'
    file_name = 'training_set_rel3.xlsx'

    for data in get_local_score(path, file_name, n):
        print(data)
