from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URL)
db = client[settings.MONGO_DB_NAME]
coll = db[settings.MONGO_COLLECTION]

# Insert test
coll.insert_one({"test": "hello"})
coll.find_one()