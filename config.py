import os


class Config(object):
    def __init__(self, debug=True):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.MONGODB_URI = 'mongodb://mongo_test_user:testtest0@ds021333.mlab.com:21333/heroku_bx11p419'
