# import all helper definitions from helper file
from helper import*

# get_text(r"test_texts\00acd3fd31ed0cde8df286697caefc5298e54df1.json")

# # Extract all files into a folder called "comm_use_subset"
# get_files_from_zip('trecc_texts.zip')

# From every file get a unique ID and text as json
convert_to_jsonl("comm_use_subset\*")