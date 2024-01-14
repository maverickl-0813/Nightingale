import os
import logging
import pymongo
from pymongo.errors import *


class DataController:

    def __init__(self):
        self.db_name = "med_data_db"
        self.mongodb_host = os.environ['MONGODB_HOST']
        self.mongodb_user = os.environ['MONGODB_USER']
        self.mongodb_pass = os.environ['MONGODB_PASS']
        self.collection_name = None
        self.db_client = None
        self.db_inst = None
        self.collection_inst = None
        self._init_db_conn()
        self.default_projection = {'_id': 0}

    def _validate_db_conn_strings(self):
        if not self.mongodb_host:
            logging.error("MONGODB_HOST is not supplied.")
            return False
        if not self.mongodb_user:
            logging.error("MONGODB_USER is not supplied.")
            return False
        if not self.mongodb_pass:
            logging.error("MONGODB_PASS is not supplied.")
            return False
        return True

    def _init_db_conn(self):
        if self._validate_db_conn_strings():
            uri = f"mongodb+srv://{self.mongodb_user}:{self.mongodb_pass}@{self.mongodb_host}/"
        else:
            raise ValueError("Cannot compose the URI for MongoDB connection.")

        try:
            self.db_client = pymongo.MongoClient(uri)
            self.db_inst = self.db_client[self.db_name]
        except ConnectionFailure as e:
            emsg = f"Connection with MongoDB failed. Reason: str{e}"
            logging.error(emsg)
            raise emsg
        except Exception:
            raise

    def _set_collection(self):
        if self.db_inst is not None:
            try:
                self.collection_inst = self.db_inst[self.collection_name]
            except CollectionInvalid:
                raise

    def query_one_in_collection(self, resource, query_filter=None, query_projection=None):
        self.collection_name = resource
        self._set_collection()
        if not query_filter:
            query_filter = dict()
        if not query_projection:
            query_projection = dict()
        query_projection.update(self.default_projection)
        query_result = self.collection_inst.find_one(query_filter, query_projection)
        return query_result

    def query_multi_in_collection(self, resource, query_filter=None, query_projection=None):
        self.collection_name = resource
        self._set_collection()
        if not query_filter:
            query_filter = dict()
        if not query_projection:
            query_projection = dict()
        query_projection.update(self.default_projection)
        query_result = self.collection_inst.find(query_filter, query_projection)
        return query_result

    def count_in_collection(self, resource, query_filter=None):
        self.collection_name = resource
        self._set_collection()
        if not query_filter:
            query_filter = dict()
        count = self.collection_inst.count_documents(query_filter)
        return count

    def insert_multi_to_collection(self, resource, list_data):
        self.collection_name = resource
        self._set_collection()
        self.collection_inst.insert_many(list_data)

    def insert_one_to_collection(self, resource, data):
        self.collection_name = resource
        self._set_collection()
        self.collection_inst.insert_one(data)

    def replace_one_to_collection(self, resource, old_filter, new_entry):
        self.collection_name = resource
        self._set_collection()
        self.collection_inst.replace_one(old_filter, new_entry, upsert=True)

    def delete_all_in_collection(self, resource):
        self.collection_name = resource
        self._set_collection()
        self.collection_inst.delete_many({})

    def create_index_in_collection(self, resource, field, unique=False):
        self.collection_name = resource
        self._set_collection()
        self.collection_inst.create_index(field, unique=unique)
