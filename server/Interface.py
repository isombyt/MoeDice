from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext import db

import marshal
import hashlib
import sys
import logging

__password__="idontknow"

__auth=hashlib.sha256(__password__).hexdigest()

def func_loads(func_serialized):
    func_serialize=marshal.loads(func_serialized)
    func=types.FunctionType(globals=globals(),**func_serialize)
    return func

def auth(self):
    auth=self.request.get('auth')
    if auth!=__auth:
        self.error(403)

class ConfigStore(db.Model):
    data = db.BlobProperty()

class Config(webapp.RequestHandler):

    def get(self):
        #auth(self)
        configName=str(self.request.get('name'))
        configData=ConfigStore.get_or_insert(configName,
                                             data=marshal.dumps(None))
        self.response.out.write(configData.data)

    def post(self):
        #auth(self)
        configName=str(self.request.get('name'))
        val=str(self.request.get('val'))
        base64=str(self.request.get('base64'))
        if base64.lower()=="true":
            val=val.decode("base64")
        logging.debug("%s:%s"%(configName,repr(val)))
        configData=ConfigStore.get_or_insert(configName,
                                             data=marshal.dumps(None))
        configData.data=val
        configData.put()

class logger:
    
    def __init__(self):
        self.data=""

    def write(self,data):
        self.data+=data

class Execute(webapp.RequestHandler):

    def get(self):
        self.error(404)

    def post(self):
        #auth(self)
        bytecode=self.request.get('bytecode').decode("base64")
        logging.debug(repr(bytecode))
        code=marshal.loads(bytecode)
        log=logger()
        oldstdout=sys.stdout
        sys.stdout=log
        exec code
        self.response.out.write(log.data)
        

app = webapp.WSGIApplication([('/InterfaceConfig', Config),
                              ('/InterfaceExecute', Execute)],
                                         debug=True)
