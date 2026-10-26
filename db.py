import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_DBNAME = os.getenv('MONGO_DBNAME')
MONGO_URI = os.getenv('MONGO_URI')

connection = pymongo.MongoClient(MONGO_URI)
db = connection[MONGO_DBNAME]