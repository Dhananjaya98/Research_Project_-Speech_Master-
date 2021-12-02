# Imports
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv1D, GlobalAveragePooling1D, MaxPooling1D
from keras.models import load_model
import get_features
from sklearn.preprocessing import LabelEncoder
import numpy as np
import os
from sklearn.metrics import classification_report


def create_mlp(num_labels):

    model = Sequential()
    model.add(Dense(256,input_shape = (40,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Dense(256,input_shape = (40,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Dense(num_labels))
    model.add(Activation('softmax'))
    return model


def create_cnn(num_labels):

    model = Sequential()
    model.add(Conv1D(64, 3, activation='relu', input_shape=(40, 1)))
    model.add(Conv1D(64, 3, activation='relu'))
    model.add(MaxPooling1D(3))
    model.add(Conv1D(128, 3, activation='relu'))
    model.add(Conv1D(128, 3, activation='relu'))
    model.add(GlobalAveragePooling1D())
    model.add(Dropout(0.5))
    model.add(Dense(num_labels))
    model.add(Activation('softmax'))
    return model


def train(model,X_train, X_test, y_train, y_test,model_file):
    # compile the model 
    model.compile(loss = 'categorical_crossentropy',metrics=['accuracy'],optimizer='adam')

    print(model.summary())

    print("training for 100 epochs with batch size 32")
   
    model.fit(X_train,y_train,batch_size= 10, epochs = 100, validation_data=(X_test,y_test))
    
    # save model to disk
    print("Saving model to disk")
    model.save(model_file)

    y_pred = model.predict_classes(X_test, batch_size=8, verbose=1)
    y_test = np.argmax(y_test, axis=1)
    y_pred_arg_max = []
    print("--------------->>>>>>>>>>>>>>>")
    print(y_pred)
    print(y_test)

    print(classification_report(y_test, y_pred))


def compute(X_test,y_test,model_file):
    # load model from disk
    loaded_model = load_model(model_file)
    score = loaded_model.evaluate(X_test,y_test)
    return score[0],score[1]*100


def predict(filename,le,model_file):
    model = load_model(model_file)
    prediction_feature = get_features.get_features(filename)
    if len(prediction_feature) == 0:
        return {"pred": "", "probability": str(0)}
    if model_file == "trained_mlp.h5":
        prediction_feature = np.array([prediction_feature])
    elif model_file == "trained_cnn.h5":    
        prediction_feature = np.expand_dims(np.array([prediction_feature]),axis=2)

    predicted_vector = model.predict_classes(prediction_feature)
    predicted_class = le.inverse_transform(predicted_vector)
    sub_dirs = os.listdir('data')
    sub_dirs.sort()
    print("Predicted class",sub_dirs[predicted_class[0]])
    predicted_proba_vector = model.predict_proba([prediction_feature])

    word = ""
    probability = 0
    predicted_proba = predicted_proba_vector[0]
    for i in range(len(predicted_proba)): 
        category = le.inverse_transform(np.array([i]))
        print(category[0], "\t\t : ", format(predicted_proba[i], '.32f') )
        if (predicted_proba[i] > probability):
            probability = predicted_proba[i]
            word = sub_dirs[predicted_class[0]]
            print("Selected word: ", word)

    return {"pred": word, "probability": str(probability)}
