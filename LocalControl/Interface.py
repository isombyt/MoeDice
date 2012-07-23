import hashlib
import marshal
import types
import urllib
import urllib2
import config

appurl="http://gplusbot.isombyt.me"

__password__=config.__password__

__auth=hashlib.sha256(__password__).hexdigest()

def func_dumps(func):
    func_serialize={"code":func.func_code,
                    "argdefs":func.func_defaults}
    return marshal.dumps(func_serialize)

def request(url,params={},method="GET",headers={}):
    opener = urllib2.build_opener()
    urllib2.install_opener(opener)
    #if "Content-Type" not in headers:
    #    headers["Content-Type"]="application/json"
    if "auth" not in params:
        params["auth"]=__auth
    if method=="POST":
        request=urllib2.Request(url, urllib.urlencode(params), headers)
    elif method=="GET":
        url=url+"?"+urllib.urlencode(params)
        request=urllib2.Request(url, headers=headers)
    else:
        return 
    return urllib2.urlopen(request).read()


class Config:
    @staticmethod
    def get(name):
        url=appurl+"/InterfaceConfig"
        return request(url,{"name":name},"GET")
    @staticmethod
    def post(name,val):
        base64="False"
        url=appurl+"/InterfaceConfig"
        for c in val:
            if c>'\x7f':
                val=val.encode('base64')
                base64="True"
                break
        return request(url,{"name":name,"val":val,"base64":base64},"POST")


class Execute:
    @staticmethod
    def post(code):
        if type(code)==type(""):
            print code
            code=compile(code,"","exec")
        bytecode=marshal.dumps(code)
        print repr(bytecode.encode("base64"))
        url=appurl+"/InterfaceExecute"
        result=request(url,{"bytecode":bytecode.encode("base64")},"POST")
        print result

