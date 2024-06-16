import os
from fuzzywuzzy import fuzz


def read_txt(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def evaluate_image(ground_truth_file, predicted_file, threshold=80):
    #print(ground_truth_file)

    ground_truth = read_txt(ground_truth_file)
    predicted = read_txt(predicted_file)

    TP = 0
    FP = 0
    FN = 0



    for prediction in predicted:
        matched = False
        for truth in ground_truth:
            similarity_ratio = fuzz.token_sort_ratio(prediction, truth)
            if similarity_ratio >= threshold:
                TP += 1
                matched = True
                #print("TP", prediction, truth)
                break
        if not matched:
            #print("FP", prediction, truth)
            FP += 1


    FN = len(ground_truth) - TP
    #if(FN > 0):
        #print("FN", predicted, ground_truth)

    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1_score, TP, FP, FN

def evaluate_all_images(ground_truth_folder, predicted_folder):
   
    ground_truth_files = os.listdir(ground_truth_folder)
    predicted_files = os.listdir(predicted_folder)

  
    total_true_positives = 0
    total_false_positives = 0
    total_false_negatives = 0

 
    for file in ground_truth_files:
        if file in predicted_files:  

            ground_truth_file = os.path.join(ground_truth_folder, file)
            predicted_file = os.path.join(predicted_folder, file)

            precision, recall, f1_score, TP, FP, FN = evaluate_image(ground_truth_file, predicted_file)


            total_true_positives += TP
            total_false_positives += FP
            total_false_negatives += FN


    overall_precision = total_true_positives / (total_true_positives + total_false_positives) if (total_true_positives + total_false_positives) > 0 else 0
    overall_recall = total_true_positives / (total_true_positives + total_false_negatives) if (total_true_positives + total_false_negatives) > 0 else 0
    overall_f1_score = 2 * (overall_precision * overall_recall) / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0

    return overall_precision, overall_recall, overall_f1_score, total_true_positives, total_false_positives, total_false_negatives


ground_truth_folder = r'C:\Users\abril\OneDrive\Documents\Enginyeria Matemàtica en Ciència de Dades\TFG\0. Text + Object detection\labels'
predicted_folder = r'C:\Users\abril\OneDrive\Documents\Enginyeria Matemàtica en Ciència de Dades\TFG\0. Text + Object detection\output'

overall_precision, overall_recall, overall_f1_score, total_true_positives, total_false_positives, total_false_negatives = evaluate_all_images(ground_truth_folder, predicted_folder)
print("Overall Precision:", overall_precision)
print("Overall Recall:", overall_recall)
print("Overall F1 Score:", overall_f1_score)
print("Total True Positives:", total_true_positives)
print("Total False Positives:", total_false_positives)
print("Total False Negatives:", total_false_negatives)
