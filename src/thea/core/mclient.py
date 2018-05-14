from pymongo import MongoClient
from bson.objectid import ObjectId

import os
server_host = '192.168.1.119' if os.environ['thea_server'] is None else os.environ['thea_server']
MONGO_HOST = '{}:27017'.format(server_host)
# creating connections for communicating with Mongo DB
print('Connecting to MongoDB at {}'.format(MONGO_HOST))
client = MongoClient(MONGO_HOST)
print('Connected to MongoDB')

db = client.MnetPioneer

# Function to insert data into mongo db
def insert(cparams):
    try:
        resp = db.mnet.insert_one(cparams)
        #print('\n[MONGO_CLIENT] Inserted data successfully\n')
        return False, resp
    except Exception as e:
        print(str(e))
        return True, str(e)


# Function to update record to mongo db
def update(cparams):
    try:
        nid = cparams['nid']
        del cparams['nid']
        db.mnet.update_one(
            {"_id": ObjectId(nid)},
            {
                "$set": cparams
            }
        )
        #print("\nRecords updated successfully\n")
        return False, None
    except Exception as e:
        print(str(e))
        return True, str(e)


# function to read records from mongo db
def read(cparams):
    try:
        if cparams is not None and 'nid' in cparams:
            id = cparams['nid']
            del cparams['nid']
            cparams['_id'] = ObjectId(id)

        rlist = []
        recs = db.mnet.find(cparams)
        for rec in recs:
            rlist.append(rec)
        return False, rlist
    except Exception as e:
        print(str(e))
        return True, str(e)


# Function to delete record from mongo db
def delete_one(cparams):
    try:
        resp = db.mnet.delete_one({"_id": ObjectId(cparams['nid'])})
        #print('\nDeletion successful\n')
        return False, resp
    except Exception as e:
        print(str(e))
        return True, str(e)


# Function to delete record from mongo db
def delete_all():
    try:
        db.mnet.remove({})
        #print('\nDeletion successful\n')
        return False, None
    except Exception as e:
        print(str(e))
        return True, str(e)