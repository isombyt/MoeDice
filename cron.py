from google.appengine.api import taskqueue
from google.appengine.ext import webapp


class CronHandler(webapp.RequestHandler):

    def get(self):
        queue = taskqueue.Queue()
        task = taskqueue.Task(url="/QueueJob",params={"data":""})
        queue.add(task)

app = webapp.WSGIApplication([('/CronJob', CronHandler)],
                                         debug=True)
