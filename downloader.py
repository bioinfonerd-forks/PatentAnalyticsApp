 import requests 
 import tempfile
 from boto import Key 
 
 
  def download(file):
            key = Key(mybucket, file)
            tempfilename = tempfile.mktemp()
            key.get_contents_to_filename(tempfilename)
            return open(tempfilename,'rb')
