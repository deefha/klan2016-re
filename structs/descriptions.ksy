meta:
  id: klan_descriptions
  file-extension: lib
  title: KLAN descriptions library
  application: KLAN discmag engine
  endian: le
  encoding: ASCII
  imports:
    - common_header

doc-ref: https://wiki.klan2016.cz/knihovny/popisky.html

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
      - id: foo_1
        type: u4
      - id: foo_2
        type: u4
      - id: foo_3
        type: u4
      - id: foo_4
        type: u4
      - id: offsets
        type: u4
        repeat: expr
        repeat-expr: 8192

  t_data:
    instances:
      descriptions:
        type: t_description(_parent.fat.offsets[_index])
        repeat: expr
        repeat-expr: 8192
      
  t_description:
    params:
      - id: param_offset
        type: u4
    instances:
      content:
        type: t_description_content
        pos: param_offset
        if: param_offset != 0

  t_description_content:
    seq:
      - id: title
        size: 128
