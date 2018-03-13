meta:
  id: klan_texts_v1
  file-extension: lib
  title: KLAN texts library v1
  application: KLAN discmag engine
  endian: le

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
