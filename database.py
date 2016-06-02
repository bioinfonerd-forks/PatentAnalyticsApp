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
        vocab = {(k, int(v)) for k, v in vocab.items()}
        model = Analyzer.initialize_model(3, vocab=vocab)
        return model

    def serialize_classifier(self, classifier_object_pickled):
        classifier_compressed = zlib.compress(pickle.dumps(pickle.load(classifier_object_pickled)))
        classifier_compressed_bson = dumps([classifier_compressed])
        return classifier_compressed_bson

    def deserialize_classifier(self, classifier_compressed_bson):
        classifier_compressed_bson = loads([classifier_compressed_bson])
        classifier = pickle.loads(zlib.decompress(classifier_compressed_bson))
        return classifier

    def push(self, collection, id, object):
        self.db[collection].insert([{id:object}])

    def pull(self, collection, id):
        return self.db[collection].find([{id}]).fetch()


if __name__ == "__main__":
    config = Config()
    database = Database(config)
    # models = ["title_feature_model", "abstract_feature_model", "claims_feature_model"]
    # for model in models:
    #     path = """D:\\Workspace\\PatentAnalyticsApp\\models\\""" + model + ".dill"
    #     model_bson = database.serialize(open(path, 'rb'))
    #     database.push('feature-models', model, model_bson)
    #     # print(model)

    classifier = "SGD2016-05-03"
    path = """D:\\Workspace\\PatentAnalyticsApp\\models\\""" + classifier + ".dill"
    classifier_serialized = database.serialize_classifier(open(path, 'rb'))
    database.push('classifiers', classifier, classifier_serialized)

