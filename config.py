import os
from datetime import date


class Config(object):
    def __init__(self, debug=True):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_uri='ds021333.mlab.com:21333/heroku_bx11p419'
        self.user_name='mongo_test_user'
        self.passwd='testmong0'
