from pymongo import MongoClient
import util

@util.singleton
class mongo_objects:
    def __init__(self):
        self._objects = {}
    def register(self, uri, obj):
        self._objects[uri] = obj
    def unregister(self, uri):
        if uri in self._objects:
            del self._objects[uri]
    def getobj(self, uri):
        if uri in self._objects:
            return self._objects[uri]
        else:
            return None
    def show(self):
        print "mongo objects:"
        for uri, obj in self._objects.items():
            print "  " + uri + ":"
            print "  ",
            obj.show()

def regobj(uri, obj):
    objs = mongo_objects()
    objs.register(uri, obj)

def unregobj(uri):
    objs = mongo_objects()
    objs.unregister(uri)

class mongo_collection:
    def __init__(self, collection, uri):
        self._collection = collection
        self._collection_name = collection.name
        self._uri = uri
        regobj(uri, self)
    def __del__(self):
        if unregobj:
            unregobj(self._uri)
    def count(self, filt):
        return self._collection.count_documents(filt)
    def count_all(self):
        return self.count({})
    def insert_one(self, document):
        return self._collection.insert_one(document)
    def insert_many(self, documents):
        return self._collection.insert_many(documents)
    def show(self):
        print "collection %s has %d documents" %(self._uri, self.count_all())

class mongo_db:
    def __init__(self, db, uri):
        self._db = db
        self._db_name = db.name
        self._uri = uri
        regobj(uri, self)
    def __del__(self):
        if unregobj:
            unregobj(self._uri)
    def open_collection(self, collection_name, create_if_not_exist = False):
        if not create_if_not_exist and collection_name not in self._db.collection_names():
            return
        collection = self._db[collection_name]
        m_collection = mongo_collection(collection, self._uri + "/" + collection_name)
        return m_collection
    def show(self):
        print "database %s, opened collection counts %d" %(self._uri, len(self._db.list_collection_names()))

class mongo_clt:
    def __init__(self, ipaddr, port, conn_id):
        self._ipaddr = ipaddr
        self._port = port
        self._conn = MongoClient(ipaddr, port)
        self._uri = "/" + conn_id
        regobj(self._uri, self)
    def __del__(self):
        self._conn.close()
        if unregobj:
            unregobj(self._uri)
    def open_db(self, db_name, create_if_not_exist = False):
        if not create_if_not_exist and db_name not in self._conn.database_names():
            return
        db = self._conn[db_name]
        m_db = mongo_db(db, self._uri + "/" + db_name)
        return m_db
    def show(self):
        print "connection: %s:%s, opened db counts %d" %(self._ipaddr, self._port, len(self._conn.list_database_names()))

mongo = mongo_clt("172.17.0.1", 10010, "conn1")
objs = mongo_objects()
objs.show()
print "first time show:"

trial_db = mongo.open_db("wk_trial", True)
objs.show()
print "second time show:"

trial_collct = trial_db.open_collection("trial_collection", True)
objs.show()
print "third time show:"

student1 = { 'id':'9527', 'name':'Jordan007', 'age':20, 'gender':'male' }
student2 = { 'id':'9528', 'name}':'"Jo"r"d{an008', 'age':20, 'gender':'female' }
student3 = { 'id':'9529', 'name':'Jordan009', 'age':20, 'gender':'male' }
result = trial_collct.insert_many([student1, student2, student3])
print result
objs.show()
print "forth time show:"

print "Bye"
'''
db = conn.local
collection = db.local_test1


def browse_json(document_json, func):
    for (key, val) in document_json.items():
        func(key, val)

def get_print_func(indent):
    def print_json(key, val):
        if isinstance(val, dict):
            print " " * indent + "key=", key
            browse_json(val, get_print_func(indent+2))
        else:
            print " " * indent + "key,val=",key,val
    return print_json

print "connection ok"
for db_name in conn.database_names():
    db = conn[db_name]
    print "  browsing database ", db.name, db_name

    for collection_name in db.collection_names():
        collection = db[collection_name]
        print "    browsing collection ", collection.name, count_documents()
        docs = collection.find()
        for doc in docs:
            print "      doc ", doc
            browse_json(doc, get_print_func(8))

conn.close()
'''
