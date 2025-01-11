import os 
os.environ["NLTK_DATA"]="data/"
from nltk.tokenize import  word_tokenize
from nltk.corpus import stopwords
from nltk import download, pos_tag
from nltk.stem import WordNetLemmatizer


class Digest:

    def __init__(self):
        
        download("stopwords", download_dir="data/") 
        download("punkt_tab", download_dir="data/")
        download("averaged_perceptron_tagger", download_dir="data/")
        download("wordnet", download_dir="data/")

        self.stopwords = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()
        
        

    def prepare(self, t):
        detalied_text = []
        text = []
        text_lemed = []
        words = word_tokenize(t)
        ns_words = [word for word in words if word.casefold() not in self.stopwords ]
        pos_ns_word = pos_tag(ns_words)
        detalied_text.append([(self.lemmatizer.lemmatize(word[0], self.pos(word[1])),word[0], word[1]) for word in pos_ns_word])
        text.append([self.lemmatizer.lemmatize(word[0]) for word in pos_ns_word])
        text_lemed.append([self.lemmatizer.lemmatize(word[0], self.pos(word[1])) for word in pos_ns_word])

        print(text)
        text = " ".join(text[0])
        text_lemed = " ".join(text_lemed[0])
        
        print(f"text is divided as such {detalied_text}")
        print(f"text lemmatized '{text}'")
        print(f"text lemmatized keeping in mind the pos '{text_lemed}'")

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