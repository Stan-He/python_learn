import ctypes as ct
import binascii

#两种load so的方法
so1 = ct.cdll.LoadLibrary("/usr/local/lib/libnvme.so.1")
so2 = ct.CDLL("/usr/local/lib/libnvme.so.1")
print(so1)
print(so2)

###########C语言类型###############
#ctypes中的数据类型
print(ct.c_bool)
print(ct.c_char)
print(ct.c_uint)
#value
print(dir(ct.c_uint))
a=ct.c_uint(100)
#c_uint(100)
print(a)
#100
print(a.value)


a=ct.c_int(-100)
print(a.value)
a=ct.c_uint(-100)
#'0xffffff9c',4294967196 uint是4个字节
print(a.value)
a=ct.c_int(42949671965)
#溢出了 c_int(-995)
print(a)
a.value=-200
#c_int(-200)
print(a)

###########指针对象###############
#c_wchar_p 字符串 或者none
#c_char_p 字节传 或者none
#c_void_p int or none
s="Hello World"
c_s = ct.c_wchar_p(s)
#c_wchar_p(140263703964784)
#Hello World
print(c_s)
print(c_s.value)
c_s.value="new string"
#c_wchar_p(140263704134880)  内存地址被改变了
print(c_s)

##########create_string_buffer##########
buf = ct.create_string_buffer(5)
#5
print(ct.sizeof(buf))
#b'\x00\x00\x00\x00\x00'
print(buf.raw)

buf = ct.create_string_buffer(b'abcdefg')
print(ct.sizeof(buf))
#b'abcdefg\x00' 8个字节，包括一个结束字符
print(buf.raw)

buf = ct.create_string_buffer(b'abcdefg',size=7)
print(ct.sizeof(buf))
#b'abcdefg' 7个字节,size不能更短了
print(buf.raw)
print(buf.value)
#b'abc'
print(ct.string_at(buf,3))


#ctypes.Union

#ctypes.Structure
"""
1、structure必须继承自ct.Structure类
2、子类必须定义__fields__对象，是一个二元tuple的数组，代表name和类型
"""
class POINT(ct.Structure):
    _fields_ = [("x",ct.c_int),
                ("y",ct.c_int)]
p1=POINT(10,20)
#10,20
print(p1.x)
print(p1.y)
#8
print(ct.sizeof(p1))
#b'0a00000014000000'
print(binascii.hexlify((bytearray(p1))))
print(ct.addressof(p1))

#如果想紧凑，拒绝padding
class POINT2(ct.Structure):
    _pack_=1 #1byte 对齐
    _fields_ = [("a",ct.c_char),
                ("b",ct.c_char),
                ("c",ct.c_char),
                ("d",ct.c_int),
                ]
p2=POINT2(1,2,3,255)
#7 byte
print(ct.sizeof(p2))
#b'010203ff000000'
print(binascii.hexlify((bytearray(p2))))








