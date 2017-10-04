meta:
  id: klan_font
  file-extension: lib
  title: KLAN font library
  application: KLAN discmag engine
  endian: le
  encoding: ASCII
  ks-version: 0.7
  imports:
    - common_header
doc-ref: https://wiki.klan2016.cz/knihovny/fonty.html
seq:
  - id: header
    type: t_header
  - id: fat
    type: m_fat
types:
  m_fat:
    seq:
      - id: count
        type: u4
      - id: foo_1
        size: 16
      - id: offsets
        type: m_offset
        repeat: expr
        repeat-expr: 59
  m_offset:
    seq:
      - id: offset
        type: u4
    instances:
      font:
        pos: offset
        type: m_font
        if: offset != 0
  m_font:
    seq:
      - id: datalength
        type: u4
      - id: height
        type: u4
      - id: palette
        type: m_palette
      - id: characters
        type: m_characters
  m_palette:
    seq:
      - id: color
        type: m_color
        repeat: expr
        repeat-expr: 256
  m_color:
    seq:
      - id: r
        type: u1
      - id: g
        type: u1
      - id: b
        type: u1
  m_characters:
    seq:
      - id: characters
        type: m_character
        repeat: expr
        repeat-expr: 256
  m_character:
    seq:
      - id: offset_and_width
        type: u4
    instances:
      offset:
        value: offset_and_width & 0xffffff
      width:
        value: offset_and_width >> 0x18
      data:
        pos: offset + _parent._parent._parent.offset + 8 + 768 + 1024
        type: m_data
        if: width != 0
  m_data:
    seq:
      - id: rows
        size: _parent.width
        repeat: expr
        repeat-expr: _parent._parent._parent.height
