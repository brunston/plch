"""
Flask server for PLCH
"""

from flask import Flask, abort
from bson import json_util
import pymongo
import pandas as pd
import jsonify
app = Flask(__name__)


#https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

DB_NAME = "plchdb"
COLLECTION_CORPI = "corpi"
COLLECTION_GRAPHS = "graph"
COLLECTION_TEST = "test"
TEST_FIELDS = {
    "title": True, "heading": True}

FIELDS = {
    "heading": True, "vector": True, "tokens": True, "docid": True
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
corpi = pd.DataFrame(list(m_corpi.find({}, FIELDS)))
corpi.set_index('docid')

@app.route("/")
def hello():
    return "hello world"
    # return flask.render_template("danny_html")

@app.route("/api/v0.1/corpus", methods=['GET'])
def get_corpus_list():
    # get a list of texts in a corpus
    return corpi.loc[:,['heading']].to_json()

@app.route("/api/v0.1/corpus/<string:text>/scoringvector", methods=['GET'])
def get_scoring_vector(text):
    # get the scoring vector for a given text
    return corpi.loc[int(text), ['vector']].to_json()

@app.route("/api/v0.1/corpus/<string:text>/heading", methods=['GET'])
def get_heading(text):
    return corpi.loc[int(text), ['heading']].to_json()

@app.route("/api/v0.1/corpus/<string:text>/tokens", methods=['GET'])
def get_tokens(text):
    return corpi.loc[int(text), ['tokens']].to_json()

@app.route("/api/v0.1/unstable/test", methods=['GET'])
def get_unstable_test():
    # get a list of things from the test database
    return test_json
