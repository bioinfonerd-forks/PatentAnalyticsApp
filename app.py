from flask import Flask, request, render_template
from scipy.sparse import hstack
from flask_basicauth import BasicAuth
from database import Database
from config import Config
from os import environ, path
import nltk

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

        classifier_name = "SGD21"
        TC21 = ""
        TC24 = ""
        TC26 = ""
        TC36 = ""
        if len(TC21) > 3:
            classifier_name= classifier_name + "21"

        elif len(TC24) > 3:
            classifier_name = classifier_name + "24"

        elif len(TC26) > 3:
            classifier_name = classifier_name + "26"

        elif len(TC36) > 3:
            classifier_name = classifier_name + "36"
        

        config = Config()
        database = Database(config)
        tfidf = database.pull_tfidf_models()

        title_vector = tfidf['title_feature_model'].transform([title])
        abstract_vector = tfidf['abstract_feature_model'].transform([abstract])
        claims_vector = tfidf['claims_feature_model'].transform([claims])

        feature_vector = hstack([title_vector, abstract_vector])
        feature_vector = hstack([feature_vector, claims_vector])

        classifier = database.pull_classifier(classifier_name)
        group = classifier.predict(feature_vector)

        return render_template('query2.html', group=group, title=title, abstract=abstract, claims=claims)

if __name__ == '__main__':
    nltk.data.path.append(path.join(Config().base_dir, 'nltk_data'))
    app.run(host='0.0.0.0', port=int(environ.get("PORT", 5000)))
