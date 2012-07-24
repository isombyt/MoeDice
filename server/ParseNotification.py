from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext import db


import logging
import marshal
import GPlusAPI
import re
import types


def func_loads(func_serialized):
    func_serialize=marshal.loads(func_serialized)
    print func_serialize
    func=types.FunctionType(globals=globals(),**func_serialize)
    return func

class ConfigStore(db.Model):
    data = db.BlobProperty()

class NotificationStore(db.Model):
    data = db.BlobProperty()

decode=lambda string:eval("u'%s'"%string.decode("u8","ignore")).encode("u8")

class ParseHandler(webapp.RequestHandler):

    def post(self):
        userData=ConfigStore.get_or_insert("user",data="{0")
        u=GPlusAPI.User(marshal.loads(userData.data))
        key=self.request.get('key')
        notificationStore=NotificationStore.get(key)
        #logging.debug(notificationStore.data)
        notification=marshal.loads(notificationStore.data)
        postID = notification[10];
        for i in range(len(notification[2])):
            block=notification[2][i]
            if block[0] not in (4,6):
                memberID = block[1][0][2][3]
                logging.debug("parsing post ID %s"%postID)
                logging.debug("Main Post:%s"%deocde(
                    notification[18][0][0][20]))
                if len(notification[18][0][0][7])==1:
                    logging.debug("Last comment:%s"%decode(
                        notification[18][0][0][7][0][2]))
                elif len(notification[18][0][0][7])==2:
                    logging.debug("Last comment:%s"%decode(
                        notification[18][0][0][7][1][2]))
                else:
                    logging.debug("Last comment:none")
                logging.debug("Notification Type is %s"%block[1][0][1])
                if block[1][0][1]==16 and i==0:
                    rawString = decode(notification[18][0][0][20])
                elif block[1][0][1]==15:
                    if len(notification[18][0][0][7])==2:
                        rawString=decode(notification[18][0][0][7][1][2])
                    else:
                        rawString=decode(notification[18][0][0][7][0][2])
                else:
                    continue
                logging.debug("metioned commet:%s"%rawString)
                _botMatchList=ConfigStore.get_or_insert("bot",
                                                        data=marshal.dumps([]))
                botMatchList=marshal.loads(_botMatchList.data)
                botDefault=None
                comment=None
                for single in botMatchList:
                    if single[0]=="default":
                        if 1:
                            botDefault=func_loads(single[1])
                        else:
                            botDefault=None
                    else:
                        if 1:
                            if re.search(single[0],rawString):
                                logging.debug("match rule %s"%single[0])
                                func=func_loads(single[1])
                                comment=func(decode(rawString),memberID)
                                if comment:break
                        else:
                            comment=None
                if comment==None and botDefault:
                    logging.debug("default rule")
                    comment=botDefault(rawString,memberID)
                logging.debug("%s#%s:%s"%(postID,memberID,comment))
                if comment:
                    u.comment(postID,comment)
        notificationStore.delete()

class TestHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("test Success")

app = webapp.WSGIApplication([('/ParseNotification', ParseHandler),
                              ('/Test', TestHandler)],
                                         debug=True)
