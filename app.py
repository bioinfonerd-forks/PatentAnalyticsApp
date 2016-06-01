from flask import Flask, request, render_template

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def home():
    return render_template('query.html')


@app.route('/query', methods=['POST', 'GET'])
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

        # feature_model_title = pickle.load(download('title_feature_model.dill'))
        # title_vector = feature_model_title.transform([title])

        # feature_model_abstract = pickle.load(download('abstract_feature_model.dill'))
        # abstract_vector = feature_model_abstract.transform([abstract])

        # feature_model_claims = pickle.load(download('claims_feature_model.dill'))
        # claims_vector = feature_model_claims.transform([claims])

        # feature_vector = hstack([title_vector, abstract_vector])
        # feature_vector = hstack([feature_vector, claims_vector])

        # classifier = pickle.load(download('SGD2016-05-03'))
        #
        # group = classifier.predict(feature_vector)
        return
        # return render_template('query.html', group=group)

if __name__ == '__main__':
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get("PORT", 5000)))
    #app.run()