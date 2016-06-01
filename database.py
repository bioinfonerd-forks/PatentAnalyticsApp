import dill as pickle
from bson.json_util import dumps, loads
from config import Config
from analyzer import Analyzer
from pymongo import MongoClient


class Database(object):
    def __init__(self, config):
        self.config = config
        self.client=self.connect()

    def connect(self):
        client = MongoClient(self.config.db_uri)
        client.the_database.authenticate(self.config.user_name, self.config.passwd, mechanism='SCRAM-SHA-1')
        return client


def serialize(analyzer_object):
    obj = pickle.load(analyzer_object)
    vocab = obj.vocabulary_
    vocab = {(k,str(v)) for k,v in vocab.items()}
    bson_object = dumps([vocab])
    return bson_object


def unserialize(bson_object):
    vocab=loads(bson_object)
    model = Analyzer.initialize_model(3, vocab=vocab)


if __name__ == "__main__":
    config = Config()
    models = ["title_feature_model.dill", "abstract_feature_model.dill", "claims_feature_model.dill"]
    path = """D:\\Workspace\\PatentAnalyticsApp\\models\\""" + models[0]
    model_bson = serialize(open(path, 'rb'))
    model = unserialize(model_bson)
    print(model)


