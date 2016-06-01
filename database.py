import dill as pickle
from bson.json_util import dumps
from config import Config
from sklearn.feature_extraction.text import TfidfVectorizer
from analyzer import Analyzer

def translate_to_bson(dill_object):
    obj = pickle.load(dill_object)
    vocab = obj.vocabulary
    bson_object = dumps(vocab)
    print(bson_object)


if __name__ == "__main__":
    config = Config()
    path = config.get_model_path('abstract')
    translate_to_bson(open(path, 'rb'))


