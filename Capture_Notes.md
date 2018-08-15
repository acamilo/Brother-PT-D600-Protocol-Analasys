## Capture ##

 - Device has a bulk in and bulk out endpoint.
 - Packets contain a stream of bytes
 - Every command starts with an escape sequence of `1B`
    - Not true, Raster data starts with '4D'
 - First BULK_OUT packet contains 100 bytes of `00`
 - packets can contain multiple commands
 - Most of the devices in the PTouch family seem to use a common protocol.
 - Found additional documentation for some of the commands (Raster mode)
 ### Raster Data Notes ###
`4d 02` is tiff mode but we're using `4d 00`
 There seems to be a repeating structure 47 10 followed by 17 bytes
 first one starts right after `4d 00`
 This is raw pixel data. Script can unpack it.
 
## Reference Documents ##
  Usefull Documents ive been referencing.
  
 - [QL550LabelPrinter Notes](http://etc.nkadesign.com/Printers/QL550LabelPrinter)
 - [QL Series Command Reference CR](http://download.brother.com/welcome/docp000678/cv_qlseries_eng_raster_600.pdf)
 - [libptouch](https://bitbucket.org/philpem/libptouch)
 - [Raster Commands Set RCS](http://download.brother.com/welcome/docp000771/cv_pth500p700e500_eng_raster_110.pdf)
 


## Command Log ##
| pcap packet| Command | Decode |
| --- | --- | --- |
| 1 | `00 .. 99 bytes` | invalidate command RCS P.5 |
| 2 | `1B 40` | Init Command CR P.18|
| 3 | `1B 69 53` | Status Information Reqest CR P.18 |
| 15 | device sends status info | |
| 16 | `1B 69 61 01` | specify Raster Mode `01` CR P.18 |
| 16 | `1B 69 55 .. 17 bytes` | Unknown Command |
| 16 | `1B 69 7a .. 12 bytes` | Send Print Information RCS P.5 |
| 16 | `1B 69 4d 40` | Unknown Command |
| 16 | `1B 69 4b 08` | Chain Printing Disabled |
| 16 | `1B 69 64 0E 00 ` | Set 2mm margins |
| 16 | `4D 00 .. # a lot | Set compression mode and send graphics? |
| 25 | 32b response | |
| 27739 | 32b response | |
| 5290 | 32b response | |
| 5291 | 32b response | |
