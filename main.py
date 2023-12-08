# import all helper definitions from helper file
from helper import*

""" Extract all files into a folder called "comm_use_subset" """
# get_files_from_zip('test_papers.zip')

""" From every file get a unique ID and text as json """
convert_to_jsonl("test_papers")

""" Processing text """
process_text("text_collection.json")

""" Calculating average document length """
avgdoclen = avg_document_length('clean_text_collection.json')

""" creating document representation Ltu """
create_document_representation('clean_text_collection.json',avgdoclen)

""" get all queries """
get_queries("test_queries.xml")
process_text("query_collection.json")

""" Calculate term query vectors """
avgquerylen = avg_document_length('clean_query_collection.json')
create_query_representation('clean_query_collection.json',avgquerylen)

""" retrieving best documents """
print(retrieving('1', 'query_representation.json','document_representation.json'))
print(retrieving('2', 'query_representation.json','document_representation.json'))
print(retrieving('3', 'query_representation.json','document_representation.json'))