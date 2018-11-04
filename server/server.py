"""
Flask server for PLCH
"""

from flask import Flask
import pymongo
import pandas as pd
import jsonify
app = Flask(__name__)


#https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

DB_NAME = "plchdb"
COLLECTION_TEXTBOOKS = "textbook"
COLLECTION_GRAPHS = "graph"
COLLECTION_TEST = "test"
FIELDS = {
    "title": True, "heading": True}

try:
    m_client = pymongo.MongoClient('mongodb://localhost:27017')
    m_client.server_info()
except pymongo.errors.ServerSelectionTimeoutError as e:
    print("mongod local service not detected")
    sys.exit()

m_db = m_client[DB_NAME]
m_collection = m_db[COLLECTION_TEST]
df = pd.DataFrame(list(m_collection.find({}, FIELDS)))
del df['_id']
print(df.T)
json = df.to_json()
print(json)

@app.route("/")
def hello():
    return "hello world"
    # return flask.render_template("danny_html")

@app.route("/api/0.1/textbooks", methods=['GET'])
def get_textbook_list():
    # get textbooks from mongodb
    #return jsonify(textbookthing)
    pass

@app.route("/api/0.1/graphs", methods=['GET'])
def get_graph_list():
    # get a list of graphs from mongodb
    pass

@app.route("/api/0.1/unstable/test", methods=['GET'])
def get_unstable_test():
    # get a list of things from the test database
    return json
