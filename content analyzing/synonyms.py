import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
nlp = spacy.load("en_core_web_sm")
stopwords = list(STOP_WORDS)
punctuation = punctuation + '\n'


def content_relativity(topic, speech):
    topic = nlp(topic)
    content = nlp(speech)

    total_similarity = 0

    for token1 in content:
        if token1.text.lower() not in stopwords:
            if token1.text.lower() not in punctuation:
                for token2 in topic:
                    print((token1.text, token2.text), "similarity", token1.similarity(token2))
                    total_similarity = total_similarity + token1.similarity(token2)

    print(f'Total score for the similarity: {total_similarity}')
    average_similarity = (total_similarity/len(content))*100
    print(f'Average score for the similarity between topic and content: {average_similarity}%')
    return {
        "message": str(f'Average score for the similarity between topic and content: {average_similarity}%'),
        "score": 50/100
    }
