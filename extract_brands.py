import os
import pandas as pd
from fuzzywuzzy import process, fuzz

marca_df = pd.read_excel(r"Num-marca.xlsx")
marca_list = marca_df['Marca'].tolist()
output_folder_path = r"predicted_brands"

def find_brands(text, marca_list):
    detected_brands = []
    lines = text.split('\n')
    for line in lines:
        line = line.lower()
        words = line.split()
        for word in words:
            match = process.extractOne(word, marca_list)
            ratio = fuzz.ratio(match, word)
            if match[1] >= 80 and ratio > 30:      #PaddleOCR i EasyOCR > 25, Tesserract > 30
                detected_brands.append(match[0])
                print(word, match, ratio)

    return detected_brands

folder_path = r'predicted_text'
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        with open(os.path.join(folder_path, filename), 'r') as file:
            text = file.read()
            detected_brands = find_brands(text, marca_list)
            output_filename = os.path.splitext(filename)[0] + '.txt'
            with open(os.path.join(output_folder_path, output_filename), 'w') as output_file:
                for brand in detected_brands:
                    output_file.write(brand + '\n')
