#no imports here
#you should only import inside your functions

#every bot has two parts

#the first is the funcitions to procress the comments
#every functions should be writen like 'func' below
def func(rawString,memberID):
    """
        This is an example on how to procress a comment
        args:
            rawString is the whole comment which mentioned you
                may be there is some html tags inside
                if any non-ascii character it will code into utf-8
            memberID is the member who had mentioned you
    """

    comment="oh,yes.i am working fine.but i cant understand you words :P"
    
    """
        you should return the comment content you want to reply
        or return None if you dont want to do this
    """
    return comment

def func2(rawString,memberID):
    #import some modules
    import time
    "here is another example"
    if rawString.find("hello world"):
        return "Godbye World!%s"%time.time()
    else:
        return None


#and the second part is the bot rules list
#it is a list with multi rules
#each rule shoud contains two element
#   [regex pattern,func to handle]
#   or ['default',func]
#       if string did not match any of other rules func will handle it 
bot=[["default",func1],
     [".*hello world.*",func2]]

#only the bot list and the functions listed in bot will be uploaded
