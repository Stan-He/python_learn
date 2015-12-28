#!encoding=utf-8
import logging
F1=logging.Filter(name='myname')
F2=logging.Filter(name='myname')
Fer=logging.Filterer()
Fer.addFilter(F1)
Fer.addFilter(F2)
onelog=logging.LogRecord('myname','10',pathname=__file__,lineno=10,msg='haha',args=None,exc_info=None,func=None)

print Fer.filter(onelog)

