from pcapng import FileScanner

def parse(data):
  cut = 20
  if len(data) ==0:
    return
  while len(data) != 0:
    b = data.pop(0)
    if  b==0x1b:
      print "[%s] (" % '{:02x}'.format(b) ,
      c = 0
      while True:
        if len(data)>0 and data[0] != 0x1b:
          b = data.pop(0)
          if c<cut:
            print "%s" % '{:02x}'.format(b) ,
          c +=1
        else:
          if c<cut:
            print ")"
          else:
            print  " .. #%d )" % c 
          break


with open('print-label-capture.pcapng') as fp:
  scanner = FileScanner(fp)
  for block in scanner:
    try:
      block = bytearray(block.packet_data)
      parse(block[27:])
    except AttributeError:
      pass #print block
