import spacy
# In here we are importing stop words from spacy. there are already spefied stop words there in the spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

ScoreforRepetedwords = 70/100

stopwords = list(STOP_WORDS)
# print(stopwords)
nlp = spacy.load('en_core_web_sm')


def identify_repeated_words(speech):
    repeated_words = []
    doc = nlp(speech)
    # Tokenization
    tokens = [token.text for token in doc]
    print("***** Analyze Repeated Words in you're Speech *****")
    for i in range(len(tokens)-1):
        if tokens[i] == tokens[i + 1]:
            print(f" You stuck in this word :{tokens[i]}")
            repeated_words.append(f" You stuck in this word :{tokens[i]}")
    return {
        "message": repeated_words,
        "score": ScoreforRepetedwords
    }

