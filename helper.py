# Importing all needed libraries
import os 
import json
from zipfile import ZipFile
import glob
import nltk
import math
import numpy as np
import string
import pandas as pd
from nltk.corpus import stopwords
from collections import Counter
from statistics import mean
from xml.etree import ElementTree as ET
from tqdm import tqdm
# nltk.download('stopwords')

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
    
    json_object = json.dumps(text_collection, indent=4)
 
    # Savind data to json file
    with open("text_collection.json", "w") as outfile:
        outfile.write(json_object)

# Cleaning and counting text
def process_text(json_file):
    f = open(json_file)
    data = json.load(f)
    stop_words = set(stopwords.words('english') + list(string.punctuation))

    clean_text_collection = {}

    # Progress bar
    pbar = tqdm(total=len(data.keys()), desc='Processing documents', unit='doc')

    # Cleaning and counting word frequenty
    for i, key in enumerate(data.keys()):
        text = data[key]
        filtered_text = [w for w in nltk.word_tokenize(text) if not w.lower() in stop_words]
        clean_text_collection[key] = Counter(filtered_text)

        # Progress bar
        pbar.update(1)


    new_file_name = "clean_" + json_file
    # Saving data to json file
    json_object = json.dumps(clean_text_collection, indent=4)
    with open(new_file_name, 'w') as outfile:
        outfile.write(json_object)

    print("Done!")

# Create a set with all unique words
def get_all_unique_words(json_file):
    f = open(json_file)
    data = json.load(f)

    unique_words = set()
    for document in data.keys():
        unique_words.update(set(data[document].keys()))
    return list(unique_words)

# Return the logarithm of a termfrequency
def log_word_freq(word, article_dict):
    return 1 + math.log(article_dict[word], 2)

# Return Average-term-frequency-based normalization
def atfbn(word, article_dict):
    term_freq = article_dict[word]
    average_term_freq = mean(list(article_dict.values()))
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
def pun(data, document, avgdoclen, slope=0.4):
    document_length = sum(data[document].values())
    return (1 - slope) + slope * (document_length / avgdoclen)

def get_queries(xml_file):
    # Parse the XML data
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract topic numbers and queries as tuples
    topic_tuples = {topic.attrib['number']: topic.find('question').text for topic in root.findall('topic')}
    
    json_object = json.dumps(topic_tuples, indent=4)
    with open("query_collection.json", "w") as outfile:
        outfile.write(json_object)

# Creating query representation lnu
def create_query_representation(json_file, avgdoclen):
    f = open(json_file)
    data = json.load(f)

    unique_words = get_all_unique_words(json_file)
    query_representation = {}

    # Calculating vector for every unique word per query
    for query in data.keys():
        output_query = {}
        for word in unique_words:
            if word in data[query].keys():
                value = (log_word_freq(word, data[query]) * 1 * pun(data, query, avgdoclen))
            else:
                value = 0
            output_query[word] = value
        query_representation[query]=output_query
    
    json_object = json.dumps(query_representation, indent=4)
    with open("query_representation.json", "w") as outfile:
        outfile.write(json_object)

# Return cosine similarity
def cosine_similarity(query_vectors, document_vectors):
    dot_product = np.dot(document_vectors, query_vectors)
    norm_query = np.linalg.norm(query_vectors)
    norm_doc = np.linalg.norm(document_vectors)

    cos_sim = dot_product / (norm_query * norm_doc)

    if np.isnan(cos_sim):
        return 0
    else:
        return cos_sim

# Score documents
def retrieving(qid, query_rep, doc_rep):
    query_vectors = list(query_rep[qid].values())
    similarities = []
    
    l = len(doc_rep.keys())
    pbar = tqdm(total=l, desc='Processing documents', unit='doc')
    for document in doc_rep.keys():
        doc_vectors = []
        for word in query_rep[qid].keys():
            doc_vectors.append(doc_rep[document][word])
        similarities.append((document , cosine_similarity(query_vectors, doc_vectors)))
        pbar.update(1)

    return sorted(similarities, key=lambda x:x[1], reverse=True)[0:1000]
        
# Create test results
def get_test_results(queries, query_rep, doc_rep):
    query_data = json.load(open(queries))
    query_rep_data = json.load(open(query_rep))
    doc_rep_data = json.load(open(doc_rep))

    with open ('results', 'w') as fp:

        for qid , q in query_data.items():
            for rank, doc_score in enumerate(retrieving(qid, q, query_rep_data, doc_rep_data)):
                rank = rank + 1
                docid = doc_score[0]
                score = doc_score[1]

                fp.write("%s Q0 %s %s %s STANDARD\n" %(str(qid),str(docid),str(rank),str(score)) )

def csv_to_json(csv_file):
    df = pd.read_csv(csv_file)
    result_dict = {row['cord_uid']:row['abstract'] for _, row in df.iterrows() if pd.notna(row['abstract'])}

    json_object = json.dumps(result_dict, indent=4)
 
    # Savind data to json file
    with open("abstract_collection.json", "w") as outfile:
        outfile.write(json_object)

def create_document_representation(json_file, avgdoclen):
    f = open(json_file)
    data = json.load(f)

    unique_words = get_all_unique_words("clean_query_collection.json")
    doc_representation = {}

    # Calculating vector for every unique word per document
    l = len(data.keys())
    pbar = tqdm(total=l, desc='Processing documents', unit='doc')
    for document in data.keys():

        output_doc = {}
        for word in unique_words:
            if word in data[document].keys():
                value = (atfbn(word, data[document]) * icf(data, word) * pun(data, document, avgdoclen))
            else:
                value = 0
            output_doc[word] = value

        doc_representation[document] = output_doc
        pbar.update(1)

    pbar.close()
    with open("document_representation.json", "w") as outfile:
        json.dump(doc_representation, outfile, indent=4)

