import os 
os.environ["NLTK_DATA"]="data/"
from nltk.tokenize import  word_tokenize
from nltk.corpus import stopwords
from nltk import download, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class Digest:

    def __init__(self):
        self.download_stuff()
        self.stopwords = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()
        self.senti = SentimentIntensityAnalyzer()

    def prepare(self, t):
        text = []
        #tokenized
        w = word_tokenize(t)
        words = [word.lower() for word in w]
        #removing stopwords (need to check if it is removing important things)
        ns_words = [word for word in words if word not in self.stopwords ]
        #adding a pos 
        pos_ns_word = pos_tag(ns_words)
        #lemmatizing by both using pos and not testing which one is better
        text = [self.lemmatizer.lemmatize(word[0], self.pos(word[1])) for word in pos_ns_word]
        data = len(text)
        text = " ".join(text)
        
        label = self.sentiment(text)
        return [data, label]

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


    def sentiment(self, text):
        t = self.senti.polarity_scores(text)

        n = t['compound']
        if n <= 0.05 and n >= -0.05:
            return "Data"
        elif n < -0.05 :
            return "Virus"
        else:
            return "Vaccine" 

    def download_stuff(self):
        download('stopwords')
        download('averaged_perceptron_tagger_eng')
        download('vader_lexicon')
        download('punkt_tab')
        download('wordnet')