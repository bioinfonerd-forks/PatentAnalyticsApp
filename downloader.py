import requests 
import tempfile
from boto.s3.key import Key
from boto.s3.connection import S3Connection
 
def download(file):
     key = Key(S3Connection().get_bucket('patent-model-data'), file)
     tempfilename = tempfile.mktemp()
     key.get_contents_to_filename(tempfilename)
     return open(tempfilename,'rb')

def doitall():
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
      return group = classifier.predict(feature_vector)
