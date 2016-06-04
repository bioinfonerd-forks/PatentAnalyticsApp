import requests 
import tempfile
from boto.s3.key import Key
 
def download(file):
     key = Key(S3Connection().get_bucket('patent-model-data'), file)
     tempfilename = tempfile.mktemp()
     key.get_contents_to_filename(tempfilename)
     return open(tempfilename,'rb')
