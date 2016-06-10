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
            
        try:
            TC2100 = request.form['TC2100']
        except KeyError:
            return render_template('query.html', error=KeyError)
        
        try:
            TC2400 = request.form['TC2400']
        except KeyError:
            return render_template('query.html', error=KeyError)
        
        try:
            TC2600 = request.form['TC2600']
        except KeyError:
            return render_template('query.html', error=KeyError)
        
        try:
            TC3600 = request.form['TC3600']
        except KeyError:
            return render_template('query.html', error=KeyError)

        classifier_name = "SGD"
        
        if len(TC2100) > 3:
            classifier_name= classifier_name + "21"

        if len(TC2400) > 3:
            classifier_name = classifier_name + "24"

        if len(TC2600) > 3:
            classifier_name = classifier_name + "26"

        if len(TC3600) > 3:
            classifier_name = classifier_name + "36"

        print(classifier_name)

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
    # app.run(host='0.0.0.0', port=int(environ.get("PORT", 5000)))
    app.run()
