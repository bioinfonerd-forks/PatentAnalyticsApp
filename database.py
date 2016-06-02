import dill as pickle
from bson.json_util import dumps, loads
from config import Config
from analyzer import Analyzer
import pymongo
import zlib


class Database(object):
    def __init__(self, config):
        self.config = config
        self.db = self.connect()

    def connect(self):
        client = pymongo.MongoClient(self.config.MONGODB_URI)
        db = client.get_default_database()
        return db

    def serialize_tfidf(self, analyzer_object):
        obj = pickle.load(analyzer_object)
        vocab = obj.vocabulary_
        vocab = {(k, str(v)) for k, v in vocab.items()}
        bson_object = dumps([vocab])
        return bson_object

    def deserialize_tfidf(self, vocab_bson):
        vocab = loads(vocab_bson)
        vocab = {(k, int(v)) for k, v in vocab[0]}
        model = Analyzer.initialize_model(3, vocab=vocab)
        return model

    def serialize(self, object_buffer):
        classifier_compressed = zlib.compress(pickle.dumps(pickle.load(object_buffer)))
        classifier_compressed_bson = dumps([classifier_compressed])
        return classifier_compressed_bson

    def deserialize_classifier(self, classifier_compressed_bson):
        classifier_compressed = loads(classifier_compressed_bson)
        classifier = pickle.loads(zlib.decompress(classifier_compressed[0]))
        return classifier

    def push(self, collection, id, object):
        data = {"name": id, "model": object}
        self.db[collection].insert([data])

    def pull(self, collection, id):
        collectiondb = self.db[collection]
        return collectiondb.find_one({"name": id})

    def push_tfidf_models(self):
        models = ["title_feature_model", "abstract_feature_model", "claims_feature_model"]
        for model in models:
            path = """D:\\Workspace\\PatentAnalyticsApp\\models\\""" + model + ".dill"
            model_bson = self.serialize(open(path, 'rb'))
            database.push('feature-models', model, model_bson)

    def pull_tfidf_models(self):
        models = ["title_feature_model", "abstract_feature_model", "claims_feature_model"]
        tfidf = dict()
        for model in models:
            db_model = self.pull('feature-models', model)
            tfidf[model] = self.deserialize_tfidf(db_model['model'])
        return tfidf

    def push_classifier(self):
        classifier_name = "SGD2016-05-03"
        path = """D:\\Workspace\\PatentAnalyticsApp\\models\\""" + classifier_name + ".dill"
        classifier_serialized = self.serialize(open(path, 'rb'))
        database.push('classifiers', classifier_name, classifier_serialized)

    def pull_classifier(self):
        classifier_name = "SGD2016-05-03"
        db_model = self.pull('classifiers', classifier_name)
        return self.deserialize_classifier(db_model['model'])


if __name__ == "__main__":
    config = Config()
    database = Database(config)
    database.push_tfidf_models()
    tfidf = database.pull_tfidf_models()



