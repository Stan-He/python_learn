
# -*- coding=UTF-8 -*-
from lxml import etree
from copy import deepcopy

dic={"key1":"meng.he"}

#定义根节点
root=etree.Element("root")
print etree.tostring(root,pretty_print=True)

#定义子节点
child1=etree.SubElement(root, "child1",shuxing="text")
child2=etree.SubElement(root, "child2")
child3=etree.SubElement(root, "child3")
child4=etree.SubElement(child2, "child4", attrib=dic)
print etree.tostring(root,pretty_print=True)

#列表式打印
for i in range(len(root)):
    print root[i].tag
    
for child in child2:
    print child.tag

#打印index
print root.index(child3)

#获取属性
child1.set("shuxing","text2")
print child1.get("shuxing")

#使用insert（）插入新的子节点
child2.insert(0,etree.Element("child5"))
print etree.tostring(root,pretty_print=True)

#拷贝xml
new_root=etree.Element("new_root")
new_root.append(deepcopy(child2))
print etree.tostring(new_root,pretty_print=True)

#父节点

print child2.getparent().tag


print "----------------操作元素-----------------------"
child3.text="No3 text"
print etree.tostring(root,pretty_print=True)
print etree.tostring(root,pretty_print=False)