import logging as l
onelog=l.LogRecord('name','10',pathname=__file__,lineno=10,msg='haha',args=None,exc_info=None,func=None)
print onelog
print onelog.getMessage()

log_dict={
        'name':'name',
        'levelno':'15',
        'lineno':'11',
        'msg':'hehe',
        'pathname':'path'

        }


secondlog=l.makeLogRecord(log_dict)
print secondlog
