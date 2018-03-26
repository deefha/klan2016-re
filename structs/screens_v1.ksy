meta:
  id: klan_screens_v1
  file-extension: z3p
  title: KLAN screens v1
  application: KLAN discmag engine
  endian: le
  encoding: ASCII

doc-ref: https://wiki.klan2016.cz

seq:
  - id: version
    type: u4
  - id: fat
    type: t_fat
  - id: data
    type: t_data

types:
  t_fat:
    seq:
      - id: offsets
        type: u4
        repeat: expr
        repeat-expr: 255

  t_data:
    instances:
      screens:
        type: t_screen(_parent.fat.offsets[_index])
        repeat: expr
        repeat-expr: 255

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
      - id: type
        type: u4
      - id: header
        type:
          switch-on: type
          cases:
            0x0e000000: t_screen_content_header_0e000000
      - id: data
        type:
          switch-on: type
          cases:
            0x0e000000: t_screen_content_data_areas

  t_screen_content_header_0e000000:
    seq:
      - id: foo_1
        type: u2
      - id: type
        type: u2
      - id: foo_2
        type:
          switch-on: type
          cases:
            0x0000: t_screen_content_header_0e000000_0000
            0x6400: t_screen_content_header_0e000000_6400
      - id: background
        type: u2

  t_screen_content_header_0e000000_0000:
    seq:
      - id: data
        size: 15

  t_screen_content_header_0e000000_6400:
    seq:
      - id: data
        size: 21

  t_screen_content_data_areas:
    seq:
      - id: areas
        type: t_area
        repeat: until
        repeat-until: _.type == 0x000b or _.type == 0x0041

  t_area:
    seq:
      - id: type
        type: u2
      - id: data
        type:
          switch-on: type
          cases:
            0x0004: t_area_0004
            0x0009: t_area_0009
            0x000b: t_area_000b
            0x0011: t_area_0011
            0x0015: t_area_0015

  # hlavni oblast
  t_area_0004:
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
      - id: foo
        type: u2

  # tlacitko
  t_area_0009:
    seq:
      - id: id
        type: u2
      - id: background
        type: u2
      - id: foo_1
        type: u2
      - id: topleft_x
        type: u2
      - id: topleft_y
        type: u2
      - id: scancode
        type: u2
      - id: hover_topleft_x
        type: u2
      - id: hover_topleft_y
        type: u2
      - id: hover_bottomright_x
        type: u2
      - id: hover_bottomright_y
        type: u2
      - id: foo
        type: u1

  # konec sekce
  t_area_000b:
    seq:
      - id: foo
        size: 14

  # tlacitko slideru
  t_area_0011:
    seq:
      - id: topleft_x
        type: u2
      - id: topleft_y
        type: u2
      - id: background
        type: u2
      - id: foo
        type: u2
      - id: scancode
        type: u2

  # reklama
  t_area_0015:
    seq:
      - id: topleft_x
        type: u2
      - id: topleft_y
        type: u2
      - id: bottomright_x
        type: u2
      - id: bottomright_y
        type: u2
      - id: background
        type: u2
      - id: id
        type: u2
