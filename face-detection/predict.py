import tensorflow as tf
from tensorflow.keras import datasets, layers, models, utils
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.losses import categorical_crossentropy
from tensorflow.keras.optimizers import Adam, RMSprop
import tensorflow.keras as keras
import cv2

font = cv2.FONT_HERSHEY_SIMPLEX

model = keras.models.load_model('./models/test1')
class_names = ['1', '2', '3', '4', '5']

def predict(image, cropped_image,index):
    image_copy = image.copy()
    img_array = cropped_image
    img_array = tf.expand_dims(img_array, 0) # Create a batch
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    cv2.putText(image_copy, "{} with a {:.2f}%".format(class_names[np.argmax(score)], 100 * np.max(score)), (10,450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(cropped_image, "{}".format(class_names[np.argmax(score)]), (0,25), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow("cropped {}".format(index), cropped_image)
    #cv2.imshow("prediction {}".format(index), image_copy)