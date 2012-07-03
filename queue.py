from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext import db

import re
import sys
import urllib
import urllib2
import marshal

class QueueHandler(webapp.RequestHandler):

    def post(self):
        notiStr=self.request.get('noti')
        noti=marshal.loads(notiStr)


class TestHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("test Success")

app = webapp.WSGIApplication([('/QueueJob', QueueHandler),
                              ('/Test', TestHandler)],
                                         debug=True)
