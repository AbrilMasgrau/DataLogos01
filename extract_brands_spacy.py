import os
import pandas as pd
import spacy
from fuzzywuzzy import process, fuzz


marca_df = pd.read_excel(r"Num-marca.xlsx")
marca_list = marca_df['Marca'].tolist()

output_folder_path = r"predicted_brands"

def find_brands(text, marca_list):
    nlp = spacy.load("model-best")

    doc = nlp(text)
    detected_brands = []

    detected_words = list(doc.ents)

    # print("text:", text)
    # print("detected:", detected_words)
    # print("\n")
    

    for word in detected_words:
        word = str(word)
        match = process.extractOne(word, marca_list)
        if match[1] >= 70:     
            detected_brands.append(match[0])

    return detected_brands

folder_path = r"predicted_text"
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        with open(os.path.join(folder_path, filename), 'r') as file:
            text = file.read().replace("\n", " ")
            detected_brands = find_brands(text, marca_list)
            output_filename = os.path.splitext(filename)[0] + '.txt'
            with open(os.path.join(output_folder_path, output_filename), 'w') as output_file:
                for brand in detected_brands:
                    output_file.write(brand + '\n')