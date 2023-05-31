import serial
import serial.tools.list_ports
import sys
import time
import binascii
from ctypes import Structure,c_ubyte,c_char


class MI_HSC(Structure):
    _pack_=1
    _fields_=[
            ('byte0',c_ubyte),
            ('byte1',c_ubyte),
            ('byte2',c_ubyte),
            ('byte3',c_ubyte),
            ('byte4',c_ubyte),
            ('byte5',c_ubyte),
            ('byte6',c_ubyte),
            ('byte7',c_ubyte),
            ]

def find_device():
    comports  = serial.tools.list_ports.comports()
    for usbdevice in comports:
        vid = usbdevice.vid
        pid = usbdevice.pid
        print("vid")
        print("pid")
        print(usbdevice.device)
        if (pid==394 and vid==10473):
            print(usbdevice)
            if "HSC" in usbdevice.product and "Starblaze" in usbdevice.manufacturer:
                HSC_VER=usbdevice.product
                print(f"HSC Detected vid={hex(vid)} pid={hex(pid)} device={usbdevice.device} product={usbdevice.product} manufacturer={usbdevice.manufacturer}")
                return usbdevice.device
    return None

device = find_device()
if device:
    hsc = serial.Serial(device, 9600, timeout=5)
else:
    print("found no device")
    sys.exit(-1)

def mi_cmd_send(hsc,data):
    hsc.write(bytearray(data))
    while True:
        res = hsc.read(8)
        if len(res):
            return res
        else:
            print('waiting...')
            time.sleep(1)

req = MI_HSC(   byte0=0xfd,
                byte1=0x01,
                byte2=0x00, #len=0
                byte3=0x00, #不需要等返回，后续data不包含i2c-header
                byte4=0x00, #retcode
                byte5=0x00, #rsvd
                byte6=0x00, #rsvd
                byte7=0x00, 
                )
print(req.byte0)
print(req.byte1)
print(binascii.hexlify((bytearray(req))))
print(bytearray(req))

resp = MI_HSC.from_buffer_copy(mi_cmd_send(hsc=hsc,data=bytearray(req)))
print('-----response-----')
print(binascii.hexlify((bytearray(resp))))
print(resp.byte4)
