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
import math
import numpy
from statistics import mean
from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET
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
        # os.remove(json_file)
        
    json_object = json.dumps(text_collection, indent=4)
 
    # Savind data to json file
    with open("text_collection.json", "w") as outfile:
        outfile.write(json_object)

    # Remove empty folder
    # os.rmdir(folder)


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

# Create a set with all unique words
def get_all_unique_words(json_file):
    f = open(json_file)
    data = json.load(f)

    unique_words = set()
    for document in data.keys():
        unique_words.update(set(data[document].keys()))
    return unique_words

# Return the logarithm of a termfrequency
def log_word_freq(word, article_dict):
    return 1 + math.log(article_dict[word], 2)

# Return Average-term-frequency-based normalization
def atfbn(word, article_dict):
    term_freq = article_dict[word]
    total_terms = sum(list(article_dict.values()))
    average_term_freq = term_freq / total_terms
    return ((1 + math.log(term_freq, 2)) / (1 + math.log(average_term_freq,2)))

# Return the amount of times a document contains a certain term
def count_term_num_docs(data, word):
    count = 0
    for document in data.keys():
        if word in data[document].keys():
            count += 1
    return count

# Return Inverse collection frequency
def icf(data, word):
    total_num_doc = len(data.keys())
    term_num_docs = count_term_num_docs(data, word) 
    return math.log(((total_num_doc + 1) / term_num_docs),2)

# Return the average document length
def avg_document_length(json_file):
    f = open(json_file)
    data = json.load(f)
    return mean([sum(data[document].values()) for document in data.keys()])

# Return Pivoted unique normalization
def pun(data, document, avgdoclen, slope=0.2):
    document_length = sum(data[document].values())
    return (1 - slope) + slope * (document_length / avgdoclen)

# Creating document representation Ltu
def create_document_representation(json_file, avgdoclen):
    f = open(json_file)
    data = json.load(f)

    unique_words = get_all_unique_words(json_file)
    doc_representation = []
    for document in data.keys():
        output_doc = []
        for word in unique_words:
            if word in data[document].keys():
                value = (atfbn(word, data[document]) * icf(data, word) * pun(data, document, avgdoclen))
            else:
                value = 0
            output_doc.append(value)
        doc_representation.append(output_doc)
    return doc_representation

def get_queries(xml_file):
    # Parse the XML data
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract topic numbers and queries as tuples
    topic_tuples = [(topic.attrib['number'], topic.find('query').text) for topic in root.findall('topic')]

    # Print the result
    print(topic_tuples)