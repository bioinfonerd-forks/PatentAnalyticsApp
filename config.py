import os
import dill as pickle


class Config(object):
    def __init__(self, debug=True):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_dir = os.path.join(self.base_dir, 'models')
        self.MONGODB_URI = 'mongodb://mongo_test_user:testtest0@ds021333.mlab.com:21333/heroku_bx11p419'


    def save_model(self, model, name):
        path = os.path.join(self.model_dir, name)
        pickle.dump(model, open(path, 'wb'))