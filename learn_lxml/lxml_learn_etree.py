#-*- coding=UTF-8
#import 一个可用的etree，lxml中默认就有etree
try:
    from lxml import etree
    print("running with lxml.etree")
except ImportError:
    try:
        import xml.etree.cElementTree as etree
        print ("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            import xml.etree.ElementTree as etree
            print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                import elementtree.ElementTree as etree
                print ("running with ElementTree")
            except ImportError:
                print("Failed to import ElementTree form any known place")
from io import BytesIO
#创建一个根对象
root=etree.Element("root")
print root.tag

#创建一个子对象，附属于root
root.append(etree.Element("child1"))

#更加便捷的工厂函数
child2=etree.SubElement(root, "child2")
child3=etree.SubElement(root, "child3")

#element同时也是list
#获取child1对象
child1=root[0]
print child1.tag
print len(root)
print root.index(child3)
for child in root:
    print child.tag
#在指定index插入一个元素
root.insert(0, etree.Element("child0"))

#和列表一样可以分片
start=root[:1]
end=root[-1:]
print start[0].tag
print end[0].tag

#判断元素是否有子元素,判断是否是一个元素
if len(root):
    print "root has children"
if etree.iselement(child3):
    print "child3 is an element"
    
#每一个元素都有一个parent
if root is child3.getparent():
    print "child3 has parent root"

#拷贝xml时，需要使用深拷贝来拷贝etree,拷贝root下的child1到new下
from copy import deepcopy
child1.append(etree.Element("child4"))
element=etree.Element("new")
element.append(deepcopy(root[1]))
print etree.tostring(element,pretty_print=True)

#邻居关系
if child1 is child2.getprevious():
    print "child1 is child2's  previous"
if child3 is child2.getnext():
    print "child3 is child2's  next"

#添加元素的属性
root.set("interesting", "totally")
root.set("hello", "world")
print root.get("interesting")
print root.keys()
for key,value in root.items():
    print "%s==%s" % (key,value)

#处理tag的属性可以将其赋值给一个dic对象
attributes=root.attrib
print attributes.items()

#也可以赋值给一个独立的dic对象，这样操作就不会影响root的属性
a=dict(root.attrib)
a["add"]="two"
print root.attrib.items()
print a.items()

print "----------------完整的etree-----------------------"
print etree.tostring(root,pretty_print=True)



print "-------------元素的text----------------"
#元素的text
root = etree.Element("root")
root.text="a text"

#html的br处理
html=etree.Element("html")
body=etree.SubElement(html,"body")
body.text= "TEXT"
br=etree.SubElement(body, "br")
br.tail="a tail"
print etree.tostring(html,pretty_print=True)
print etree.tostring(html,method="text")

print "--------------使用XPath查找text-----------------------"

input1="""<?xml version='1.0' encoding='UTF-8'?>
<LbsResult><KeywordRes><SEngineVersion>sp-alpha-0.2-release-20141023-4306</SEngineVersion><searchtime></searchtime><status>1</status><list><searchresult><list type="list"><poi><pguid><![CDATA[B000A83HSC]]></pguid><name><![CDATA[平安大街加油站]]></name><ename><![CDATA[Ping'an Street Filling Station]]></ename><address><![CDATA[address]]></address><eaddress><![CDATA[Di'anmen West Street Jiaochangkou Hutong No.26]]></eaddress><typecode><![CDATA[010101]]></typecode><x><![CDATA[116.386709]]></x><y><![CDATA[39.932896]]></y><x_entr><![CDATA[116.386328]]></x_entr><y_entr><![CDATA[39.933145]]></y_entr><x_exit><![CDATA[]]></x_exit><y_exit><![CDATA[]]></y_exit></poi><poi><pguid><![CDATA[B0FFFAIW7Z]]></pguid><name><![CDATA[加油站]]></name><ename><![CDATA[Filling Station]]></ename><address><![CDATA[景山后街7号]]></address><eaddress><![CDATA[Jingshan Back Street No.7]]></eaddress><typecode><![CDATA[010101]]></typecode><x><![CDATA[116.397444]]></x><y><![CDATA[39.928587]]></y><x_entr><![CDATA[]]></x_entr><y_entr><![CDATA[]]></y_entr><x_exit><![CDATA[]]></x_exit><y_exit><![CDATA[]]></y_exit></poi></list></searchresult></list></KeywordRes></LbsResult>
"""
root=etree.fromstring(input1)
print etree.tostring(root,pretty_print=True)
print root.xpath("/LbsResult/KeywordRes/list/searchresult/list/poi[2]")
poi_list=root.xpath("/LbsResult/KeywordRes/list/searchresult/list/poi")
for i in poi_list:
    x1=i.xpath("./address")
    x2=i.xpath("./pguid")
    x3=i.xpath("./name")
    print x2[0].text,x3[0].text,x1[0].text

#选取所有poi的name元素，保存在namelist中
name_list=root.xpath("/LbsResult/KeywordRes/list/searchresult/list//poi/name")
for i in name_list:
    print i.text


print "-----------------------Tree iteration-------------------------"

root=etree.Element("root")
etree.SubElement(root, "child").text="child1"
etree.SubElement(root, "child").text="child2"
etree.SubElement(root, "another").text="child3"

for element in root.iter("child"):
    print "%s--%s" % (element.tag,element.text)

print "-----------------------Serialisation--------------------------"
root = etree.XML('<root><a><b/></a></root>')
print etree.tostring(root)
#加入xml声明
print etree.tostring(root, xml_declaration=True)
print etree.tostring(root, encoding='UTF-8',xml_declaration=True)

root = etree.XML('<html><head/><body><p>Hello<br/>World</p></body></html>')
print etree.tostring(root, method='html',pretty_print=True)
#输出纯文本,如果纯文本中 有中文，需要指定encoding='unicode'
print etree.tostring(root, method='text',pretty_print=True)

print "-----------------------Parsing from strings and files------------------"
some_xml_data="""<?xml version='1.0' encoding='UTF-8'?>
<LbsResult><KeywordRes><SEngineVersion>sp-alpha-0.2-release-20141023-4306</SEngineVersion><searchtime></searchtime><status>1</status><list><searchresult><list type="list"><poi><pguid><![CDATA[B000A83HSC]]></pguid><name><![CDATA[平安大街加油站]]></name><ename><![CDATA[Ping'an Street Filling Station]]></ename><address><![CDATA[address]]></address><eaddress><![CDATA[Di'anmen West Street Jiaochangkou Hutong No.26]]></eaddress><typecode><![CDATA[010101]]></typecode><x><![CDATA[116.386709]]></x><y><![CDATA[39.932896]]></y><x_entr><![CDATA[116.386328]]></x_entr><y_entr><![CDATA[39.933145]]></y_entr><x_exit><![CDATA[]]></x_exit><y_exit><![CDATA[]]></y_exit></poi><poi><pguid><![CDATA[B0FFFAIW7Z]]></pguid><name><![CDATA[加油站]]></name><ename><![CDATA[Filling Station]]></ename><address><![CDATA[景山后街7号]]></address><eaddress><![CDATA[Jingshan Back Street No.7]]></eaddress><typecode><![CDATA[010101]]></typecode><x><![CDATA[116.397444]]></x><y><![CDATA[39.928587]]></y><x_entr><![CDATA[]]></x_entr><y_entr><![CDATA[]]></y_entr><x_exit><![CDATA[]]></x_exit><y_exit><![CDATA[]]></y_exit></poi></list></searchresult></list></KeywordRes></LbsResult>
"""
root=etree.fromstring(some_xml_data)
print root.tag
print etree.tostring(root)

#用bytesio来包装字符串,也可以直接打开一个文件
some_file_like_object=BytesIO(some_xml_data)
#parse函数返回一个tree对象
tree=etree.parse(some_file_like_object)
print etree.tostring(tree)
#tree.getroot()返回一个根节元素对象
root = tree.getroot()
print root.tag
print etree.tostring(root)

print "-----------------------parser objects----------------------------"

#修改解析器的参数
parser=etree.XMLParser(remove_blank_text=True)
root=etree.XML("<root>  <a/>   <b>  </b>     </root>", parser)
print etree.tostring(root)

#遍历子节点，移除子节点中的空格
for element in root.iter("*"):
    if element.text is not None and not element.text.strip():
        element.text=None
print etree.tostring(root)

print "-----------------------Incremental parsing-----------------------"
class DataSource:
    data = [ b"<roo", b"t><", b"a/", b"><", b"/root>" ]
    def read(self,requested_size):
        try:
            return self.data.pop(0)
        except IndexError:
            return b''

tree=etree.parse(DataSource())
print etree.tostring(tree)

print "------------------------elementPath-------------------------------"
some_xml_data="""<?xml version='1.0' encoding='UTF-8'?>
<LbsResult><KeywordRes><SEngineVersion>sp-alpha-0.2-release-20141023-4306</SEngineVersion><searchtime></searchtime><status>1</status><list><searchresult><list type="list"><poi><pguid><![CDATA[B000A83HSC]]></pguid><name><![CDATA[平安大街加油站]]></name><ename><![CDATA[Ping'an Street Filling Station]]></ename><address><![CDATA[address]]></address><eaddress><![CDATA[Di'anmen West Street Jiaochangkou Hutong No.26]]></eaddress><typecode><![CDATA[010101]]></typecode><x><![CDATA[116.386709]]></x><y><![CDATA[39.932896]]></y><x_entr><![CDATA[116.386328]]></x_entr><y_entr><![CDATA[39.933145]]></y_entr><x_exit><![CDATA[]]></x_exit><y_exit><![CDATA[]]></y_exit></poi><poi><pguid><![CDATA[B0FFFAIW7Z]]></pguid><name><![CDATA[加油站]]></name><ename><![CDATA[Filling Station]]></ename><address><![CDATA[景山后街7号]]></address><eaddress><![CDATA[Jingshan Back Street No.7]]></eaddress><typecode><![CDATA[010101]]></typecode><x><![CDATA[116.397444]]></x><y><![CDATA[39.928587]]></y><x_entr><![CDATA[]]></x_entr><y_entr><![CDATA[]]></y_entr><x_exit><![CDATA[]]></x_exit><y_exit><![CDATA[]]></y_exit></poi></list></searchresult></list></KeywordRes></LbsResult>
"""
root=etree.fromstring(some_xml_data)
#获得tree对象
tree=etree.ElementTree(root)
#打印name的path
name_list=root.xpath("/LbsResult/KeywordRes/list/searchresult/list//poi/name")
for name in name_list:
    print tree.getelementpath(name)

#获得一个poi列表下，所有poi名字的迭代器
a=root.iterfind("./KeywordRes/list/searchresult/list//poi/name")
print next(a).text
print next(a).text