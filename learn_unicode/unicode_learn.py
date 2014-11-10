# encoding=UTF-8
import sys

#python默认使用ascii编码
print sys.getdefaultencoding()
a='s'
print a
print "a的编码为：%s" % repr(a)
print "-------------------------"

#如果是非字母，那么python会使用脚本开头指定的coding来选择编码，这里使用的是UTF-8
b='汉'
print b         #在windows命令行模式下回出现乱码
print type(b)   #utf8编码的字符为str类型
print "b的编码为：%s" % repr(b)
print "-------------------------"

#定义unicode，输出时，会自动的转换为当前系统适应的编码（推荐，不容易出错）
c=u'我'
print c
print type(c)
print "c的编码为：%s" % repr(c)
print "-------------------------"

#使用unicode函数转码输出
d='哈哈'          #UTF-8
print unicode(d,'utf-8')   #以unicode方式输出
print "-------------------------"

#UTF-8和gbk转码，通过unicode中转
e='呵呵'          #UTF-8
f=e.decode('UTF-8').encode('gbk')  #UTF-8先转码为unicode，再转码为gbk
print f
print type(f)
print "e的编码为：%s" % repr(e)
print "f的编码为：%s" % repr(f)
print "-------------------------"

#使用codecs提供的open函数，打开文件后自动转码为unicode
import codecs
g = codecs.open('test.txt', encoding='UTF-8')
h = g.read()
print type(h)
print h.encode("UTF-8")
print "----"
x=open('test.txt')
z=x.readline()
print "z的编码为：%s" % repr(z)
print z
#print "".join(x.readlines())
print "h的编码为：%s" % repr(h)    #打开的文本前，有两个byte的bom，FEFF说明是big endian

#python对字符串的理解，有可能作为字节流，也有可能理解为文本字符的组合
#字节流：6个byte
str1="中国"
for i in str1:
    print repr(i)
#文本字符：每个字符两个byte
str2=u"中国"
for i in str2:
    print repr(i)
    
#编码检测，检测字符串是用的哪种编码
import chardet
uni=u"中华人民共和国"
s_utf=uni.encode('UTF-8')
s_gbk=uni.encode('gbk')
print chardet.detect(s_utf)
print chardet.detect(s_gbk)

#调查1.text
f=open("1.txt","r")
re=f.readline()
print re
f.close()