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
    seq:
      - id: data
        size: _io.size

  t_text_content_plain:
    seq:
      - id: data
        size: _io.size
