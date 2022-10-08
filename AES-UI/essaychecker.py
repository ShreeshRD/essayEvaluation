import gensim.models.keyedvectors as word2vec
import numpy as np
import os
from nltk.corpus import stopwords
import re

#lSTM
from keras.layers import Embedding, LSTM, Dense, Dropout, Lambda, Flatten
from keras.models import Sequential, load_model, model_from_config
import keras.backend as K

def get_model():
    """Define the model."""
    model = Sequential()
    model.add(LSTM(300, dropout=0.4, recurrent_dropout=0.4, input_shape=[1, 300], return_sequences=True))
    model.add(LSTM(64, recurrent_dropout=0.4))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='relu'))

    model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['mae'])
    model.summary()

    return model

def essay_to_wordlist(essay_v, remove_stopwords):
    """Remove the tagged labels and word tokenize the sentence."""
    essay_v = re.sub("[^a-zA-Z]", " ", essay_v)
    words = essay_v.lower().split()
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
    return (words)

def makeFeatureVec(words, model, num_features):
    """Make Feature Vector from the words list of an Essay."""
    featureVec = np.zeros((num_features,),dtype="float32")
    num_words = 0.
    index2word_set = set(model.wv.index2word)
    for word in words:
        if word in index2word_set:
            num_words += 1
            featureVec = np.add(featureVec,model[word])        
    featureVec = np.divide(featureVec,num_words)
    return featureVec

def getAvgFeatureVecs(essays, model, num_features):
    """Main function to generate the word vectors for word2vec model."""
    counter = 0
    essayFeatureVecs = np.zeros((len(essays),num_features),dtype="float32")
    for essay in essays:
        essayFeatureVecs[counter] = makeFeatureVec(essay, model, num_features)
        counter = counter + 1
    return essayFeatureVecs

def evaluate(content):
    current_path = "D:\Shreesh\Study\Capstone\PROJECT (code)\Automated-Essay--Scoring-master\mysite\grader"

    #content = """Dear @ORGANIZATION1, @CAPS1 has been brought to my attention that some people feel that computers are bad for us. Some people say that they are a distraction to our physicaland mental health. Although I can see how some people would think this, I believe that computers are a good benifit to all society. I believe this because computers can help people learn, stay intach with friends or family that live faraway, and stay orginized. Sometimes people are on the computer, learning and they don't even know @CAPS1. Simply by visiting the @ORGANIZATION2 homepage, you automaticly see the news feeds of things happening around the world. Other times people go online diliberatly to learn. If someone is thinking about going to @LOCATION1 then they would probably go on the internet to learn about @CAPS1. Simply by searching equadore many choices will pop up you climate, sesonal weather, hotel options, and other farts. But thats not the only way people are learning on the internet. Now, many college students have the option of taking their lessons online. This is because some students like calm quietness or own house the distractions of sitting in class. Friends could be a big distraction in class, but how can you stay intouch with your friends if they moved away? I remember in second grade my bestfriend, @LOCATION2, move away. I was so sad. I badey ever talked to her, but then one day our parents set us up on a vidio chat! I felt like I was right their with her! This was great, and I though about how many people could use this to talk to relatives or friends. Another great way to stay intouch into friends and family is through e-mail. By writing a message and sending @CAPS1 can make staying in touch so easey, and your personal wants can chat and emails are a easey thing to send world wide. So many people love to type on a keyboard as well, but so many different papers that you type could be lost. I, for me, hate clutter, and I have so many school binders for papers to be lost in. This is why I take great advantage of typing my paper every chance I get. My computer keeps me orginiced because I could never loose my work. File save, is an idiot proof way to keep all your files in a safe place. Then all you have to do is press print to get a hard copy. I am sure that many people love using their computer for the same reason. Also, I myself am a much faster typer than I am writer so my work is a lot needey on the computer. As you can see their are plenty of reasons why using a computer is goof for our society you can learn, stay intouch with friends and family, and stay orginiced. Many people, could agree with me. Don't you?"""

    num_features = 300
    model = word2vec.KeyedVectors.load_word2vec_format(os.path.join(current_path, "deep_learning_files/word2vec.bin"), binary=True)
    clean_test_essays = []
    clean_test_essays.append(essay_to_wordlist( content, remove_stopwords=True ))
    testDataVecs = getAvgFeatureVecs( clean_test_essays, model, num_features )
    testDataVecs = np.array(testDataVecs)
    testDataVecs = np.reshape(testDataVecs, (testDataVecs.shape[0], 1, testDataVecs.shape[1]))

    lstm_model = get_model()
    lstm_model.load_weights(os.path.join(current_path, "deep_learning_files/final_lstm.h5"))
    preds = lstm_model.predict(testDataVecs)
    return str(preds[0][0])

if __name__ == "__main__":
    text = """Dear @ORGANIZATION1, @CAPS1 has been brought to my attention that some people feel that computers are bad for us. Some people say that they are a distraction to our physicaland mental health. Although I can see how some people would think this, I believe that computers are a good benifit to all society. I believe this because computers can help people learn, stay intach with friends or family that live faraway, and stay orginized. Sometimes people are on the computer, learning and they don't even know @CAPS1. Simply by visiting the @ORGANIZATION2 homepage, you automaticly see the news feeds of things happening around the world. Other times people go online diliberatly to learn. If someone is thinking about going to @LOCATION1 then they would probably go on the internet to learn about @CAPS1. Simply by searching equadore many choices will pop up you climate, sesonal weather, hotel options, and other farts. But thats not the only way people are learning on the internet. Now, many college students have the option of taking their lessons online. This is because some students like calm quietness or own house the distractions of sitting in class. Friends could be a big distraction in class, but how can you stay intouch with your friends if they moved away? I remember in second grade my bestfriend, @LOCATION2, move away. I was so sad. I badey ever talked to her, but then one day our parents set us up on a vidio chat! I felt like I was right their with her! This was great, and I though about how many people could use this to talk to relatives or friends. Another great way to stay intouch into friends and family is through e-mail. By writing a message and sending @CAPS1 can make staying in touch so easey, and your personal wants can chat and emails are a easey thing to send world wide. So many people love to type on a keyboard as well, but so many different papers that you type could be lost. I, for me, hate clutter, and I have so many school binders for papers to be lost in. This is why I take great advantage of typing my paper every chance I get. My computer keeps me orginiced because I could never loose my work. File save, is an idiot proof way to keep all your files in a safe place. Then all you have to do is press print to get a hard copy. I am sure that many people love using their computer for the same reason. Also, I myself am a much faster typer than I am writer so my work is a lot needey on the computer. As you can see their are plenty of reasons why using a computer is goof for our society you can learn, stay intouch with friends and family, and stay orginiced. Many people, could agree with me. Don't you?"""
    print("YOUR SCORE IS: ",evaluate(text))