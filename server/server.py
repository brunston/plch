"""
Flask server for PLCH
"""

from flask import Flask, abort, jsonify
from flask_cors import CORS, cross_origin
from bson import json_util
import pymongo
import pandas as pd
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


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
#print(corpi.iloc[0]['vector'])

@app.route("/")
def hello():
    return "hello world"

@app.route("/api/v0.1/corpus", methods=['GET', 'OPTIONS'])
@cross_origin()
#@cross_origin(origin='localhost', headers=['Content-Type','Authorization'])
def get_corpus_list():
    # get a list of texts in a corpus
    return jsonify([i[0] for i in corpi.loc[:,['docid']].values.tolist()])

@app.route("/api/v0.1/corpus/text/<int:text>/vector", methods=['GET', 'OPTIONS'])
@cross_origin()
def get_scoring_vector(text):
    # get the scoring vector for a given text
    return jsonify(list(corpi.loc[text, ['vector']]))

@app.route("/api/v0.1/corpus/text/<int:text>/heading", methods=['GET', 'OPTIONS'])
@cross_origin()
def get_heading(text):
    # get the section heading for this particular piece of text
    return jsonify(list(corpi.loc[text, ['heading']]))

@app.route("/api/v0.1/corpus/text/<int:text>/tokens", methods=['GET', 'OPTIONS'])
@cross_origin()
def get_tokens(text):
    # get all the words in the text that are kept by the data pipeline
    return jsonify(list(corpi.loc[text, ['tokens']]))

@app.route("/api/v0.1/corpus/text/<int:text>/tokens_by_wordid", methods=['GET', 'OPTIONS'])
@cross_origin()
def get_scoring_vector_by_wordid(text):
    # get all the words (by wordid) in the text kept by the data pipeline
    return jsonify(list(corpi.loc[text, ['tokens_by_wordid']]))

@app.route("/api/v0.1/corpus/search/text/<int:text>/find_related/spatial/<int:n>/quantity/<int:qty>", methods=['GET', 'OPTIONS'])
@cross_origin()
def get_related_texts(text, n, qty):
    # get related texts by a combination of configurable spatial locality
    # and sorting by largest dot product
    index_of_text = corpi[corpi['docid'].isin([text])].iloc[0].name
    index_vector_intermediate = corpi.iloc[0]['vector']
    index_vector = index_vector_intermediate #index_vector = [lst[ for lst in index_vector_intermediate]
    #print(index_vector)
    lower = max(min(corpi['docid']), index_of_text - n)
    upper = min(max(corpi['docid']), index_of_text + n)
    return jsonify(list(corpi[lower:upper].loc[:, ['docid']].T))
    """
    list_of_candidate_vectors = [corpi.iloc[i]['vector'] for i in range(lower, upper + 1)]
    list_of_dot_products = [_dot(index_vector, candidate) for candidate in list_of_candidate_vectors]
    zipped_dots = zip(range(lower, upper+1, 1), list_of_dot_products)
    zipped_dots.sort(key=lambda x: x[1])
    if qty <= len(zipped_dots):
        return jsonify([corpi.iloc[i[0]]['docid'] for i in zipped_dots[:qty]])
    else:
        return jsonify([corpi.iloc[i[0]]['docid'] for i in zipped_dots])
    """

def _dot(v1, v2):
    sum = 0
    v2_words = [i[0] for i in v2]
    for i in range(len(v1)):
        for j in range(len(v2)):
            if v1[i][0] in v2_words:
                sum += v1[i][0] * v2[i][0]


@app.route("/api/v0.1/corpus/search/word/<int:wordid>/find_texts", methods=['GET', 'OPTIONS'])
@cross_origin()
def get_texts_with_word(wordid):
    # search for other texts that contain a specific wordid
    return jsonify([text['docid'] for text in l_corpi if wordid in text['tokens_by_wordid']])

