from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext import db


import logging
import GPlusAPI
import marshal

class ConfigStore(db.Model):
    data = db.BlobProperty()

class NotificationStore(db.Model):
    data = db.BlobProperty()

class CheckHandler(webapp.RequestHandler):

    def get(self):
        parseQueue = taskqueue.Queue(name="parse")
        userData=ConfigStore.get_or_insert("user",data="{0")
        userData=marshal.loads(userData.data)
        if len(userData)<=0:
            logging.error("didn't login")
            self.response.out.write("didn't login")
        u=GPlusAPI.User(userData)
        raw=u.getNotification()
        notifications=raw[0][1][1][0]
        for notification in notifications:
            if len(notification[18])>0 and \
                notification[18][0]!=None and \
                len(notification[18][0])>=9 and \
                notification[18][0][8]!=None:
                if notification[18][0][8][3]==None:
                    notificationStore=NotificationStore()
                    notificationStore.data=marshal.dumps(notification)
                    notificationStore.put()
                    task = taskqueue.Task(url="/ParseNotification",params={"key":notificationStore.key()})
                    parseQueue.add(task)
                    logging.debug("post ID:%s added to queue"%notification[10])
        u.updateReadTime(int(notifications[0][3]))
        checkQueue=taskqueue.Queue()
        task = taskqueue.Task(url="/CheckNotification")
        checkQueue.add(task)
        
    def post(self):
        return self.get()

app = webapp.WSGIApplication([('/CheckNotification', CheckHandler)],
                                         debug=True)
