from Systems.digest import Digest
from nltk.corpus import twitter_samples
import nltk
import random 
from nltk.probability import FreqDist
from nltk.tokenize import  word_tokenize
from nltk.classify import NaiveBayesClassifier, SklearnClassifier
import nltk.classify.util

positive = twitter_samples.strings("positive_tweets.json")
negative = twitter_samples.strings("negative_tweets.json")

texts = positive + negative
labels = ["Positive"] * len(positive) + ["Negative"] * len(negative)


combined = list(zip(texts, labels))
random.shuffle(combined)
texts, labels = zip(*combined)

digest = Digest()
cleaned = []
cleaned_lemmed = []

for text in texts :
    cleaned.append(digest.prepare(text))
    cleaned_lemmed.append(digest.prepare_lemed(text))

print("cleaned")
all_words = [word.lower() for tweet in cleaned for word in word_tokenize(tweet)]
all_words_freq = FreqDist(all_words)
word_features = list(all_words_freq.keys())

all_words_lem = [word.lower() for tweet in cleaned_lemmed for word in word_tokenize(tweet)]
all_words_freq_lem = FreqDist(all_words_lem)
word_features_lem = list(all_words_freq_lem.keys())
print("features")
def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features[format(word)] = (word in document_words)
    return features


def document_features_lemmed(document):
    document_words = set(document)
    features = {}
    for word in word_features_lem:
        features[format(word)] = (word in document_words)
    return features

# Create feature sets for training and testing
feature_sets = [(document_features(word_tokenize(tweet)), label) for (tweet, label) in zip(cleaned, labels)]
feature_sets_lem = [(document_features_lemmed(word_tokenize(tweet)), label) for (tweet, label) in zip(cleaned_lemmed, labels)]
half = len(feature_sets)//2 
print("data ready ")
training_set, testing_set = feature_sets[:half], feature_sets[half:]
training_set_lem, testing_set_lem = feature_sets_lem[:half], feature_sets_lem[half:]

print("split done")

classfier = NaiveBayesClassifier.train(training_set)
calssfier_lem = NaiveBayesClassifier.train(training_set_lem)


accuracy = nltk.classify.util.accuracy(classfier, testing_set)
print(f'Accuracy: {accuracy * 100:.2f}%')

accuracy = nltk.classify.util.accuracy(calssfier_lem, testing_set_lem)
print(f'Accuracy: {accuracy * 100:.2f}%')



while True:
    data = input("Your sentence is: ")
    print("I think the sentement is (naive): ", classfier.classify(document_features(word_tokenize(digest.prepare(data)))))
    print("I think the sentement is (naive lem): ", calssfier_lem.classify(document_features_lemmed(word_tokenize(digest.prepare_lemed(data)))))