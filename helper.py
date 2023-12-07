# Importing all needed libraries
import os 
import json
from zipfile import ZipFile
import glob
import nltk
from nltk.corpus import stopwords
import string
from collections import Counter
import time
# nltk.download('stopwords')

# Progress bar
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# Extracting zipfile 
def get_files_from_zip(file):
    with ZipFile(file) as zip:
        zip.extractall()

# Getting all texts in one json file with key
def convert_to_jsonl(folder):
    true_folder = folder + "\*"
    text_collection = {}

    # itterate trough all files
    for json_file in glob.iglob(true_folder):
        f = open(json_file)
        data = json.load(f)

        id = data['paper_id']
        text = ''

        # Add all text parts to one stringS
        for text_part in data['body_text']:
            text = text + text_part['text']
        text_collection[id] = text

        # Remove old json file
        f.close()
        os.remove(json_file)
        
    json_object = json.dumps(text_collection, indent=4)
 
    # Savind data to json file
    with open("text_collection.json", "w") as outfile:
        outfile.write(json_object)

    # Remove empty folder
    os.rmdir(folder)


# Cleaning and counting text
def process_text(json_file):
    f = open(json_file)
    data = json.load(f)
    stop_words = set(stopwords.words('english') + list(string.punctuation))

    clean_text_collection = {}
    l = len(data.keys())

    # Progress bar
    printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

    # Cleaning and counting word frequenty
    for i, key in enumerate(data.keys()):
        text = data[key]
        filtered_text = [w for w in nltk.word_tokenize(text) if not w.lower() in stop_words]
        clean_text_collection[key] = Counter(filtered_text)

        # Progress bar
        printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

    # Saving data to json file
    json_object = json.dumps(clean_text_collection, indent=4)
    with open('clean_text_collection.json', 'w') as outfile:
        outfile.write(json_object)

    print("Done!")