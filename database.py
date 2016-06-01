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
        parsed = urlsplit(url)
        db_name = parsed.path[1:]

        # Get your DB
        db = Connection(url)[db_name]

        # Authenticate
        if '@' in url:
            user, password = parsed.netloc.split('@')[0].split(':')
            db.authenticate(user, password)
        client = MongoClient(self.config.database_uri)
        client.the_database.authenticate(self.config.user_name, self.config.passwd, mechanism='SCRAM-SHA-1')
        return client

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
    database.push(model_bson)
    database.pull(model_id)
    model = database.unserialize(model_bson)
    print(model)


