import os
import librosa
import soundfile as sf
import numpy as np
import glob
import pandas as pd


def get_features(file_name):

    print(sf.available_formats())
    if file_name: 
        X, sample_rate = sf.read(file_name, dtype='float32')

    # mfcc (mel-frequency cepstrum)
    print("sample rate: ", sample_rate)
    monoX = []
    for leftX in X:
        if len(X.shape) == 2:
            monoX.append(leftX[0])
        else:
            monoX.append(leftX)
    shape = np.shape(monoX)
    padded_array = np.zeros((150000))
    padded_array[:shape[0]] = monoX
    mfccs = librosa.feature.mfcc(y=padded_array, sr=sample_rate, n_mfcc=40)
    mfccs_scaled = np.mean(mfccs.T,axis=0)
    return mfccs_scaled


def extract_features():
    # path to dataset containing 10 subdirectories of .ogg files
    sub_dirs = os.listdir('data')
    sub_dirs.sort()
    print(sub_dirs)
    features_list = []
    for label, sub_dir in enumerate(sub_dirs):  
        for file_name in glob.glob(os.path.join('data',sub_dir,"*.ogg")):
            print("Extracting file ", file_name)
            try:
                mfccs = get_features(file_name)
            except Exception as e:
                print(e)
                print("Extraction error")
                continue
            features_list.append([mfccs,label])

    features_df = pd.DataFrame(features_list,columns = ['feature','class_label'])
    print(features_df.head())    
    return features_df
