import usb.core
import usb.util

dev = usb.core.find(idVendor= 0x0000,idProduct=0x0000)

if dev is None:
  raise ValueError('device not found')

dev.set_configuration()
intf = cfg[(0,0)]
  
print intf