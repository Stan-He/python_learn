#!encoding=utf-8
from logging import getLogger,StreamHandler,LoggerAdapter,basicConfig
import sys
import os
import random
L=getLogger('xxx')
#print L.manager
#print L
basicConfig(
    format='%(levelname)s:%(name)s:%(message)s'
    )
L.setLevel('DEBUG')
L.debug('aa')

class myLogger(LoggerAdapter):

    def process(self,msg,kwargs):

        return '(%d),%s' % (self.extra['name1'](1,1000),msg)  ,kwargs

LA=myLogger(L,{'name1':random.randint})

LA.debug('hahah')
LA.debug('hahah')

