# -*- coding = UTF-8 -*-
from lxml import  etree 


input1="""<?xml version='1.0' encoding='GBK'?>
<LbsResult><KeywordRes><SEngineVersion>sp-alpha-0.2-release-20141023-4306</SEngineVersion><searchtime></searchtime><status>1</status><list><searchresult><list type="list"><poi><pguid><![CDATA[B000A83HSC]]></pguid><name><![CDATA[pingandajiejiayouzhan]]></name><ename><![CDATA[Ping'an Street Filling Station]]></ename><address><![CDATA[address]]></address><eaddress><![CDATA[Di'anmen West Street Jiaochangkou Hutong No.26]]></eaddress><typecode><![CDATA[010101]]></typecode><x><![CDATA[116.386709]]></x><y><![CDATA[39.932896]]></y><x_entr><![CDATA[116.386328]]></x_entr><y_entr><![CDATA[39.933145]]></y_entr><x_exit><![CDATA[]]></x_exit><y_exit><![CDATA[]]></y_exit></poi><poi><pguid><![CDATA[B0FFFAIW7Z]]></pguid><name><![CDATA[jiayouzhan]]></name><ename><![CDATA[Filling Station]]></ename><address><![CDATA[jingshanhoujie7hao]]></address><eaddress><![CDATA[Jingshan Back Street No.7]]></eaddress><typecode><![CDATA[010101]]></typecode><x><![CDATA[116.397444]]></x><y><![CDATA[39.928587]]></y><x_entr><![CDATA[]]></x_entr><y_entr><![CDATA[]]></y_entr><x_exit><![CDATA[]]></x_exit><y_exit><![CDATA[]]></y_exit></poi></list></searchresult></list></KeywordRes></LbsResult>
"""
#print input1
root=etree.fromstring(input1)
#print etree.tostring(root,pretty_print=True)
print etree.tostring(root,pretty_print=False)
print etree.tostring(root,pretty_print=True)