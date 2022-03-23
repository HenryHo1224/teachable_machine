import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import pathlib
import csv
import os

model = tensorflow.keras.models.load_model('../teachable machine testing/animal/model/300_sample.h5')
f = open("../worksheet/data_300.csv","w",newline='')
writer = csv.writer(f,)
with open ('../teachable machine testing/animal/model/300_sample_label.txt','r')as label:
    class_name = label.read().split('\n')
skip=0
for path in pathlib.Path("../worksheet/photo").iterdir():
    if path.is_file():
        try:
            answer = os.path.basename(path)
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            image= Image.open(path)

            size = (224,224)

            image = ImageOps.fit(image, size, Image.ANTIALIAS)
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32)/127.0)-1
            data[0] = normalized_image_array
            prediction = model.predict(data)

            index = np.argmax(prediction)

            result_name = class_name[index]
            confidence_score = prediction[0][index]

            writer.writerow([answer, result_name,str(confidence_score)])

        except Exception as e:
            skip+=1
            print(skip)
            pass
f.close()