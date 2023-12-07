# import all helper definitions from helper file
from helper import*

# Extract all files into a folder called "comm_use_subset"
get_files_from_zip('test_papers.zip')

# From every file get a unique ID and text as json
convert_to_jsonl("test_papers")

# Processing text
process_text("text_collection.json")