from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext import db


import logging
import marshal
import GPlusAPI
import re
import types


from HTMLParser import HTMLParser
class MyParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.buf=""
        self.mention=False

    def handle_starttag(self,tag,attrs):
        #print "start",tag
        #print "start",tag
        if tag=="a":
            for key,val in attrs:
                if key=="oid":
                    self.buf+=val
                    self.mention=True
        if tag=="b":
            self.buf+="*"
        elif tag=="s":
            self.buf+="-"
        elif tag=="i":
            self.buf+="_"

    def handle_endtag(self,tag):
        if tag=="b":
            self.buf+="*"
        elif tag=="s":
            self.buf+="-"
        elif tag=="i":
            self.buf+="_"
        elif tag=="br":
            self.buf+='\n'

    def handle_data(self,data):
        #print data,self.mention
        if not self.mention:
            self.buf+=data
        else:
            self.mention=False

def func_loads(func_serialized):
    func_serialize=marshal.loads(func_serialized)
    func=types.FunctionType(globals=globals(),**func_serialize)
    return func

class ConfigStore(db.Model):
    data = db.BlobProperty()

class NotificationStore(db.Model):
    data = db.BlobProperty()

decode=lambda string:eval(repr(string.decode("u8")).replace('\\\\\\\\',"\\").replace("\\\\","\\")).encode("u8")

class ParseHandler(webapp.RequestHandler):

    def post(self):
        userData=ConfigStore.get_or_insert("user",data="{0")
        userData=marshal.loads(userData.data)
        u=GPlusAPI.User(userData)
        key=self.request.get('key')
        notificationStore=NotificationStore.get(key)
        #logging.debug(notificationStore.data)
        notification=marshal.loads(notificationStore.data)
        postID = notification[10];
        memberID = notification[18][0][0][16]
        logging.debug("procssing %s from %s %s"%(
            postID,notification[18][0][0][3],memberID))
        logging.debug("Main Post:%s"%notification[18][0][0][20])
        for i in range(len(notification[2])):
            block=notification[2][i]
            if block[0] not in (4,6):
                logging.debug("Notification Type is %s"%block[1][0][1])
                rawString=None
                if block[1][0][1]==16:
                    if i!=0:
                        continue
                    rawString = notification[18][0][0][47]
                    if not rawString:
                        rawString = notification[18][0][0][4]
                elif block[1][0][1]==15:
                    if len(notification[18][0][0][7])==2:
                        lastMemberID = ""
                        memberID = notification[18][0][0][7][1][6]
                        if memberID != u.userID:
                            rawString = notification[18][0][0][7][1][2]
                        else:
                            _oid='oid="(\d+)"'
                            lastMemberID=re.findall(_oid,notification[18][0][0][7][1][2])
                            if len(lastMemberID)<1:
                                continue
                        memberID=notification[18][0][0][7][0][6]
                        if memberID!=u.userID and memberID!=lastMemberID:
                            rawString=notification[18][0][0][7][0][2]
                    elif notification[18][0][0][7][0][6] != u.userID:
                        memberID =notification[18][0][0][7][0][6]
                        rawString =notification[18][0][0][7][0][2]
                    if rawString!=None:
                        logging.debug("found comment %s"%decode(rawString))
                else:
                    continue
                rawString=decode(rawString)
                parser=MyParser()
                parser.feed(rawString)
                rawString=parser.buf
                logging.debug("metioned commet:%s"%repr(rawString))
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
