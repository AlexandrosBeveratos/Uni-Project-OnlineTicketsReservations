#Database
import pymongo

def get_db():
  client = pymongo.MongoClient(host='dsairline_mongodb', 
                              port=27017,
                              username='root',
                              password='pass',
                              authSource='admin')
  db = client['ds_airline_db']
  return db

db = get_db()