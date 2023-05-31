import ctypes as ct
import binascii

#ctypes.Structure
"""
1、structure必须继承自ct.Structure类
2、子类必须定义__fields__对象，是一个二元tuple的数组，代表name和类型
"""
class POINT(ct.Structure):
    _fields_ = [("x",ct.c_int),
                ("y",ct.c_int)]
p1=POINT(10,20)
#b'0a00000014000000'
print(binascii.hexlify((bytearray(p1))))
print(bytearray(p1))

p2 = POINT.from_buffer_copy(bytearray(p1))
print(p2.x)
print(p2.y)





