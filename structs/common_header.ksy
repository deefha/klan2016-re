meta:
  id: t_header
  endian: le
  encoding: ASCII

doc-ref: https://wiki.klan2016.cz/knihovny/spolecna-hlavicka.html

seq:
  - id: magic
    contents: 'SNOPSoft'
  - id: version
    type: u4
  - id: type
    type: u2
  - id: filesize
    type: u4
  - id: filetime
    type: u2
  - id: filedate
    type: u2
  - id: foo_1
    type: u4
  - id: foo_2
    type: u4
  - id: crc
    type: u2
