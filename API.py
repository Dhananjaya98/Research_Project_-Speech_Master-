import datetime
import json
import os
import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
import sys
import subprocess
import moviepy.editor

sys.path.insert(1, 'content analyzing')
sys.path.insert(1, 'Flow of the sppech')
sys.path.insert(1, 'Grammer')
sys.path.insert(1, 'Emotion')

import speechToText
import quotesIdentify
import clearness
import conclusion
import introduction
import keyWordExtraction
import synonyms
import DoubleWords
import FillerWords
import Silence
import grammar
import webScraping
import suggestContent
import videoAnalyzing
import textAnalyze

app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True

@app.route('/clearness/word', methods=['GET'])
@cross_origin()
def clearnerssWords():
    if clearness.identify_complicated_words(request.args['text']):
        return clearness.identify_complicated_words(request.args['text'])
    else:
        return "No results"

@app.route('/clearness/sentense', methods=['GET'])
@cross_origin()
def clearnerssSentence():
    if clearness.identify_complicated_sentences(request.args['text']):
        return clearness.identify_complicated_sentences(request.args['text'])
    else:
        return "No results"

@app.route('/quotes/sentense', methods=['GET'])
@cross_origin()
def quotesSentence():
    if quotesIdentify.identifyQuotes(request.args['text']):
        return json.dumps(quotesIdentify.identifyQuotes(request.args['text']))
    else:
        return "No results"

@app.route('/emotion/sentense', methods=['GET'])
@cross_origin()
def emotionSentence():
    if textAnalyze.text_analyze(request.args['text']):
        return json.dumps(textAnalyze.text_analyze(request.args['text']))
    else:
        return "No results"

@app.route('/conclusion', methods=['GET'])
@cross_origin()
def conclusions():
    if conclusion.identify_conclusion(request.args['text']):
        return conclusion.identify_conclusion(request.args['text'])
    else:
        return "No results"

@app.route('/conclusion/comments', methods=['GET'])
@cross_origin()
def comments():
    if len(conclusion.conclusion_best_practices(request.args['text'])) > 0:
        return json.dumps(conclusion.conclusion_best_practices(request.args['text']))
    else:
        return "No results"

@app.route('/conclusion/questions', methods=['GET'])
@cross_origin()
def questions():
    if conclusion.conclusion_questions(request.args['text']):
        return json.dumps(conclusion.conclusion_questions(request.args['text']))
    else:
        return "No results"

@app.route('/introduction', methods=['GET'])
@cross_origin()
def introductionFunc():
    if introduction.identify_introduction(request.args['text']):
        return introduction.identify_introduction(request.args['text'])
    else:
        return "No results"

@app.route('/introduction/bestUses', methods=['GET'])
@cross_origin()
def introductionBestUsesFunc():
    if introduction.introduction_best_practices(request.args['text']):
        return introduction.introduction_best_practices(request.args['text'])
    else:
        return "No results"

@app.route('/introduction/questions', methods=['GET'])
@cross_origin()
def introductionQuestions():
    if len(introduction.introduction_questions(request.args['text'])) > 0:
        return json.dumps(introduction.introduction_questions(request.args['text']))
    else:
        return "No results"

@app.route('/keywordExtraction', methods=['GET'])
@cross_origin()
def keywordExtraction():
    print(keyWordExtraction.key_word_extraction(request.args['topic'], request.args['speech']))
    if len(keyWordExtraction.key_word_extraction(request.args['topic'], request.args['speech'])) > 0:
        return json.dumps(keyWordExtraction.key_word_extraction(request.args['topic'], request.args['speech']))
    else:
        return "No results"

@app.route('/synonyms', methods=['GET'])
@cross_origin()
def synonymsFunction():
    if synonyms.content_relativity(request.args['topic'], request.args['speech']):
        return synonyms.content_relativity(request.args['topic'], request.args['speech'])
    else:
        return "No results"

@app.route('/doubleWords', methods=['GET'])
@cross_origin()
def doubleWordsFunc():
    if len(DoubleWords.identify_repeated_words(request.args['text'])) > 0:
        return json.dumps(DoubleWords.identify_repeated_words(request.args['text']))
    else:
        return "No results"

@app.route('/fillerWords', methods=['GET'])
@cross_origin()
def fillerWordsFunc():
    if FillerWords.wordcount(request.args['text'], ["Like","okay" ,"so", "actually" ,"basically","right"]):
        return FillerWords.wordcount(request.args['text'], ["Like","okay" ,"so", "actually" ,"basically","right"])
    else:
        return "No results"

@app.route('/countPauses', methods=['GET'])
@cross_origin()
def countPauses():
    if Silence.count_silences("temp.wav"):
        return Silence.count_silences("temp.wav")
    else:
        return "No results"

@app.route('/grammar', methods=['GET'])
@cross_origin()
def grammarFunc():
    if len(grammar.processGrammar(request.args['text'])) > 0:
        return json.dumps(grammar.processGrammar(request.args['text']))
    else:
        return "No results"

@app.route('/gingerItParse', methods=['GET'])
@cross_origin()
def gingerItParse():
    if grammar.gingerItParse(request.args['text']):
        return grammar.gingerItParse(request.args['text'])
    else:
        return "No results"

@app.route('/webScrapping', methods=['GET'])
@cross_origin()
def webScrapping():
    webScraping.suggest_youtube_content()
    return "Success"

@app.route('/suggestContent', methods=['GET'])
@cross_origin()
def suggestContent():
    suggestContent.suggestContent()
    return "Success"


@app.route('/audioUpload', methods=['GET', 'POST'])
@cross_origin()
def uploader():
    print(os.getcwd())
    if request.method == 'POST':
        f = request.files['file']
        print(request.headers.get('lat'))
        splits = f.filename.split("/")
        print(splits[len(splits)-1])
        # os.remove(os.path.join(uploadPath, "temp.mp4"))
        f.save(os.path.join("temp.wav"))
        return speechToText.get_large_audio_transcription("temp.wav")


@app.route('/videoUpload', methods=['GET', 'POST'])
@cross_origin()
def videoUploader():
    print(os.getcwd())
    if request.method == 'POST':
        f = request.files['file']
        print(request.headers.get('lat'))
        splits = f.filename.split("/")
        print(splits[len(splits)-1])
        # os.remove(os.path.join(uploadPath, "temp.mp4"))
        f.save(os.path.join("temp.mp4"))
        # command = "ffmpeg -i C:/Users/ADMIN/Downloads/Compressed/2021-060/speechVideo/speech.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.wav"
        # subprocess.call(command, shell=True)

        video = moviepy.editor.VideoFileClip(os.path.join("temp.mp4"))
        audio = video.audio
        audio.write_audiofile("temp.wav")

        audioResult = speechToText.get_large_audio_transcription("temp.wav")

        videoResult = json.dumps(videoAnalyzing.get_emotions("temp.mp4"))
        return {
            "videoResult": videoResult,
            "audioResult": audioResult
        }

app.run()
