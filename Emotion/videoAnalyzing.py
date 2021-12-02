#Import useful libraries
import cv2
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras.preprocessing import image

#Load the trained model
Saved_model = tf.keras.models.load_model('emotion_lts.h5')
Saved_model.summary()

#Prediction categories
objects = ('Angry', 'Happy', 'Sad', 'Neutral')
vid = cv2.VideoCapture(0)


def emotion_analysis(emotions):
    objects = ['Angry', 'Happy', 'Sad', 'Neutral']
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, emotions, align='center', alpha=0.9)
    plt.tick_params(axis='x', which='both', pad=10, width=4, length=10)
    plt.xticks(y_pos, objects)
    plt.ylabel('percentage')
    plt.title('emotion')

#Predict facial expressions
def get_emotions(filePath):
    cap = cv2.VideoCapture(filePath)

    emotions = [] #Define emotion list

    while (cap.isOpened()):
        try:
            ret, frame = cap.read()
            frame = cv2.resize(frame, (48, 48))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            x = image.img_to_array(frame)
            x = np.expand_dims(x, axis=0)

            x /= 255

            custom = Saved_model.predict(x)
            emotion_analysis(custom[0])
            x = np.array(x, 'float32')
            x = x.reshape([48, 48]);
            m = 0.000000000000000000001
            a = custom[0]
            for i in range(0, len(a)):
                if a[i] > m:
                    m = a[i]
                    ind = i

            print('Expression Prediction:', objects[ind])
            emotions.append(objects[ind])

            if cv2.waitKey(20) & 0XFF == ord('q'):
                break
        except:
            print("Damaged frame")
            break
    return emotions

get_emotions("speech.mp4")
cv2.destroyAllWindows()
