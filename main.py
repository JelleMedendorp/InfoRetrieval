# import all helper definitions from helper file
from helper import*
from evaluation import*

""" From csv file get a unique ID and text as json """
csv_to_json("metadata.csv")

""" Processing text """
print("Processing text")
process_text("text_collection.json")

""" Calculating average document length """ 
avgdoclen = avg_document_length('clean_text_collection.json')

""" Get all queries """
print("Processing queries")
get_queries("topics-rnd1.xml")
process_text("query_collection.json")

""" Calculate term query vectors """
print("Creating query representation")
avgquerylen = avg_document_length('clean_query_collection.json')
create_query_representation('clean_query_collection.json',avgquerylen)

""" Creating document representation Ltu """
print("Creating document representation")
create_document_representation('clean_text_collection.json',avgdoclen)

""" Creating result"""
get_test_results("clean_query_collection.json", 'query_representation.json','document_representation.json')
