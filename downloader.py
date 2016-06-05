import requests 
import tempfile
from boto.s3.key import Key
from boto.s3.connection import S3Connection

from flask import Flask, request, render_template, redirect, url_for
import os, json, boto
#import sys
#from datetime import date
from scipy.sparse import hstack
import dill as pickle
import os
from datetime import date
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from flask_basicauth import BasicAuth
from database import Database
from config import Config
import nltk 
from rq import Queue
from worker import conn
 
def download(file):
     key = Key(S3Connection().get_bucket('patent-model-data'), file)
     tempfilename = tempfile.mktemp()
     key.get_contents_to_filename(tempfilename)
     return open(tempfilename,'rb')

def doitall(title, abstract, claims):
      config = Config()
      database = Database(config)
      feature_model_title = pickle.load(download('title_feature_model.dill'))
      title_vector = feature_model_title.transform([title])

      feature_model_abstract = pickle.load(download('abstract_feature_model.dill'))
      abstract_vector = feature_model_abstract.transform([abstract])

      feature_model_claims = pickle.load(download('claims_feature_model.dill'))
      claims_vector = feature_model_claims.transform([claims])

      feature_vector = hstack([title_vector, abstract_vector])
      feature_vector = hstack([feature_vector, claims_vector])
        
      classifier = database.pull_classifier()
      return classifier.predict(feature_vector)
