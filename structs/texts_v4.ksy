meta:
  id: klan_texts_v4
  file-extension: lib
  title: KLAN texts library v4
  application: KLAN discmag engine
  endian: le
  encoding: ASCII
  imports:
    - common_header

doc-ref: https://wiki.klan2016.cz/knihovny/texty.html

seq:
  - id: header
    type: t_header
  - id: fat
    type: t_fat
  - id: data
    type: t_data

types:
  t_fat:
    seq:
      - id: count
        type: u2
      - id: offsets
        type: t_fat_offset
        repeat: expr
        repeat-expr: 500

  t_fat_offset:
    seq:
      - id: name
        size: 9
      - id: offset_1
        type: u4
      - id: offset_2
        type: u4
      - id: offset_3
        type: u4
      - id: offset_4
        type: u4

  t_data:
    instances:
      texts:
        type: t_text(_parent.fat.offsets[_index].offset_1, _parent.fat.offsets[_index].offset_2, _parent.fat.offsets[_index].offset_3, _parent.fat.offsets[_index].offset_4)
        repeat: expr
        repeat-expr: 500

  t_text:
    params:
      - id: param_offset_1
        type: u4
      - id: param_offset_2
        type: u4
      - id: param_offset_3
        type: u4
      - id: param_offset_4
        type: u4
    instances:
      variants:
        type:
          switch-on: _index
          cases:
            0: t_text_variant_full(param_offset_1, param_offset_2 - param_offset_1)
            1: t_text_variant_full(param_offset_2, param_offset_3 - param_offset_2)
            2: t_text_variant_plain(param_offset_3, param_offset_4 - param_offset_3)
        repeat: expr
        repeat-expr: 3

  t_text_variant_full:
    params:
      - id: param_offset
        type: u4
      - id: param_length
        type: u4
    instances:
      content:
        type: t_text_content_full
        pos: param_offset
        size: param_length
        if: param_offset != 0

  t_text_variant_plain:
    params:
      - id: param_offset
        type: u4
      - id: param_length
        type: u4
    instances:
      content:
        type: t_text_content_plain
        pos: param_offset
        size: param_length
        if: param_offset != 0

  t_text_content_full:
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

  t_text_content_plain:
    seq:
      - id: data
        size: _io.size

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
      - id: pieces
        type: t_linktable_content_piece
        repeat: eos

  t_linktable_content_piece:
    seq:
      - id: mode
        type: u2
      - id: data
        type:
          switch-on: mode
          cases:
            4: t_linktable_content_piece_4
            6: t_linktable_content_piece_6
            9: t_linktable_content_piece_9
            11: t_linktable_content_piece_11
            12: t_linktable_content_piece_12
            13: t_linktable_content_piece_13
            14: t_linktable_content_piece_14
            20: t_linktable_content_piece_20
            99: t_linktable_content_piece_99
            240: t_linktable_content_piece_240
            16717: t_linktable_content_piece_16717
            49407: t_linktable_content_piece_49407
            65535: t_linktable_content_piece_65535

  t_linktable_content_piece_4:
    seq:
      - id: topleft_x
        type: u2
      - id: topleft_y
        type: u2
      - id: width
        type: u2
      - id: height
        type: u2
      - id: slider_topleft_x
        type: u2
      - id: slider_topleft_y
        type: u2
      - id: slider_height
        type: u2
      - id: textfile_length
        type: u1
      - id: textfile
        size: textfile_length

  t_linktable_content_piece_6:
    seq:
      - id: foo
        size: 71

  t_linktable_content_piece_9:
    seq:
      - id: foo
        size: 27

  t_linktable_content_piece_11:
    seq:
      - id: foo
        type: u2

  t_linktable_content_piece_12:
    seq:
      - id: id
        type: u1
      - id: foo
        type: u1

  t_linktable_content_piece_13:
    seq:
      - id: id
        type: u2
      - id: textfile_length
        type: u1
      - id: textfile
        size: textfile_length

  t_linktable_content_piece_14:
    seq:
      - id: id
        type: u2
      - id: value
        type: u2

  t_linktable_content_piece_20:
    seq:
      - id: textfile_length
        type: u1
      - id: textfile
        size: textfile_length
      - id: foo
        type: u1

  t_linktable_content_piece_99:
    seq:
      - id: length
        type: u2
      - id: foo
        size: length - 2

  t_linktable_content_piece_240:
    seq:
      - id: foo
        size: _io.size - 2

  t_linktable_content_piece_16717:
    seq:
      - id: foo
        size: _io.size - 2

  t_linktable_content_piece_49407:
    seq:
      - id: foo
        size: _io.size - 2

  t_linktable_content_piece_65535:
    seq:
      - id: foo
        type: u2

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
