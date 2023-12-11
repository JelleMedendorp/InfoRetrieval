# import all helper definitions from helper file
from helper import*
from evaluation import*

# """ Extract all files into a folder called "comm_use_subset" """
# # get_files_from_zip('test_papers.zip')

""" From every file get a unique ID and text as json """
print("Unfolding text")
convert_to_jsonl("pdf_json")
print("Unfolding text done!")

""" Processing text """
print("Processing text")
process_text("text_collection.json")

""" Calculating average document length """ 
avgdoclen = avg_document_length('clean_text_collection.json')

""" Creating document representation Ltu """
print("Creating document representation")
create_document_representation('clean_text_collection.json',avgdoclen)

# """ Get all queries """
# print("Processing queries")
# get_queries("test_queries.xml")
# process_text("query_collection.json")

# """ Calculate term query vectors """
# print("Creating query representation")
# avgquerylen = avg_document_length('clean_query_collection.json')
# create_query_representation('clean_query_collection.json',avgquerylen)

# """ Creating result"""
# get_test_results("clean_query_collection.json", 'query_representation.json','document_representation.json')
