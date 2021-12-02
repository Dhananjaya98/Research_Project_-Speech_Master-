import spacy


def identifyQuotes(text):
    nlp = spacy.load("content analyzing/quotesIdentify")
    doc = nlp(text)

    for sent in doc.sents:
        sentence = nlp(sent.text)
        return sentence.cats


