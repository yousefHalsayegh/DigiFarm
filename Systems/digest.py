import os 
os.environ["NLTK_DATA"]="data/"
from nltk.tokenize import  word_tokenize
from nltk.corpus import stopwords
from nltk import download, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class Digest:
    def __init__(self):
        """
        A class used to analyse the sentences used in 'feed' to identify the semantics 
        """
        self.download_stuff()
        self.stopwords = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()
        self.senti = SentimentIntensityAnalyzer()

    def prepare(self, t):
        """
        This method process the data, and strip it down to the basics to be labeled, by tokanising the words and finding the part of speech
        # Parameters
        **t**: _str_ \n
        the sentence which will be processed
        # Return
        **a**: _list_ \n
        Contains the amount of words in the text and the lable of said sentence from the sentiment analysis
        """
        text = []
        #tokenized
        w = word_tokenize(t)
        words = [word.lower() for word in w]
        #removing stopwords (need to check if it is removing important things)
        ns_words = [word for word in words if word not in self.stopwords ]
        #adding a part of speech  (Noun,Verb,Adjective, etc)
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
        """
        Identify the sentiment of the text provided by using `nltk.sentiment.vader.SentimentIntensityAnalyzer()` and translate the different output to digimon terms
        # Parameters
        **text** : _str_ \n
        The text to be processed 
        # Return 
        **label** : _str_ \n
        The label depending on the sentiment \n
        - Neutral : Data
        - Negative : Virus
        - Positive : Vaccine
        """
        t = self.senti.polarity_scores(text)

        n = t['compound']
        if n <= 0.05 and n >= -0.05:
            return "Data"
        elif n < -0.05 :
            return "Virus"
        else:
            return "Vaccine" 

    def download_stuff(self):
        """
        An initial step of the NLP which gets the model ready by donwloading the necessary bag of words
        """
        download('stopwords')
        download('averaged_perceptron_tagger_eng')
        download('vader_lexicon')
        download('punkt_tab')
        download('wordnet')