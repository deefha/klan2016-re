meta:
  id: klan_cursors
  file-extension: lib
  title: KLAN cursors library
  application: KLAN discmag engine
  endian: le
  encoding: ASCII
  imports:
    - common_header

doc-ref: https://wiki.klan2016.cz/knihovny/kurzory.html

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
      - id: cursors_offset
        type: u4
      - id: cursors_count
        type: u4
      - id: foo_1_offset
        type: u4
      - id: foo_2_count
        type: u4
      - id: colortables_ofset
        type: u4
      - id: foo
        size: 8
      - id: foo_2
        type: t_fat_foo_2
        repeat: expr
        repeat-expr: 99

  t_fat_foo_2:
    seq:
      - id: offset
        type: u4
      - id: foo
        type: u4

  t_data:
    instances:
      cursors:
        type: t_cursor(_parent.fat.cursors_offset, _index)
        repeat: expr
        repeat-expr: _parent.fat.cursors_count
      foo_1:
        type: t_foo_1(_parent.fat.foo_1_offset)
      foo_2:
        type: t_foo_2(_parent.fat.foo_2[_index].offset)
        repeat: expr
        repeat-expr: _parent.fat.foo_2_count
      colortables:
        type: t_colortable(_parent.fat.colortables_ofset, _index)
        repeat: expr
        repeat-expr: 5

  t_cursor:
    params:
      - id: param_offset
        type: u4
      - id: param_index
        type: u4
    instances:
      content:
        type: t_cursor_content
        pos: param_offset + (param_index * (1 + 1 + 2 + 1024))

  t_cursor_content:
    seq:
      - id: x
        type: u1
      - id: y
        type: u1
      - id: id
        type: u2
      - id: data
        size: 1024

  t_foo_1:
    params:
      - id: param_offset
        type: u4
    instances:
      content:
        type: t_foo_1_content
        pos: param_offset

  t_foo_1_content:
    seq:
      - id: data
        size: 512

  t_foo_2:
    params:
      - id: param_offset
        type: u4
    instances:
      content:
        type: t_foo_2_content
        pos: param_offset

  t_foo_2_content:
    seq:
      - id: data
        size: 31

  t_colortable:
    params:
      - id: param_offset
        type: u4
      - id: param_index
        type: u4
    instances:
      content:
        type: t_colortable_content
        pos: param_offset + (param_index * 768)

  t_colortable_content:
    seq:
      - id: data
        size: 768
