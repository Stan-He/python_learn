#!encoding=utf-8
import logging
F1=logging.Filter(name='myname')
F2=logging.Filter(name='myname')
Fer=logging.Filterer()
Fer.addFilter(F1)
Fer.addFilter(F2)
onelog=logging.LogRecord('myname','10',pathname=__file__,lineno=10,msg='haha',args=None,exc_info=None,func=None)

print Fer.filter(onelog)

FF1=logging.Filter(name='A')
FF2=logging.Filter(name='A.B')
FF3=logging.Filter(name='A.B.C')
two=logging.LogRecord('A.B.C.D','10',pathname=__file__,lineno=10,msg='haha',args=None,exc_info=None,func=None)
FFer=logging.Filterer()
FFer.addFilter(FF1)
FFer.addFilter(FF2)
FFer.addFilter(FF3)
print FFer.filter(two)
