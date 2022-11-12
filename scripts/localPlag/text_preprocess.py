import nltk
from nltk import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
#from nltk.stem.snowball import SnowballStemmer
import regex as re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords



def txt_prep(text):
    #text = re.sub(r'[^\w\s]', "", text)
    text = re.sub(r"\[.*\]|\{.*\}|\(|\)", "", text)
    text = re.sub(r'[?!;:#@$%^&]', '', text)
    
    text = word_tokenize(text)
    
    stops = set(stopwords.words("english"))
    text = [word for word in text if word not in stops]
    
    wnl = WordNetLemmatizer()
    text = [wnl.lemmatize(word) for word in text]
    
    stemmer = LancasterStemmer()
    text = [stemmer.stem(word) for word in text]
    
    return " ".join(text)


if __name__ == '__main__':
    qq = '''Google began in January 1996 as a research project by Larry Page and Sergey Brin when they were both PhD students at Stanford University in California.[22][23][24] The project initially involved an unofficial "third founder", Scott Hassan, the original lead programmer who wrote much of the code for the original Google Search engine, but he left before Google was officially founded as a company;[25][26] Hassan went on to pursue a career in robotics and founded the company Willow Garage in 2006.'''
    
    print(" ".join(txt_prep(qq)))