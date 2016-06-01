import dill as pickle
from bson.json_util import dumps, loads
from config import Config
from analyzer import Analyzer
import pymongo


class Database(object):
    def __init__(self, config):
        self.config = config
        self.db = self.connect()

    def connect(self):
        client = pymongo.MongoClient(self.config.MONGODB_URI)
        db = client.get_default_database()
        return db

    def serialize(self, analyzer_object):
        obj = pickle.load(analyzer_object)
        vocab = obj.vocabulary_
        vocab = {(k, str(v)) for k, v in vocab.items()}
        bson_object = dumps([vocab])
        return bson_object

    def unserialize(self, vocab_bson):
        vocab = loads(vocab_bson)
        vocab = {(k, int(v)) for k, v in vocab.items()}
        model = Analyzer.initialize_model(3, vocab=vocab)
        return model

    def push(self, collection, id, object):
        self.db[collection].insert([{id:object}])

    def pull(self, collection, id):
        return self.db[collection].find([{id}]).fetch()


if __name__ == "__main__":
    config = Config()
    database = Database(config)
    models = ["title_feature_model", "abstract_feature_model", "claims_feature_model"]
    for model in models:
        path = """D:\\Workspace\\PatentAnalyticsApp\\models\\""" + model + ".dill"
        model_bson = database.serialize(open(path, 'rb'))
        database.push('feature-models', model, model_bson)
        # print(model)

    classifier = ["SGD2016-05-03"]
    path = """D:\\Workspace\\PatentAnalyticsApp\\classifiers\\""" + classifier + ".dill"
    classifier_bson = database.serialize(open(path, 'rb'))
    database.push('classifiers', classifier, classifier_bson)

