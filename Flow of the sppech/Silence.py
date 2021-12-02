import os

from pydub import AudioSegment
from pydub.silence import split_on_silence

# countPauses("../content analyzing/temp.wav")
ScoreforUserSilence = 70/100


def count_silences(filePath):
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

    print("****** How many times User Silence in their Speech *****")

    # print count of silence
    print(str(len(chunks) - 1) + " : Silence/s found")
    return {
        "message": str(len(chunks) - 1) + " : Silence/s found",
        "score": ScoreforUserSilence
    }

