#Import useful libraries
import string
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def text_analyze(speech):
    text = speech

    #convert text to lower case
    lower_case = text.lower()
    cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

    # Using word_tokenize because it's faster than split()
    tokenized_words = word_tokenize(cleaned_text, "english")

    # Removing Stop Words
    final_words = []
    for word in tokenized_words:
        if word not in stopwords.words('english'):
            final_words.append(word)

    #Lemmatization (convert base or dictionary form of a word)
    lemma_words = []
    for word in final_words:
        word = WordNetLemmatizer().lemmatize(word)
        lemma_words.append(word)

    #Defind emotion list
    emotion_list = []

    #Looping final words and identify emotional words
    for i in final_words:
        with open('Emotion/emotions.txt', 'r') as file:#Emotions dictionary
            for line in file:
                #Remove dictionary punctuations
                clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
                word, emotion = clear_line.split(':')
                if i in word:
                    final_emotion = emotion.replace("", '').strip()
                    def sentiment_analyse(sentiment_text): #Measure sentiment and verify the emotions
                        score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
                        if score['neg'] > score['pos']:
                            emotion_list.append(final_emotion)
                        elif score['neg'] < score['pos']:
                            emotion_list.append(final_emotion)
                        else:
                            emotion_list.append(final_emotion)
                    sentiment_analyse(word)

#Return the final emotions
    return {
        "message": emotion_list
    }
