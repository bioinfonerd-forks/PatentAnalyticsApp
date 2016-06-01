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

    def unserialize(self, bson_object):
        vocab = loads(bson_object)
        vocab = {(k, int(v)) for k, v in vocab.items()}
        model = Analyzer.initialize_model(3, vocab=vocab)
        return model


if __name__ == "__main__":
    config = Config()
    database = Database(config)
    models = ["title_feature_model.dill", "abstract_feature_model.dill", "claims_feature_model.dill"]
    path = """D:\\Workspace\\PatentAnalyticsApp\\models\\""" + models[0]
    model_bson = database.serialize(open(path, 'rb'))
    # database.push(model_bson)
    # database.pull(model_id)
    model = database.unserialize(model_bson)
    print(model)


