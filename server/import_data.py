import pymongo
import sys
from bson import json_util
from collections import defaultdict
from gensim import corpora, models
import topic_analysis as ta
import pdf_extractor as pdf_extractor

# paths and names
DB_NAME = "plchdb"
COLLECTION_NAME = "corpi"

VERBOSE = True
def vmode(text):
    if VERBOSE:
        print(text)

# connect to running mongod service
try:
    vmode("attempting to connect to the mongoDB service through pymongo")
    m_client = pymongo.MongoClient('mongodb://localhost:27017/')
    m_client.server_info() # try to connect to the server
except pymongo.errors.ServerSelectionTimeoutError as e:
    print("mongod local service not detected within timeout specification")
    sys.exit()

# create model and import

pdf_file = pdf_extractor.get_pdf_file_in_texts("reinforcement-an-introduction.pdf")
analyzer = ta.TopicAnalyzer(pdf_file)
corpus_to_json_list = []
for i in range(len(analyzer.pages)):
    corpus_to_json_list.append({
        "docid": analyzer.pages[i],
        "heading": analyzer.headers[i],
        "tokens": analyzer.processed_corpus[i],
        "tokens_by_wordid": [j[0] for j in analyzer.id_to_score_corpus[i]],
        "vector": analyzer.id_to_score_corpus[i]})

#print(corpus_to_json_list)
# connect to database and collection
vmode("connecting to the database: " + DB_NAME)
m_db = m_client[DB_NAME]
m_collection = m_db[COLLECTION_NAME]

vmode("dropping current info of collection")
m_collection.drop() # remove what's there right now
# Stackoverflow 20167194 https://goo.gl/DsVPoV
vmode("loading records")
records = corpus_to_json_list
m_collection.insert_many(records) # https://goo.gl/mPJQqr
vmode("closing connection")

m_client.close()

