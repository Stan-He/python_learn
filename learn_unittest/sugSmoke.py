#!/usr/bin/python
#coding:utf-8

#case num="3" redmine="" level="p0" desc="数据类型指定datatype=1（表示公交站）

import unittest
import os,sys
import urllib
from lxml import etree

class TestSequenceFunctions(unittest.TestCase):
    
    def createUrlPrefix(self,ip,port):
        strTmp = 'http://'+ip+':'+port+'/sisserver.php?'
        return strTmp
        
    def setUp(self):
        self.url = self.createUrlPrefix('10.13.5.8','90')
        #print self.url;
        

    def test1(self):
        #self.assertEqual(self.url,'http://10.13.5.8:90')
        paradict = {'query_type':'inputtip', 'data_type': '1', 'citycode': '010','input':'0','query_src':'test','user_info':'test'}
        paradict['language'] = 'chn'
        print paradict
        params = urllib.urlencode(paradict)
        weburl = "%s%s"%(self.url,params)
        print weburl
        f = urllib.urlopen(weburl)
        strRes = f.read()
        print strRes
        root=etree.fromstring(strRes)
        #print root
        etree.tostring(root,pretty_print=True)
        poi_list=root.xpath("/tipresult/list/tip")
        #print poi_list
        list_res = []
        for i in poi_list:
            x1=i.xpath("./name")
            #print x1
            name = x1[0].text
            print name,type(name)
            #self.assertIn(u'总', name) 
            self.assertIn(u'和', x1[0].text,msg='站名匹配错误') 
            list_res.append(x1[0].text)
        #print list_res


    def test3(self):
        self.assertEqual(24,23)
    def test4(self):             
        self.assertEqual(type(1),int)


if __name__ == '__main__':
    unittest.main()
    