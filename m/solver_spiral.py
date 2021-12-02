from tensorflow import keras
from keras.models import load_model
import numpy as np
import os

def load(filename):
    image_size = (100,100)
    image = keras.preprocessing.image.load_img(filename,target_size=image_size)
    input_arr = keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])
    return input_arr

def solver(image_path):
    # load model
    model = load_model('./m/spiral_model.h5')
    # get file path
    file_names = []
    for _,_,filenames in os.walk(image_path):
        file_names.extend(filenames)
        break
    # predict image
    result_dict = dict()
    for name in file_names:
        img = load(image_path + name)
        result = model.predict(img)[0][0]
        result_dict[name] = result
    # get image have the biggest predicted value
    value_max = -1
    name_max = ''
    for k in result_dict.keys():
        if value_max < result_dict[k]:
            value_max = result_dict[k]
            name_max = k
    return int(name_max[-5])
