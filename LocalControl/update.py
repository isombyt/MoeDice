import bot
import Interface
import GPlusAPI
import config
import sys
import marshal


print "login google account %s"%config.email
u=GPlusAPI.User()
u.userID=config.userID
if u.login(config.email,config.password):
    print "login successed"
else:
    print "login failed"
    print "exiting"
    sys.exit(1)
if len(config.baseUrl)>0:
    u.baseUrl=config.baseUrl
print "-"*80
userData=u.dump()
print "account Info:"
print "cookie:"
print userData["cookie"]
print "sessionID:"
print userData["sessionID"]
print "baseUrl:"
print userData["baseUrl"]
print "-"*80
print "update google account information..."
Interface.Config.post("user",marshal.dumps(userData))
print "-"*80
print "find %d bot rules"%len(bot.bot)
print "serializing bot"
serialized=[[rule[0],Interface.func_dumps(rule[1])] for rule in bot.bot]
print "update bot"
Interface.Config.post("bot",marshal.dumps(serialized))
print "-"*80
print "all finished"
