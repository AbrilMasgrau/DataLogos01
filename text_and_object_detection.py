from paddleocr import PaddleOCR, draw_ocr
from matplotlib import pyplot as plt
import cv2 
import os
import spacy
from fuzzywuzzy import process, fuzz
import pandas as pd
from ultralytics import YOLO
from PIL import Image
import json
import collections as ct

def find_brands(text, marca_list):
    nlp = spacy.load("model-best")

    doc = nlp(text)
    detected_brands = []

    detected_words = list(doc.ents)  

    for word in detected_words:
        word = str(word)
        match = process.extractOne(word, marca_list)
        #ratio = fuzz.ratio(match, word)
        if match[1] >= 70:     
            detected_brands.append(match[0])
        #print(text, detected_words, word, match)

    return detected_brands


nlp = spacy.load("es_core_news_sm")

folder_path = r"images"
output_folder = r"output"
output_folder_text = r"output_text"
output_folder_object = r"output_object"

marca_df = pd.read_excel(r"Num-marca.xlsx")
marca_list = marca_df['Marca'].tolist()


ocr_model = PaddleOCR(lang='en')

yolo_model = YOLO('best.pt')


for filename in os.listdir(folder_path):
    if filename.endswith('.JPG') or filename.endswith('.jpg') or filename.endswith('.png'):

        detected_brands_object = []
        detected_brands_text = []
        
        img_path = os.path.join(folder_path, filename)

        result_text = ocr_model.ocr(img_path)[0]


        result_object = yolo_model(img_path)

        # Text recognition
        if result_text and isinstance(result_text, list) and result_text[0]:
            texts_paddle = [res[1][0] for res in result_text]

            for text in texts_paddle:
                detected_ = find_brands(text, marca_list)
                detected_brands_text.extend(detected_)
            #print("Text results:", detected_brands_text)


        #Object detection
        for i, r in enumerate(result_object):
            brands = json.loads(r.tojson(normalize=False))
            names = [brand["name"] for brand in brands]
            detected_brands_objects = names

        print("Text:", detected_brands_text)
        text_count = ct.Counter(detected_brands_text)

        print("Object:", detected_brands_objects)
        object_count = ct.Counter(detected_brands_objects)

        total_img = (text_count - object_count) + (object_count - text_count) + (text_count & object_count)

        result_list = []

        for key, value in total_img.items():
            result_list.extend([key] * value)

        print(result_list)
        output_filename = os.path.splitext(filename)[0] + '.txt'
        with open(os.path.join(output_folder, output_filename), 'w') as output_file:
            for brand in result_list:
                output_file.write(brand + '\n')

        output_filename = os.path.splitext(filename)[0] + '.txt'
        with open(os.path.join(output_folder_text, output_filename), 'w') as output_file:
            for brand in detected_brands_text:
                output_file.write(brand + '\n')


        output_filename = os.path.splitext(filename)[0] + '.txt'
        with open(os.path.join(output_folder_object, output_filename), 'w') as output_file:
            for brand in detected_brands_objects:
                output_file.write(brand + '\n')
