import flask
from flask_cors import CORS, cross_origin

import getFillterWordCount

app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True


@app.route('/countFillerWords', methods=['GET'])
@cross_origin()
def countFillerWords():
    fillterWordCount = getFillterWordCount.count_filler_words("../temp.wav")
    return fillterWordCount

app.run(port=5001)
