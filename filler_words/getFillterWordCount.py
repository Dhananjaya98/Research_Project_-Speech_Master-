import os

from pydub import AudioSegment
from pydub.silence import split_on_silence
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
import numpy as np
import get_features
import neural_network

# countPauses("../content analyzing/temp.wav")
ScoreforUserSilence = 70/100


def get_numpy_array(features_df):
    X = np.array(features_df.feature.tolist())
    y = np.array(features_df.class_label.tolist())
    # encode classification labels
    le = LabelEncoder()
    # one hot encoded labels
    yy = to_categorical(le.fit_transform(y))
    return X, yy, le

features_df = get_features.extract_features()
X, y, le = get_numpy_array(features_df)


def count_filler_words(filePath):
    filler_word_count = 0
    sound = AudioSegment.from_wav(filePath)
    chunks = split_on_silence(sound, min_silence_len=200, silence_thresh=sound.dBFS - 16, keep_silence=150)

    # Chunk Folder file Path
    chunk_folder_name = "chunks"

    # create folder to store chunks
    if not os.path.isdir(chunk_folder_name):
        os.mkdir(chunk_folder_name)

    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_file = os.path.join(chunk_folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_file, format="wav", bitrate='192k')
        prediction = neural_network.predict(chunk_file, le, "trained_cnn.h5")
        print(prediction)
        if float(prediction["probability"]) > 0.99:
            filler_word_count += 1

    print("****** How many times Filler words in their Speech *****")

    # print count of silence
    print("Filler words: ", filler_word_count)
    return {
        "message": str(filler_word_count) + " : filler word/s found",
        "score": ScoreforUserSilence
    }

# countFillerWords("../audio.wav")
