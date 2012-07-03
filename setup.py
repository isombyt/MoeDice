from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext import db
import GPlusAPI

class ConfigStore(db.Model):
    data = db.BlobProperty()

class SetupHandler(webapp.RequestHandler):

    def post(self):
        cookie=self.request.get('cookie')
        if len(cookie)>0:
            dbCookie=ConfigStore.get_or_insert("Cookie",data="")
            dbCookie.data=cookie
            dbCookie.put()
        else:
            email=self.request.get('email')
            passwd=self.request.get('passwd')
            u=GPlusAPI.User(email,passwd)
            u.login()
            dbCookie=ConfigStore.get_or_insert("Cookie","")
            dbCookie.data=u.dumpCookie()
            dbCookie.put()
            

app = webapp.WSGIApplication([('/Setup', CronHandler)],
                                         debug=True)
