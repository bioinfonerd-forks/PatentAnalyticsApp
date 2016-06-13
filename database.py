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
        compressed = zlib.compress(pickle.dumps(pickle.load(object_buffer)))
        compressed_bson = dumps([compressed])
        return compressed_bson

    @staticmethod
    def deserialize(compressed_bson):
        compressed = loads(compressed_bson)
        object = pickle.loads(zlib.decompress(compressed[0]))
        return object

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
            path = self.config.model_dir + "\\" + model + ".dill"
            model_bson = self.serialize(open(path, 'rb'))
            database.put('feature-models', model, model_bson)

    def pull_tfidf_models(self):
        models = ["title_feature_model", "abstract_feature_model", "claims_feature_model"]
        tfidf = dict()
        for model in models:
            db_model = self.get('feature-models', model)
            tfidf[model] = self.deserialize(db_model['model'])
        return tfidf

    def pull_tfidf_models_local(self):
        models = ["title_feature_model", "abstract_feature_model", "claims_feature_model"]
        tfidf = dict()
        for model in models:
            model_path = self.config.model_dir + '/' + model
            tfidf[model] = pickle.load(open(model_path, 'rb'))
        return tfidf

    def push_classifier(self, classifier_name):
        path = self.config.model_dir + "\\" + classifier_name
        classifier_serialized = self.serialize(open(path, 'rb'))
        database.put('classifiers', classifier_name, classifier_serialized)

    def pull_classifier(self, classifier_name):
        db_model = self.get('classifiers', classifier_name)
        return self.deserialize(db_model['model'])

    def pull_classifier_local(self, classifier_name):
        classifier_path = self.config.model_dir + '/' + classifier_name
        return pickle.load(open(classifier_path, 'rb'))


if __name__ == "__main__":
    config = Config()
    database = Database(config)
    # database.push_tfidf_models()
    # tfidf = database.pull_tfidf_models()
    classifier_name = "Perceptron2016-06-11"
    # database.push_classifier(classifier_name)
    classifier = database.pull_classifier(classifier_name)
    classifier._predict_proba_lr()
    # config.save_model(classifier, classifier_name)




