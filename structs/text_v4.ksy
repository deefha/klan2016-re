meta:
  id: klan_text_v4
  file-extension: lib
  title: KLAN text library v4
  application: KLAN discmag engine
  endian: le
  encoding: ASCII
  imports:
    - common_macros_v2

doc-ref: https://wiki.klan2016.cz/knihovny/texty.html

instances:
  offset_linktable:
    pos: _io.size - 4
    type: u4
  count_linktable:
    pos: _io.size - 8
    type: u4
  offset_linktable_meta:
    value: _io.size - 8 - (20 * count_linktable)
  linktable_meta:
    type: t_linktable_meta(offset_linktable_meta + 20 * _index)
    repeat: expr
    repeat-expr: count_linktable
    if: count_linktable != 0
  linktable:
    type:
      switch-on: _index
      cases:
        (count_linktable - 1): t_linktable(linktable_meta[_index].content.offset, offset_linktable_meta - linktable_meta[_index].content.offset)
        _: t_linktable(linktable_meta[_index].content.offset, linktable_meta[_index + 1].content.offset - linktable_meta[_index].content.offset)
    repeat: expr
    repeat-expr: count_linktable
    if: count_linktable != 0
  count_linetable_meta:
    pos: offset_linktable - 52
    type: u4
  offset_linetable_meta:
    value: offset_linktable - 52 - (count_linetable_meta * 17) - 17
  linetable_meta:
    type: t_linetable_meta(offset_linetable_meta + 17 * _index)
    repeat: expr
    repeat-expr: count_linetable_meta
    if: count_linetable_meta != 0
  count_palettetable:
    pos: offset_linetable_meta - 1
    type: u1
  offset_palettetable:
    value: offset_linetable_meta - 1 - (count_palettetable * 768)
  palettetable:
    type: t_palettetable(offset_palettetable + 768 * _index)
    repeat: expr
    repeat-expr: count_palettetable
    if: count_palettetable != 0
  linetable:
    type:
      switch-on: _index
      cases:
        (count_linetable_meta - 1): t_linetable(linetable_meta[_index].content.offset, offset_palettetable - linetable_meta[_index].content.offset)
        _: t_linetable(linetable_meta[_index].content.offset, linetable_meta[_index + 1].content.offset - linetable_meta[_index].content.offset)
    repeat: expr
    repeat-expr: count_linetable_meta
    if: count_linetable_meta != 0
  title:
    pos: 0
    size: 256

types:
  t_linktable_meta:
    params:
      - id: param_offset
        type: u4
    instances:
      content:
        type: t_linktable_meta_content
        pos: param_offset

  t_linktable_meta_content:
    seq:
      - id: topleft_x
        type: u4
      - id: topleft_y
        type: u4
      - id: bottomright_x
        type: u4
      - id: bottomright_y
        type: u4
      - id: offset
        type: u4

  t_linktable:
    params:
      - id: param_offset
        type: u4
      - id: param_length
        type: u4
    instances:
      content:
        type: t_linktable_content
        pos: param_offset
        size: param_length

  t_linktable_content:
    seq:
      - id: macros
        type: t_macros_v2
        repeat: until
        repeat-until: _.type == 0x00f0 or _.type == 0x414d or _.type == 0xc0ff or _.type == 0xffff

  t_linetable_meta:
    params:
      - id: param_offset
        type: u4
    instances:
      content:
        type: t_linetable_meta_content
        pos: param_offset

  t_linetable_meta_content:
    seq:
      - id: offset
        type: u4
      - id: height
        type: u1
      - id: top
        type: u2
      - id: foo
        size: 10

  t_palettetable:
    params:
      - id: param_offset
        type: u4
    instances:
      content:
        size: 768
        pos: param_offset

  t_linetable:
    params:
      - id: param_offset
        type: u4
      - id: param_length
        type: u4
    instances:
      content:
        type: t_linetable_content
        pos: param_offset
        size: param_length

  t_linetable_content:
    seq:
      - id: pieces
        type: t_linetable_content_piece
        repeat: eos

  t_linetable_content_piece:
    seq:
      - id: raw
        type: u1
      - id: data
        type:
          switch-on: raw
          cases:
            1: t_linetable_content_piece_1
            8: t_linetable_content_piece_8
            9: t_linetable_content_piece_9
            32: t_linetable_content_piece_32
        if: raw == 1 or raw == 8 or raw == 9 or raw == 32

  # font
  t_linetable_content_piece_1:
    seq:
      - id: mode
        type: u1

  # obrazek
  t_linetable_content_piece_8:
    seq:
      - id: table
        type: u1
      - id: width
        type: u2
      - id: height
        type: u1
      - id: rows
        type: t_linetable_content_piece_8_row
        repeat: expr
        repeat-expr: height
        if: height != 0

  t_linetable_content_piece_8_row:
    seq:
      - id: content
        type: t_linetable_content_piece_8_row_data
        repeat: until
        repeat-until: _.data == 192

  t_linetable_content_piece_8_row_data:
    seq:
      - id: data
        type: u1
      - id: addon
        type: u1
        if: data > 192

  # odkaz
  t_linetable_content_piece_9:
    seq:
      - id: id
        type: u2

  # mezera
  t_linetable_content_piece_32:
    seq:
      - id: length
        type: u1
