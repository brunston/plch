"""
Flask server for PLCH
"""

from flask import Flask, abort, jsonify
from bson import json_util
import pymongo
import pandas as pd
app = Flask(__name__)


#https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

DB_NAME = "plchdb"
COLLECTION_CORPI = "corpi"
COLLECTION_GRAPHS = "graph"
COLLECTION_TEST = "test"
TEST_FIELDS = {
    "title": True, "heading": True}

FIELDS = {
    "heading": True, "vector": True, "tokens": True, "docid": True,
    "tokens_by_wordid": True
    }

try:
    m_client = pymongo.MongoClient('mongodb://localhost:27017')
    m_client.server_info()
except pymongo.errors.ServerSelectionTimeoutError as e:
    print("mongod local service not detected")
    sys.exit()

m_db = m_client[DB_NAME]

m_collection = m_db[COLLECTION_TEST]
test_df = pd.DataFrame(list(m_collection.find({}, TEST_FIELDS)))
del test_df['_id']
test_json = test_df.to_json()

m_corpi = m_db[COLLECTION_CORPI]
l_corpi = list(m_corpi.find({}, FIELDS))
corpi = pd.DataFrame(l_corpi)
corpi.set_index('docid')
print(l_corpi)

@app.route("/")
def hello():
    return "hello world"

@app.route("/api/v0.1/corpus", methods=['GET'])
def get_corpus_list():
    # get a list of texts in a corpus
    return corpi.loc[:,['heading']].to_json()

@app.route("/api/v0.1/corpus/<string:text>/vector", methods=['GET'])
def get_scoring_vector(text):
    # get the scoring vector for a given text
    return jsonify(list(corpi.loc[int(text), ['vector']]))

@app.route("/api/v0.1/corpus/<string:text>/tokens_by_wordid", methods=['GET'])
def get_scoring_vector_by_wordid(text):
    return jsonify(list(corpi.loc[int(text), ['tokens_by_wordid']))

@app.route("/api/v0.1/corpus/<string:text>/heading", methods=['GET'])
def get_heading(text):
    return jsonify(list(corpi.loc[int(text), ['heading']]))

@app.route("/api/v0.1/corpus/<string:text>/tokens", methods=['GET'])
def get_tokens(text):
    return jsonify(list(corpi.loc[int(text), ['tokens']]))


@app.route("/api/v0.1/corpus/word/<int:wordid>/find_texts", methods=['GET'])
def get_texts_with_word(wordid):
    return jsonify([text['docid'] for text in l_corpi if wordid in text['tokens_by_wordid']])

@app.route("/api/v0.1/unstable/test", methods=['GET'])
def get_unstable_test():
    # get a list of things from the test database
    return test_json
