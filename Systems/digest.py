import os 
os.environ["NLTK_DATA"]="data/"
from nltk.tokenize import  word_tokenize
from nltk.corpus import stopwords
from nltk import download, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist

class Digest:

    def __init__(self):

        self.stopwords = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()
        
        

    def prepare(self, t):
        text = []
        text_lemed = []
        #tokenized
        w = word_tokenize(t)
        words = [word.lower() for word in w]
        #removing stopwords (need to check if it is removing important things)
        ns_words = [word for word in words if word not in self.stopwords ]
        #adding a pos 
        pos_ns_word = pos_tag(ns_words)
        #lemmatizing by both using pos and not testing which one is better
        text.append([self.lemmatizer.lemmatize(word[0]) for word in pos_ns_word])
        
        text = " ".join(text[0])


        return text
    
    def prepare_lemed(self, t):
        text = []
        #tokenized
        w = word_tokenize(t)
        words = [word.lower() for word in w]
        #removing stopwords (need to check if it is removing important things)
        ns_words = [word for word in words if word not in self.stopwords ]
        #adding a pos 
        pos_ns_word = pos_tag(ns_words)
        #lemmatizing by both using pos and not testing which one is better
        text.append([self.lemmatizer.lemmatize(word[0], self.pos(word[1])) for word in pos_ns_word])

        text = " ".join(text[0])
        
        return text

    def pos (self, tag):
        if tag.startswith('J'):
            return "a"
        elif tag.startswith('V'):
            return "v"
        elif tag.startswith('N'):
            return "n"
        elif tag.startswith('R'):
            return "r"
        else:
            return "n"

    def eat(self):
        pass


        