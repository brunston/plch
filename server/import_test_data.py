"""
fsfe_import_data.py
(c) 2017 Fanalytical Solutions, LLC - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited.
maintainer: @brunston (Brunston Poon, CTO)
"""

import pandas as pd
import pymongo
import sys
import json

# useful reference github/kbroman/d3examples/mongodb_flask

# paths and names
DATA_PATH = "section_headings.csv"
DB_NAME = "plchdb"
COLLECTION_NAME = "test"

VERBOSE = True

def vmode(text):
    if VERBOSE:
        print(text)

try:
    vmode("reading data csv")
    df = pd.read_csv(DATA_PATH)
except Exception as e:
    print(e)
    sys.exit()

# connect to running mongod service
try:
    vmode("attempting to connect to the mongoDB service through pymongo")
    m_client = pymongo.MongoClient('mongodb://localhost:27017/')
    m_client.server_info() # try to connect to the server
except pymongo.errors.ServerSelectionTimeoutError as e:
    print("mongod local service not detected within timeout specification")
    sys.exit()

# connect to database and collection
vmode("connecting to the database: " + DB_NAME)
m_db = m_client[DB_NAME]
vmode("connecting to the collection: " + COLLECTION_NAME)
m_collection = m_db[COLLECTION_NAME]

vmode("dropping current info of collection")
m_collection.drop() # remove what's there right now
# Stackoverflow 20167194 https://goo.gl/DsVPoV
vmode("loading records")
records = json.loads(df.T.to_json()).values()
m_collection.insert_many(records) # https://goo.gl/mPJQqr
vmode("closing connection")

m_client.close()
