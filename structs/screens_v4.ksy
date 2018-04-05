meta:
  id: klan_screens_v4
  file-extension: z3p
  title: KLAN screens v4
  application: KLAN discmag engine
  endian: le
  encoding: ASCII
  imports:
    - common_macros_v4

doc-ref: https://wiki.klan2016.cz

seq:
  - id: header
    type: t_header
  - id: fat
    type: t_fat
  - id: data
    type: t_data

types:
  t_header:
    seq:
      - id: version
        type: u2
      - id: foo
        type: u2

  t_fat:
    seq:
      - id: offsets
        type: u4
        repeat: expr
        repeat-expr: 1023

  t_data:
    instances:
      screens:
        type: t_screen(_parent.fat.offsets[_index])
        repeat: expr
        repeat-expr: 1023

  t_screen:
    params:
      - id: param_offset
        type: u4
    instances:
      content:
        type: t_screen_content
        pos: param_offset
        if: param_offset != 0xffffffff

  t_screen_content:
    seq:
      - id: type_1
        type: u1
      - id: type_2
        type: u1
      - id: foo
        type:
          switch-on: type_2
          cases:
            1: u2
            _: u1
      - id: data
        type: t_screen_data

  t_screen_data:
    seq:
      - id: macros
        type: t_macros_v4
        repeat: until
        repeat-until: _.type == 0xffff
      - id: events
        type: t_screen_data_event
        repeat: until
        repeat-until: _.binding == 0xffff

  t_screen_data_event:
    seq:
      - id: binding
        type: u2
      - id: content
        type: t_screen_data_event_content
        if: binding != 0xffff

  t_screen_data_event_content:
    seq:
      - id: data_length
        type: u2
      - id: data
        type: t_screen_data_event_macros
        size: data_length - 4

  t_screen_data_event_macros:
    seq:
      - id: macros
        type: t_macros_v4
        repeat: eos
