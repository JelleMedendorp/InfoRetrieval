import os 
import json
from zipfile import ZipFile
import glob

def get_files_from_zip(file):
    with ZipFile(file) as zip:
        zip.extractall()


def convert_to_jsonl(folder):
    text_collection = {}
    for json_file in glob.iglob(folder):
        f = open(json_file)
        data = json.load(f)

        id = data['paper_id']
        text = ''
        for text_part in data['body_text']:
            text = text + text_part['text']
        text_collection[id] = text

        f.close()
        os.remove(json_file)
        
    json_object = json.dumps(text_collection, indent=4)
 
    with open("text_collection.json", "w") as outfile:
        outfile.write(json_object)
        
    os.rmdir(folder)






    