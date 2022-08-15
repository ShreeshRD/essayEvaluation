from sklearn.feature_extraction.text import HashingVectorizer #, CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import text_preprocess as tp

def str_hash(string):
    string = ''.join(string)
    return sum([ord(ch) for ch in string])

def sim_score(pat, txt,):
    vectorizer = HashingVectorizer()
    txt = txt.split(' ')
    #tp.txt_prep(txt) # split into words
    pat = pat.split(' ')
    #tp.txt_prep(pat)
    #print('\npattern:\n', pat)
    #print('\ntext:\n', txt, '\n\n\n')
    m = len(pat)
    n = len(txt)
    res = 0
    p_hsh = str_hash(pat)
    t_hsh = str_hash(txt[:m])
    p_vec = vectorizer.fit_transform([' '.join(pat)]).toarray()
    
    if abs(p_hsh - t_hsh) < 10 * m:
        t_vec = vectorizer.fit_transform([' '.join(txt[:m])]).toarray()
        score = cosine_similarity(p_vec, t_vec)[0][0]
        res = max(res, score)
        # print(txt[:m], score)
        # print(t_hsh)
    
    for i in range(n - m):
        t_hsh -= str_hash(txt[i])
        t_hsh += str_hash(txt[i + m])
        #print(txt[i],txt[i+m], txt[i+1:i+m+1])
        if abs(p_hsh - t_hsh) <= 10 * m: # chk similar hsh then vec
            t_vec = vectorizer.fit_transform([' '.join(txt[i+1:i + m+1])]).toarray()
            score = cosine_similarity(p_vec, t_vec)[0][0]
            res = max(res, score)
            # print(txt[i+1:i + m+1], score)
            # print(t_hsh)
    return res

if __name__ == '__main__':
    txt = '''Garbage Collector is the program running in the background that looks into all the objects in the memory and find out objects that are not referenced by any part of the program.Java Garbage Collection is the process to identify and remove the unused objects from the memory and free space.One of the best feature of java programming language is the automatic garbage collection, unlike other programming languages such as C where memory allocation '''
    pat = 'memory allocation and deallocation is a manual process.'
    
    # vectorizer = HashingVectorizer()
    print(sim_score(pat, txt))