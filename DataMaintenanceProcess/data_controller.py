import pymongo


class DataController:

    def __init__(self):
        self.db_name = "med_data_db"
        self.collection_name = None
        self.db_client = None
        self.db_inst = None
        self.collection_inst = None
        self._init_db_conn()

    def _init_db_conn(self):
        self.db_client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        self.db_inst = self.db_client[self.db_name]

    def _set_collection(self):
        if self.db_inst is not None:
            self.collection_inst = self.db_inst[self.collection_name]

    def display_collection(self, resource):
        self.collection_name = resource
        self._set_collection()
        rows = self.collection_inst.find()
        for row in rows:
            print(row)

    def query_one_in_collection(self, resource, query_filter=None):
        self.collection_name = resource
        self._set_collection()
        if not query_filter:
            query_filter = dict()
        query_result = self.collection_inst.find_one(query_filter)
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
