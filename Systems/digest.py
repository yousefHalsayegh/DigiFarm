import os 
os.environ["NLTK_DATA"]="data/"
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import download, pos_tag
from nltk.stem import WordNetLemmatizer


class Digest:

    def __init__(self):
        
        download("stopwords", download_dir="data/") 
        download("punkt_tab", download_dir="data/")
        download("averaged_perceptron_tagger_eng", download_dir="data/")
        download("wordnet", download_dir="data/")

        self.stopwords = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()
        
        

    def prepare(self, t):
        text = []
        sentences = sent_tokenize(t)
        for sentence in sentences:
           words = word_tokenize(sentence)
           ns_words = [word for word in words if word.casefold() not in self.stopwords ]
           pos_ns_word = pos_tag(ns_words)
           text.append([ self.lemmatizer.lemmatize(word[0]) for word in pos_ns_word])


        return text



    def eat(self):
        pass