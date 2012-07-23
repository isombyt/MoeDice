# -*- coding: utf-8 -*-

def default(rawString,memberID):
    comment="@%s \xe3\x81\x86\xe3\x82\x8b\xe3\x81\x95\xe3\x81\x84"%memberID
    return comment

def Dice(rawString,memberID):
    import re
    import random
    result=re.findall("(\d+)d(\d+)",rawString)
    if len(result)>0:
        num=int(result[0][0])
        max=int(result[0][1])
        if num==0 or max==0:
            comment=='\xe4\xbd\xa0\xe8\x80\x8d\xe8\x80\x81\xe5\xa8\x98\xe6\x98\xaf\xe4\xb8\x8d'
        else:
            lst=[str(random.randint(0,max)) for i in range(num)]
            comment='%s\xe5\x8f\xaa\xe9\xaa\xb0\xe5\xad\x90\xe8\xbd\xac\xe5\x87\xba%s'%(num,'\xe3\x80\x81'.join(lst))
        comment="@%s %s"%(memberID,comment)
        return comment
    return None
        

bot=[["default",default],
     ["(\d+)d(\d+)",Dice],]

import re

if __name__=="__main__":
    rawString='<span class="proflinkWrapper"><span class="proflinkPrefix">+</span><a href="https://plus.google.com/100974053404896066917" class="proflink" oid="100974053404896066917">bit Huang</a></span> 1024d1024﻿'
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
