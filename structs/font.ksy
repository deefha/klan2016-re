meta:
  id: klan_font
  file-extension: lib
  title: KLAN font library
  application: KLAN discmag engine
  endian: le
  encoding: ASCII
  imports:
    - common_header

doc-ref: https://wiki.klan2016.cz/knihovny/fonty.html

seq:
  - id: header
    type: t_header
  - id: fat
    type: t_fat

instances:
  fonts:
    pos: fat.offsets[_index]
    type: t_font(fat.offsets[_index])
    if: fat.offsets[_index] != 0
    repeat: expr
    repeat-expr: 63

types:
  t_fat:
    seq:
      - id: count
        type: u4
      - id: offsets
        type: u4
        repeat: expr
        repeat-expr: 63

  t_font:
    params:
      - id: offset
        type: u4
    seq:
      - id: datalength
        type: u4
      - id: height
        type: u4
#      - id: colors
#        type: t_color
#        repeat: expr
#        repeat-expr: 256
      - id: colormap
        size: 768
      - id: characters
        type: t_character
        repeat: expr
        repeat-expr: 256
    instances:
      matrices:
        pos: offset + 8 + 768 + 1024 + characters[_index].offset
#        type: t_matrix(characters[_index].width, height)
        size: characters[_index].width * height
        if: characters[_index].width != 0
        repeat: expr
        repeat-expr: 256

#  t_color:
#    seq:
#      - id: r
#        type: u1
#      - id: g
#        type: u1
#      - id: b
#        type: u1

  t_character:
    seq:
      - id: offset_and_width
        type: u4
    instances:
      offset:
        value: offset_and_width & 0xffffff
      width:
        value: offset_and_width >> 0x18

#  t_matrix:
#    params:
#      - id: width
#        type: u4
#      - id: height
#        type: u4
#    seq:
#      - id: rows
#        type: t_row(width)
#        repeat: expr
#        repeat-expr: height

#  t_row:
#    params:
#      - id: width
#        type: u4
#    seq:
#      - id: columns
#        type: u1
#        repeat: expr
#        repeat-expr: width
