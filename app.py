from flask import Flask, request, render_template
from scipy.sparse import hstack
from flask_basicauth import BasicAuth
from database import Database
from config import Config
from analyzer import Analyzer
from dill import pickle 

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
app = Flask(__name__)
app.config.from_object(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'vt'
app.config['BASIC_AUTH_PASSWORD'] = 'hokies'

basic_auth = BasicAuth(app)

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


        config = Config()
        database = Database(config)
        title_vocab_bson = database.pull('feature-models', 'title')
        abstract_vocab_bson = database.pull('feature-models', 'abstract')
        claims_vocab_bson = database.pull('feature-models', 'claims')
        feature_model_title = Analyzer.initialize_model(3, database.deserialize_tfidf(title_vocab_bson))
        feature_model_abstract = Analyzer.initialize_model(3, database.deserialize_tfidf(abstract_vocab_bson))
        feature_model_claims = Analyzer.initialize_model(3, database.deserialize_tfidf(claims_vocab_bson))

        title_vector = feature_model_title.transform([title])
        abstract_vector = feature_model_abstract.transform([abstract])
        claims_vector = feature_model_claims.transform([claims])

        feature_vector = hstack([title_vector, abstract_vector])
        feature_vector = hstack([feature_vector, claims_vector])

        classifier = database.pull('classifier-models', 'SGD2016-05-03')
        classifier = database.deserialize_classifier(classifier)
        group = classifier.predict(feature_vector)

        return render_template('query.html', group=group)

if __name__ == '__main__':
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get("PORT", 5000)))
    #app.run()
