## Capture ##

 - Device has a bulk in and bulk out endpoint.
 - Packets contain a stream of bytes
 - Every command starts with an escape sequence of `1B`
 - First BULK_OUT packet contains 100 bytes of `00`
 - packets can contain multiple commands
 - Most of the devices in the PTouch family seem to use a common protocol.
 
## Reference Documents ##
  Usefull Documents ive been referencing.
  
 - [QL550LabelPrinter Notes](http://etc.nkadesign.com/Printers/QL550LabelPrinter)
 - [QL Series Command Reference CR](http://download.brother.com/welcome/docp000678/cv_qlseries_eng_raster_600.pdf)
 - [libptouch](https://bitbucket.org/philpem/libptouch)


## Command List ##
| Command | Decode |
| `1B 40` | Init Command CR P.18|
| `1B 69 53` | Status Information Reqest CR P.18 |
| device sends status info | |
| `1B 69 61 01` | specify Raster Mode `01` CR P.18 |
| `1B 69 55 .. 17 bytes` | Unknown Command |
| `1B 69 7a .. 12 bytes` | Unknown Command |
| `1B 69 4d 40` | Unknown Command |
| `1B 69 4b 08` | Unknown Command |
| `1B 69 64 .. 2724 bytes` | Unknown Command |
