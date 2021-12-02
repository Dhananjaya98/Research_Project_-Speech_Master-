import spacy
from scipy.io.wavfile import read

scoreForClearness = 50/100
nlp = spacy.load("en_core_web_sm")


def identify_complicated_words(text):
    doc = nlp(text)
    complicated_words = ""
    for token in doc:
        count = len(token)
        if count > 18:
            complicated_words += f"{token.text} - {count} letters: This is a too complicated word. It is better to use more simpler word."
    return {
        "message": complicated_words,
        "score": scoreForClearness
    }


def identify_complicated_sentences(text):
    doc = nlp(text)
    complicated_sentences = ""
    for sent in doc.sents:
        word_count = 0
        # print(sent.text)
        for words in sent:
            # print(words.text)
            word_count = word_count + 1
        if word_count > 43:
            # print(f'"{sent}" is a overcomplicated sentence. There are {word_count}  words in it.')
            complicated_sentences += f'"{sent}" is a overcomplicated sentence. There are {word_count}  words in it.'
        # print(word_count)
    return {
        "message": complicated_sentences,
        "score": scoreForClearness
    }


def analyze_speed(filePath):
    # Read the Audiofile
    samplerate, data = read(filePath)
    # Frame rate for the Audio
    print(samplerate)

    # Duration of the audio in seconds.
    duration = len(data)/samplerate
    print("Duration of Audio in Seconds", duration)
    print("Duration of Audio in Minutes", duration/60)
    print(len(data))

