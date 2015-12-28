import logging

F=logging.Formatter(fmt='%(asctime)s:%(message)s:%(pathname)s:%(funcName)s')

onelog=logging.LogRecord('name','10',pathname=__file__,lineno=10,msg='haha',args=None,exc_info=None,func=None)

#print F.formatTime(onelog)
#print type(F.formatTime(onelog))
#F.formatException(ei=)
#print F.usesTime()
print F.format(onelog)
