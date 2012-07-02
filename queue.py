from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext import db

import re
import sys
import urllib
import urllib2


class QueueHandler(webapp.RequestHandler):

    def post(self):
        dn=self.request.get('data')


class TestHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("test Success")

app = webapp.WSGIApplication([('/QueueJob', QueueHandler),
                              ('/Test', TestHandler)],
                                         debug=True)
