import urllib
import urllib2
import StrCookieJar
import re
import time
import json
import logging

getTime=lambda:int((time.time()*1000-time.timezone)%1000000)

def parseJSON(json):
    json=json.replace("[,","[None,")
    json=json.replace(",,",",None,")
    json=json.replace(",,",",None,")
    json=json.replace(",]",",None]")
    return eval("#"+json)

class User:

    def __init__(self,user=[]):
        if "cookie" in user:
            self.cookie=StrCookieJar.StrCookieJar(user["cookie"])
        else:
            self.cookie=StrCookieJar.StrCookieJar("")
        if "baseUrl" in user:
            self.baseUrl=user["baseUrl"]
        else:
            self.baseUrl="https://plus.google.com"
        if "sessionID" in user:
            self.sessionID=user["sessionID"]
        else:
            self.sessionID=""
        if "userID" in user:
            self.userID=user["userID"]
        else:
            self.userID=""

    def dump(self):
        user={}
        user["cookie"]=self.cookie.dump()
        user["baseUrl"]=self.baseUrl
        user["sessionID"]=self.sessionID
        user["userID"]=self.userID
        return user

    def parseForm(self,data):
        params={}
        _dsh="""name="dsh" id="dsh" value="(.+?)"\n"""
        _GALX="""name="GALX"\n         value="(.+?)">"""
        params["dsh"]=re.findall(_dsh,data,re.S)[0]
        params["GALX"]=re.findall(_GALX,data,re.S)[0]
        return params

    def refreshInfo(self):
        url=self.baseUrl+"/"
        responText=self.request(url,method="GET")
        _sessionID="(AObGSA.*:[0-9]+)"
        self.sessionID=re.findall(_sessionID,responText)[0]
        return responText
        
    
    def login(self,email,passwd):
        params=self.parseForm(self.request("https://accounts.google.com/Login",method="GET"))
        params['Email']=email
        params['Passwd']=passwd
        params['signIn']='Sign in'
        params['PersistentCookie']='yes'
        url = 'https://accounts.google.com/ServiceLoginAuth'
        headers = {'Referer':'https://accounts.google.com/ServiceLoginAuth',}
        self.request(url, headers, params)
        try:
            self.refreshInfo()
            return True
        except:
            return False
        

    def request(self,url,headers={},params={},method="POST"):
        if 'User-Agent' not in headers:
            headers['User-Agent']='Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1171.0 Safari/537.1'
        if ('Content-type' not in headers) and False:
            headers['Content-type']="application/x-www-form-urlencoded;charset=utf-8"
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(opener)
        if "at" not in params:
            if self.sessionID:
                params["at"]=self.sessionID
        if method=="POST":
            request=urllib2.Request(url, urllib.urlencode(params), headers)
        elif method=="GET":
            request=urllib2.Request(url, headers=headers)
        else:
            return 0
        return urllib2.urlopen(request).read()

    def getNotification(self):
        url=self.baseUrl+'/_/notifications/getnotificationsdata?rt=j&_reqid=%s'%getTime()
        logging.debug(url)
        params={
            "f.req":"[null,[],5,null,[],null,true,[],null,null,null,null,2]"
        }
        return parseJSON(self.request(url,params=params,method="POST"))

    def updateReadTime(self,updateTime):
        url=self.baseUrl+"/_/notifications/updatelastreadtime?rt=j&_reqid=%s"%getTime()
        params={"f.req":json.dumps([updateTime]),}
        return parseJSON(self.request(url,params=params))

    def comment(self,postID,comment):
        url=self.baseUrl+"/_/stream/comment/?rt=j&_reqid=%s"%getTime()
        t=int(time.time()*1000)
        commentData=[postID,
                     "os:%s:%s"%(postID,t),
                     comment,
                     t+3725,
                     None,
                     None,
                     4,
            ]
        params={"f.req":json.dumps(commentData)}
        return parseJSON(self.request(url,params=params))


