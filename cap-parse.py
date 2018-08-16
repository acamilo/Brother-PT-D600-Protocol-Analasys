from pcapng import FileScanner
import sys 
graphic = []

# take a packet and extract commands.
# commands start with 0x1b
def parse(data):
  packets = None
  packet = []
  if len(data) ==0:
    return
  while len(data) != 0:
    b = data.pop(0)
    if  b==0x1b: # escape char, command.
      if packets == None:
        packets = []
      packet += [b]
      try:
        while data[0] != 0x1b:
          # read untill next escape char
          # pushing command to its own array
          packet += [data.pop(0)]
      except IndexError:
          pass
        # add it to packets and refresh for next packet
      packets += [packet]
      packet = []
  return packets

def extractPicture(command):
    lines = []
    # seek to beginning of pixel data
    while command[0:2] != [0x4d, 0x00]:
      command.pop(0)
    command.pop(0)
    command.pop(0)
    print "aligned with image"
    # read off image lines
    while len(command) != 0:
      c = command.pop(0)
      if c == 0x47:
        lines += [command[0:18]]
    # return lines
    print "Read %d lines!" % len(lines)
    return lines

    
def displayImage(lines):
  ascii = "|"
  l = "|"
  for p in lines[0]:
    l += "I....... "
  print l+"|"
  for line in lines:
    for pixel in line:
      ascii += format(pixel, '08b').strip().replace('0',' ').replace('1',chr(219))+"."
    ascii += "|\n|"
  print ascii
  


with open(sys.argv[1]) as fp:
  stream = bytearray("")
  print fp
  scanner = FileScanner(fp)
  for block in scanner:
    try:
      block = bytearray(block.packet_data)
      #strip off USB stuff
      stream += block[27:]
    except AttributeError:
      pass 

  # work with bytearray stream

  print len(stream)
  commands = parse(stream)

  for c in commands:
    print c[0:40],
    if len(c)>40:
      print "..(%d)" % len(c)
    else:
      print ""
    if c[0:3] == [27, 105, 100]:
      print "Found Bitmap Data"
      pixels = extractPicture(c)
      displayImage( pixels)
