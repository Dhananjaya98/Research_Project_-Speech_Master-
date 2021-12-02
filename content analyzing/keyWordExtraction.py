import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import string
nlp = spacy.load('en_core_web_sm')


def key_word_extraction(topic, speech):
    topic = nlp(topic)
    content = nlp(speech)
    stopwords = list(STOP_WORDS)
    topic_words = []
    key_words = []

    punctuation = string.punctuation + '\n'

    word_frequencies = {}
    for word in content:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    for words in topic:
        topic_words.append(words.text)

    for word in word_frequencies.keys():
        if word_frequencies[word] >= 3:
            key_words.append(word)
            print(word)

    return {
        "message": key_words,
        "score": 50/100
    }

