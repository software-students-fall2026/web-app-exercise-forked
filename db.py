import pymongo
import datetime
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()
MONGO_DBNAME = os.getenv('MONGO_DBNAME')
MONGO_URI = os.getenv('MONGO_URI')

connection = pymongo.MongoClient(MONGO_URI)
db = connection[MONGO_DBNAME]