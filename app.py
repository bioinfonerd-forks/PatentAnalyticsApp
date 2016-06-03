from flask import Flask, request, render_template
from scipy.sparse import hstack
from flask_basicauth import BasicAuth
from database import Database
from config import Config

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
        tfidf = database.pull_tfidf_models()

        title_vector = tfidf['title_feature_model'].transform([title])
        abstract_vector = tfidf['abstract_feature_model'].transform([abstract])
        claims_vector = tfidf['claims_feature_model'].transform([claims])

        feature_vector = hstack([title_vector, abstract_vector])
        feature_vector = hstack([feature_vector, claims_vector])

        classifier = database.pull_classifier()
        group = classifier.predict(feature_vector)

        return render_template('query.html', group=group)

if __name__ == '__main__':
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get("PORT", 5000)))
    #app.run()
