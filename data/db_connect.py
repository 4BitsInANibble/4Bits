import os

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

RECIPE_DB = 'recipeDB'
USERS_COLLECTION = 'Users'
RECIPE_COLLECTION = 'Recipes'
FOOD_COLLECTION = 'FOOD'

client = None

MONGO_ID = '_id'


def connect_db():
    """
    This provides a uniform way to connect to the DB across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    We should probably either return a client OR set a
    client global.
    """
    print("CONNECTING!!!!")
    global client
    if client is None:  # not connected yet!
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
            password = os.environ.get("MONGO_DB_PASSWORD")
            if not password:
                raise ValueError('You must set your password '
                                 + 'to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")
            client = pm.MongoClient(f'mongodb+srv://nz2065:{password}'
                                    + '@nibble.pcnhctc.mongodb.net/'
                                    + '?retryWrites=true&w=majority')
            # PA recommends these settings:
            # + 'connectTimeoutMS=30000&'
            # + 'socketTimeoutMS=None
            # + '&connect=false'
            # + 'maxPoolsize=1')
            # but they don't seem necessary

        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient()


def insert_one(collection, doc, db=RECIPE_DB):
    """
    Insert a single doc into collection.
    """
    print(f'{db=}')
    return client[db][collection].insert_one(doc)


def fetch_one(collection, filt, fields=None, db=RECIPE_DB):
    """
    Find with a filter and return on the first doc found.
    """
    res = client[db][collection].find(filt, fields)
    if res is not None:
        for doc in res:
            if MONGO_ID in doc:
                # Convert mongo ID to a string so it works as JSON
                doc[MONGO_ID] = str(doc[MONGO_ID])
            return doc

    raise ValueError("Object to fetch does not exist")


def del_one(collection, filt, db=RECIPE_DB):
    """
    Find with a filter and return on the first doc found.
    """
    client[db][collection].delete_one(filt)


def fetch_all(collection, db=RECIPE_DB):
    ret = []
    res = client[db][collection].find()
    if res is not None:
        for doc in res:
            ret.append(doc)
    return ret


def fetch_all_as_dict(key, collection, db=RECIPE_DB):
    ret = {}
    res = client[db][collection].find()
    if res is not None:
        for doc in res:
            del doc[MONGO_ID]
            ret[doc[key]] = doc
    return ret


def update_one(collection, filter, query, db=RECIPE_DB):
    return client[db][collection].update_one(filter, query)


def update_many(collection, filter, query, db=RECIPE_DB):
    return client[db][collection].update_many(filter, query)


def aggregate(collection, pipeline, db=RECIPE_DB):
    return client[db][collection].aggregate(pipeline)


def status(db=RECIPE_DB):
    server_status = client.admin.command('serverStatus')
    db_stats = client[db].command('dbstats')
    return server_status, db_stats
