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
import tempfile
from flask_basicauth import BasicAuth
from database import Database
from config import Config
import nltk 


DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_object(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'vt'
app.config['BASIC_AUTH_PASSWORD'] = 'hokies'
basic_auth = BasicAuth(app)

conn = S3Connection()
#AWS_ACCESS_KEY_ID = AKIAJPYNQBFLNNVKU3UQ
#AWS_SECRET_ACCESS_KEY = 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
mybucket = conn.get_bucket('patent-model-data')
nltk.download('punkt')




@app.route('/')
@basic_auth.required
def home():
    return render_template('query.html')


@app.route('/query', methods=['POST', 'GET'])
@basic_auth.required
def submit_query():
    title = None
    abstract = None
    claims = None

    if request.method == 'POST':
        try:
            title = request.form['title']
        except KeyError:
            return render_template('query.html', error=KeyError)

        try:
            abstract = request.form['abstract']
        except KeyError:
            return render_template('query.html', error=KeyError)

        try:
            claims = request.form['claims']
        except KeyError:
            return render_template('query.html', error=KeyError)

        
        def download(file):
            key = Key(mybucket, file)
            tempfilename = tempfile.mktemp()
            key.get_contents_to_filename(tempfilename)
            return open(tempfilename,'rb')
        
    
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
        group = classifier.predict(feature_vector)
        
        #path = config.get_classifier_path('SGD2016-05-03', False)
        #classifier = pickle.load(download('SGD2016-05-03'))
        #group = classifier.predict(feature_vector)

        return render_template('query.html', group=group)



if __name__ == '__main__':
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get("PORT", 5000)))
    #app.run()
