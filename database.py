import dill as pickle
from bson.json_util import dumps, loads
from config import Config
import gridfs
import pymongo
import zlib


class Database(object):
    def __init__(self, config):
        self.config = config
        self.db = self.connect()
        self.fs = gridfs.GridFS(self.db)

    def connect(self):
        client = pymongo.MongoClient(self.config.MONGODB_URI)
        db = client.get_default_database()
        return db

    @staticmethod
    def serialize(object_buffer):
        classifier_compressed = zlib.compress(pickle.dumps(pickle.load(object_buffer)))
        classifier_compressed_bson = dumps([classifier_compressed])
        return classifier_compressed_bson

    @staticmethod
    def deserialize(classifier_compressed_bson):
        classifier_compressed = loads(classifier_compressed_bson)
        classifier = pickle.loads(zlib.decompress(classifier_compressed[0]))
        return classifier

    def put(self, collection, id, object):
        data = {"name": id, "model": object}
        self.db[collection].insert([data])

    def put_fs(self, name, model):
        model = model.encode()
        self.fs.put(model, name=name)

    def get(self, collection, id):
        collectiondb = self.db[collection]
        return collectiondb.find_one({"name": id})

    def get_fs(self, name):
        bytes = self.fs.find_one({"name": name})
        return bytes.read().decode()

    def push_tfidf_models(self):
        models = ["title_feature_model", "abstract_feature_model", "claims_feature_model"]
        for model in models:
            path = """D:\\Workspace\\PatentAnalyticsApp\\models\\""" + model + ".dill"
            model_bson = self.serialize(open(path, 'rb'))
            database.put_fs(model, model_bson)

    def pull_tfidf_models(self):
        models = ["title_feature_model", "abstract_feature_model", "claims_feature_model"]
        tfidf = dict()
        for model in models:
            db_model = self.get_fs(model)
            tfidf[model] = self.deserialize(db_model)
        return tfidf

    def push_classifier(self):
        classifier_name = "SGD2016-05-03"
        path = """D:\\Workspace\\PatentAnalyticsApp\\models\\""" + classifier_name + ".dill"
        classifier_serialized = self.serialize(open(path, 'rb'))
        database.put('classifiers', classifier_name, classifier_serialized)

    def pull_classifier(self):
        classifier_name = "SGD2016-05-03"
        db_model = self.get('classifiers', classifier_name)
        return self.deserialize(db_model['model'])


if __name__ == "__main__":
    config = Config()
    database = Database(config)
    # database.push_tfidf_models()
    tfidf = database.pull_tfidf_models()



