
def defaultHandler(rawString,memberID):
    "default handler"
    comment="@%s no rule match"%memberID #way to mention the member who had mention you
    return comment

def DiceHandler(rawString,memberID):
    "handles the rule '(\d+)d(\d+)'"
    import re
    import random
    "import must write inside every functions which need it"
    result=re.findall("(\d+)d(\d+)",rawString)#get the re match result
    if len(result)>0:
        num=int(result[0][0])
        max=int(result[0][1])
        if num==0 or max==0:
            comment=='error input'
        else:
            lst=[str(random.randint(0,max)) for i in range(num)]
            comment='%sdices roled %s'%(num,'\xe3\x80\x81'.join(lst))
        comment="@%s %s"%(memberID,comment)#add a mention
        return comment
    return None
        

bot=[["default",defaultHandler],#make function defaultHandler default
     ["(\d+)d(\d+)",DiceHandler],]#handle '(\d+)d(\d+)' with function DiceHandler






"""
some local test code,copied from server/ParseNotification.py to test the bot
forget it if you cant understand it
"""
import re

if __name__=="__main__":
    rawString='1024d1024'
    memberID="233233233"
    comment=None
    for single in bot:
        if single[0]=="default":
            try:
                botDefault=single[1]
            except:
                    botDefault=None
        else:
            if re.search(single[0],rawString):
                print single[0]
                bot=single[1]
                comment=bot(rawString,memberID)
                if comment:break
    if comment==None and botDefault:
        print "default"
        comment=botDefault(rawString,memberID)
    print comment.decode("u8")
