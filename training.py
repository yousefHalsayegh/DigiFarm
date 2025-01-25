from Systems.digest import Digest
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import random 

digest = Digest()

senti = SentimentIntensityAnalyzer()
while True:
    text = input("Your text is: ")

    text_nor = digest.prepare(text)
    text_lemmed = digest.prepare_lemed(text)


    print(senti.polarity_scores(text_nor))

    print(senti.polarity_scores(text_lemmed))