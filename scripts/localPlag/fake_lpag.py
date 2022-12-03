from sklearn.feature_extraction.text import HashingVectorizer #, CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#import text_preprocess as tp
import os

def str_hash(string):
    string = ''.join(string)
    return sum([ord(ch) for ch in string])

def sim_score(pat, txt):
    vectorizer = HashingVectorizer()
    txt = txt.split(' '); pat = pat.split(' ')
    m = len(pat); n = len(txt)
    res = 0
    p_hsh = str_hash(pat); t_hsh = str_hash(txt[:m])
    p_vec = vectorizer.fit_transform([' '.join(pat)]).toarray()
    
    if abs(p_hsh - t_hsh) < 10 * m:
        t_vec = vectorizer.fit_transform([' '.join(txt[:m])]).toarray()
        score = cosine_similarity(p_vec, t_vec)[0][0]
        res = max(res, score)
    
    for i in range(n - m):
        t_hsh -= str_hash(txt[i])
        t_hsh += str_hash(txt[i + m])
        if abs(p_hsh - t_hsh) <= 10 * m:
            t_vec = vectorizer.fit_transform([' '.join(txt[i+1:i + m+1])]).toarray()
            score = cosine_similarity(p_vec, t_vec)[0][0]
            res = max(res, score)
    return res

def lscores(name, pat, path):
    files = os.listdir(path)
    scores = []
    sents = pat.split('.')
    n = len(sents)
    for file in files:
        if name in file:
            continue
        score = 0
        fscore = 0
        with open(path+'/'+file, 'r') as my_file:
            text = my_file.read()
            for sent in sents:
                score = round(sim_score(sent, text) * 100,2)
                fscore += score
            fscore /= n
        scores.append(str(round(fscore,2))+"% similarity with "+file[:-4])
    return scores

if __name__ == '__main__':
    name = "admin"
    with open("C:/Users/Shreesh/Programs/Capstone/Project/uploads/1/admin.txt") as file:
        t = file.read()
    print(lscores(name, t, "C:/Users/Shreesh/Programs/Capstone/Project/uploads/1"))
