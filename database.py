import dill as pickle
from bson.json_util import dumps
from config import Config


def translate_to_bson(dill_object):
    obj = pickle.load(dill_object)
    bson_object = dumps(obj)
    return bson_object


if __name__ == "__main__":
    config = Config()
    path = config.get_model_path('abstract')
    translate_to_bson(open(path, 'rb'))


