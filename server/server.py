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

m_corpi = m_db[COLLECTION_CORPI]
l_corpi = list(m_corpi.find({}, FIELDS))
corpi = pd.DataFrame(l_corpi)

@app.route("/")
def hello():
    return "hello world"

@app.route("/api/v0.1/corpus", methods=['GET'])
def get_corpus_list():
    # get a list of texts in a corpus
    return jsonify([i[0] for i in corpi.loc[:,['docid']].values.tolist()])

@app.route("/api/v0.1/corpus/text/<int:text>/vector", methods=['GET'])
def get_scoring_vector(text):
    # get the scoring vector for a given text
    return jsonify(list(corpi.loc[text, ['vector']]))

@app.route("/api/v0.1/corpus/text/<int:text>/tokens_by_wordid", methods=['GET'])
def get_scoring_vector_by_wordid(text):
    return jsonify(list(corpi.loc[text, ['tokens_by_wordid']]))

@app.route("/api/v0.1/corpus/text/<int:text>/heading", methods=['GET'])
def get_heading(text):
    return jsonify(list(corpi.loc[text, ['heading']]))

@app.route("/api/v0.1/corpus/text/<int:text>/tokens", methods=['GET'])
def get_tokens(text):
    return jsonify(list(corpi.loc[text, ['tokens']]))

@app.route("/api/v0.1/corpus/search/text/<int:text>/find_related/spatial/<int:n>/quantity/<int:qty>", methods=['GET'])
def get_related_texts(text, n, qty):

    index_of_text = corpi[corpi['docid'].isin([text])].iloc[0].name
    lower = max(min(corpi['docid']), index_of_text - n)
    upper = min(max(corpi['docid']), index_of_text + n)
    return jsonify(list(corpi[lower:upper].loc[:, ['docid']].T))

@app.route("/api/v0.1/corpus/search/word/<int:wordid>/find_texts", methods=['GET'])
def get_texts_with_word(wordid):
    return jsonify([text['docid'] for text in l_corpi if wordid in text['tokens_by_wordid']])

