import urllib
import urllib2
import StrCookieJar
import re
import time


getTime=lambda:int((time.time()*1000-time.timezone)%1000000)

def parseJSON(json):
    json=json.replace("[,","[None,")
    json=json.replace(",,",",None,")
    json=json.replace(",,",",None,")
    json=json.replace(",]",",None]")
    return eval(json[6:])

class User:

    def __init__(self,email="",passwd=""):
        self.email=email
        self.passwd=passwd
        self.cookie=StrCookieJar.StrCookieJar()

    def loadCookie(self,cookie):
        self.cookie=StrCookieJar.StrCookieJar(cookie)

    def dumpCookie(self):
        return self.cookie.dump()

    def parseForm(self,data):
        params={}
        _dsh="""name="dsh" id="dsh" value="(.+?)"\n"""
        _GALX="""name="GALX"\n         value="(.+?)">"""
        params["dsh"]=re.findall(_dsh,data,re.S)[0]
        params["GALX"]=re.findall(_GALX,data,re.S)[0]
        return params
    
    def login(self):
        params=self.parseForm(self.request("https://accounts.google.com/Login"))
        params['Email']=self.email
        params['Passwd']=self.passwd
        params['signIn']='Sign in'
        params['PersistentCookie']='yes'
        login_url = 'https://accounts.google.com/ServiceLoginAuth'
        login_data = urllib.urlencode(params)
        login_headers = {'Referer':'https://accounts.google.com/ServiceLoginAuth',}
        return self.request(login_url, login_headers, login_data)

    def request(self,url,headers={},params="",method="POST"):
        if 'User-Agent' not in headers:
            headers['User-Agent']='Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1171.0 Safari/537.1'
        if ('Content-type' not in headers) and False:
            headers['Content-type']="application/x-www-form-urlencoded;charset=utf-8"
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(opener)
        if method=="POST":
            request=urllib2.Request(url, params, headers)
        elif method=="GET":
            request=urllib2.Request(url, headers=headers)
        else:
            return 0
        return urllib2.urlopen(request).read()

    def getNotification(self):
        url='https://plus.google.com/_/notifications/getnotificationsdata?rt=j&_reqid=%s'%getTime()
        return parseJSON(self.request(url,method="GET"))

    def updateReadTime(self,time):
        url="https://plus.google.com/_/notifications/updatelastreadtime?rt=j&_reqid=%s"%getTime()
        print url
        return parseJSON(self.request(url))

    def comment(self,**agrs):
        #didn't finished
        return

def parseNotification(self,noti=None):
    import marshal
    noti=marshal.load(file("g:\\data"))

if __name__=="__main__":
    u=User("email","passwd")
    u.login()
    cookie=u.dumpCookie()
    u=User()
    u.loadCookie(cookie)
    notis=u.getNotification()
