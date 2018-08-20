import usb.core
import usb.util
import time
import struct
import sys
from PIL import Image


class d600Printer():
  dev     = None
  bulkin  = None
  bulkout = None

  def __init__(self):
    if self.dev == None:
      self.dev = usb.core.find(idVendor= 0x04f9,idProduct=0x2074)
      #Detatch any other driver trying to use this devic (usblp..)
      try:
        self.dev.detach_kernel_driver(0)
      except:
          pass

    if self.dev == None:
      print("Cound not find USB Printer!")
      raise usb.core.USBError(0,0)
    self.dev.set_configuration()
    cfg = self.dev.get_active_configuration()
    intf = cfg[(0,0)]
    self.bulkout = usb.util.find_descriptor(
        intf,
        # match the first OUT endpoint
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_OUT)
    self.bulkin = usb.util.find_descriptor(
        intf,
        # match the first OUT endpoint
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_IN)
    if self.bulkout == None:
      print("Could not find a bulk-out endpoint")
    if self.bulkin == None:
      print("Could not find a bulk-in endpoint")

  def command_null(self,repeat = 100):
    cmd = [0x0] * 100
    phex(cmd)
    self.bulkout.write(cmd)

  def command_init(self):
    cmd = [0x1b,0x40]
    phex(cmd)
    self.bulkout.write(cmd)

  def command_request_status_info(self):
    cmd = [0x1B, 0x69, 0x53]
    phex(cmd)
    self.bulkout.write(cmd)
    time.sleep(0.1)
    return self.bulkin.read(32,5000)

  def command_switch_mode(self,mode = 0x01):
    cmd = struct.pack("BBBB",0x1b,0x69,0x61, mode )
    phex(cmd)
    self.bulkout.write(cmd)

  # 0x1b 0x69 0x7a 0x0 0x0 0xc 0x0 0x8f 0x0 0x0 0x0 0x0 0x0 
  def command_set_print_information(self, paperwidth,paperlength,rasternumber, validflag = 0x00,papertype = 0x00, startingpage = 0x00):
    #print rasternumber
    cmd = struct.pack("=BBBBBBBIBB",0x1b, 0x69, 0x7a, validflag, papertype, paperwidth, paperlength, rasternumber,startingpage,0x00)
    phex (cmd)
    self.bulkout.write(cmd)

  def command_set_autocut(self,cut):
    bv  = 0x00
    if cut:
      bv = 0x40
    cmd = struct.pack("BBBB",0x1b, 0x69, 0x4d, bv )
    phex(cmd)
    self.bulkout.write(cmd)

  def command_set_expanded_mode(self, cut_at_end = True, high_rez_printing = False):
    bv = 0x00
    if cut_at_end:
      bv |= 0x08
    if high_rez_printing:
      bv |= 0x20
    cmd = struct.pack("BBBB",0x1b, 0x69, 0x4b, bv )
    phex(cmd)
    self.bulkout.write(cmd)
  # 0x47   0x10 0x0   0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0
  def command_send_graphics(self, graphics):
    command = [0x4d, 0x00]
    for line in graphics:
      command += [0x47, 0x10, 00] + line
    command += [0x1a]
    phex(command)
    self.bulkout.write(command)
    # 128 dots per line.  16 bytes  

  def printimage(self,image):
    self.command_null()
    self.command_init()
    data = self.command_request_status_info()
    #print(data)
    self.command_switch_mode(0x01)
    self.command_set_print_information(paperwidth = 24,paperlength = 0, rasternumber = len(image) )
    self.bulkout.write([0x1b, 0x69 ,0x55, 0x4a, 0x0, 0xc, 0x0, 0x10, 0x18, 0x5c, 0x9d, 0x55, 0x0 ,0x0 ,0xb ,0x0 ,0x0 ,0x0])
    self.command_set_autocut(True)
    self.command_set_expanded_mode(cut_at_end = True)
    self.bulkout.write([0x1B ,0x69 ,0x64 ,0x0E ,0x00])
    self.command_send_graphics(image)

  


def phex(d):
  for c in d:
    try:
      print hex(c),
    except:
      print hex(ord(c)),
  print


img = Image.open( sys.argv[1] )
img = img.convert('1')
px = img.load()


if (img.size[1] != 128) and (img.size[1] != 64):
  print("image size of '%d' is not 128 or 64"%img.size[1])

im=[]
for y in range(img.size[0]):
  line = [0]*16
  if img.size[1] == 64:
    for x in range(32,96):
      bit  = x%8
      mask = 0x80>>bit
      byte = x/8
      if px[y,x-32]==0:
        line[byte] |= mask
  else:
    for x in range(128):
      bit  = x%8
      mask = 0x80>>bit
      byte = x/8
      if px[y,x]==0:
        line[byte] |= mask
  im += [line]

p = d600Printer()

#convert -size x64 -font Clear-Sans-Bold label:"A quick brown fox jumped over a lazy dog\nA quick brown fox jumped over a lazy dog" +dither -monochrome fox-64.bmp
#print 
#for line in im:
#  print line
p.printimage(im)



