from google.appengine.api import taskqueue
from google.appengine.ext import webapp
import GPlusAPI
import marshal

class ConfigStore(db.Model):
    data = db.BlobProperty()

class CronHandler(webapp.RequestHandler):

    def get(self):
        queue = taskqueue.Queue()
        dbCookie=ConfigStore.get_or_insert("Cookie",data="")
        u=GPlusAPI.User()
        u.loadCookie(dbCookie.data)
        notiData=u.getNotification()
        for noti in notiData[0][1][1][0]:
            if len(noti[18])>0 and \
               noti[18][0]!=None and \
               len(noti[18][0])>=9 and \
               noti[18][0][8]!=None:
                if noti[18][0][8][3]==None:
                    task = taskqueue.Task(url="/QueueJob",params={"noti":marshal.dumps(noti)})
                    queue.add(task)

app = webapp.WSGIApplication([('/CronJob', CronHandler)],
                                         debug=True)
