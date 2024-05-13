from keras.models import model_from_json
import numpy as np
from keras.preprocessing import image
import cv2
from time import sleep

import serial
ser = serial.Serial("COM3", baudrate = '9600',timeout = 0.5)

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("model.h5")
print("Loaded model from disk")

def classify(img_file):
    img_name = img_file
    test_image = image.load_img(img_name, target_size = (512,512))

    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = model.predict(test_image)

    if result[0][0] == 0:
        prediction = 'CORN_AFFECTED'
        img = cv2.imread(img_name)
        cv2.imshow("CORN_AFFECTED",img)
        print(prediction)
        url = 'https://www.bighaat.com/collections/crop-protection'
        text = 'SEED AFFECTED'
        msg = f"Lime or sulfur can be added to adjust the soil pH to the optimal range for maize cultivation."
        ser.write(text.encode())
        sleep(15)
        ser.write(url.encode())
        sleep(15)
        ser.write(msg.encode())
        
    else:
        prediction = 'CORN_NORMAL'
        img = cv2.imread(img_name)
        cv2.imshow("CORN_NORMAL",img)
        print(prediction)
        msg2 = "Seed is Normal"
        ser.write(msg2.encode())
import os
path = 'data/test'
files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
   for file in f:
     if '.jpg' in file:
       files.append(os.path.join(r, file))

for f in files:
   classify(f)
   print('\n')
