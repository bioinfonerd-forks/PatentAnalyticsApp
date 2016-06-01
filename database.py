import dill as pickle
from bson.json_util import dumps
from config import Config
from sklearn.feature_extraction.text import TfidfVectorizer
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


def translate_to_bson(dill_object):
    obj = pickle.load(dill_object)
    vocab = obj.vocabulary_
    bson_object = dumps(vocab)
    print(bson_object)


if __name__ == "__main__":
    config = Config()
    path = """D:\\Workspace\\PatentAnalyticsApp\\models\\title_feature_model.dill"""
    translate_to_bson(open(path, 'rb'))


