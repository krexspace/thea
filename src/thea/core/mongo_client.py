from pymongo import MongoClient
from bson.objectid import ObjectId
import thea.core.utils as ut

import os
server_host = '192.168.1.119' if os.environ['thea_server'] is None else os.environ['thea_server']
MONGO_HOST = '{}:27017'.format(server_host)
# creating connections for communicating with Mongo DB
ut.log('Connecting to MongoDB at {}'.format(MONGO_HOST))
client = MongoClient(MONGO_HOST)
ut.log('Connected to MongoDB')

db = client.MnetPioneer

# Function to insert data into mongo db
def insert(cparams):
    try:
        resp = db.mnet.insert_one(cparams)
        #ut.log('\n[MONGO_CLIENT] Inserted data successfully\n')
        return False, resp
    except Exception as e:
        ut.log(str(e))
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
        #ut.log("\nRecords updated successfully\n")
        return False, None
    except Exception as e:
        ut.log(str(e))
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
        ut.log(str(e))
        return True, str(e)

# function to read mutiple records by id
def read_multi_by_nid(cparams):
    try:
        obj_id_list = []
        for nid in cparams:
            obj_id_list.append(ObjectId(nid))

        rlist = []
        recs = db.mnet.find(
            { "_id": {
                    "$in" : obj_id_list
                }
            }
        )
        for rec in recs:
            rlist.append(rec)
        return False, rlist
    except Exception as e:
        ut.log(str(e))
        return True, str(e)


# Function to delete record from mongo db
def delete_one(cparams):
    try:
        resp = db.mnet.delete_one({"_id": ObjectId(cparams['nid'])})
        #ut.log('\nDeletion successful\n')
        return False, resp
    except Exception as e:
        ut.log(str(e))
        return True, str(e)


# Function to delete record from mongo db
def delete_all():
    try:
        db.mnet.remove({})
        #ut.log('\nDeletion successful\n')
        return False, None
    except Exception as e:
        ut.log(str(e))
        return True, str(e)
