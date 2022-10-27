import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf

from tensorflow.keras import datasets, layers, models, utils
import matplotlib.pyplot as plt
import numpy as np
from model import MobileNetV3LiteRASPP
from tensorflow.keras.losses import categorical_crossentropy
from tensorflow.keras.optimizers import Adam, RMSprop
import tensorflow.keras as keras
import glob

gpus = tf.config.list_physical_devices('GPU')
if gpus:
  try:
    # Currently, memory growth needs to be the same across GPUs
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
    logical_gpus = tf.config.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Memory growth must be set before GPUs have been initialized
    print(e)

model = keras.models.load_model('test1-way-too-low')
class_names = ['1', '2', '3', '4', '5']


path = r'./test/*.png'
files = glob.glob(path)
#             file,class,score
predictions = []
print(files)
for image in files:
    img = tf.keras.utils.load_img(
    image, target_size=(128, 128)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    print(
        "{}: {} with a {:.2f} percent confidence."
        .format(image,class_names[np.argmax(score)], 100 * np.max(score))
        
    )