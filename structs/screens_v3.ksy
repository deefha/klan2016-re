meta:
  id: klan_screens_v3
  file-extension: z3p
  title: KLAN screens v3
  application: KLAN discmag engine
  endian: le
  encoding: ASCII

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
        type: u2
      - id: foo
        type: u2
      - id: data
        type: t_screen_data

  t_screen_data:
    seq:
      - id: commands
        type: t_screen_data_command
        repeat: until
        repeat-until: _.type == 0xffff
      - id: events
        type: t_screen_data_event
        repeat: until
        repeat-until: _.binding == 0xffff
    
  t_screen_data_command:
    seq:
      - id: type
        type: u2
      - id: content
        type:
          switch-on: type
          cases:
            0x0001: t_screen_data_command_0001 # doit
            0x0004: t_screen_data_command_0004 # text
            0x0005: t_screen_data_command_0005 # video
            0x0006: t_screen_data_command_0006 # obrazky
            0x0007: t_screen_data_command_0007 # zvuk
            0x0009: t_screen_data_command_0009 # button
            0x000a: t_screen_data_command_000a # area
            0x000b: t_screen_data_command_000b # event
            0x000c: t_screen_data_command_000c # gotopage
            0x000d: t_screen_data_command_000d # svar
            0x000e: t_screen_data_command_000e # ivar / mov
            0x000f: t_screen_data_command_000f # screen
            #0x0010: t_screen_data_command_0010 # woknoshit (no content)
            0x0011: t_screen_data_command_0011 # keybutt
            0x0012: t_screen_data_command_0012 # getchar
            0x0013: t_screen_data_command_0013 # pic
            0x0014: t_screen_data_command_0014 # demo
            0x0015: t_screen_data_command_0015 # reklama
            0x0016: t_screen_data_command_0016 # keyevent
            0x0017: t_screen_data_command_0017 # snap
            0x0018: t_screen_data_command_0018 # playwav
            0x0020: t_screen_data_command_0020 # image
            0x0023: t_screen_data_command_0023 # curhelp
            0x0063: t_screen_data_command_0063 # if

  t_screen_data_event:
    seq:
      - id: binding
        type: u2
      - id: content
        type: t_screen_data_event_content
        if: binding != 0xffff

  # doit
  t_screen_data_command_0001:
    seq:
      - id: id
        type: u2

  # text
  t_screen_data_command_0004:
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

  # video
  t_screen_data_command_0005:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2
      - id: foo_3
        type: u2
      - id: foo_4
        type: u2
      - id: foo_5
        type: u2
      - id: foo_6
        type: u1

  # obrazky
  t_screen_data_command_0006:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2
      - id: foo_3
        type: u2
      - id: foo_4
        type: u2
      - id: foo_5
        type: u1

  # zvuk
  t_screen_data_command_0007:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2
      - id: foo_3
        type: u2
      - id: foo_4
        type: u2
      - id: foo_5
        type: u1

  # button
  t_screen_data_command_0009:
    seq:
      - id: id
        type: u2
      - id: image
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
      - id: foo_2
        type: u1

  # area
  t_screen_data_command_000a:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2
      - id: foo_3
        type: u2
      - id: foo_4
        type: u2
      - id: foo_5
        type: u2
      - id: foo_6
        type: u1

  # event
  t_screen_data_command_000b:
    seq:
      - id: id
        type: u2

  # gotopage
  t_screen_data_command_000c:
    seq:
      - id: id
        type: u2

  # svar
  t_screen_data_command_000d:
    seq:
      - id: variable
        type: u2
      - id: value_length
        type: u1
      - id: value
        size: value_length

  # ivar / mov
  t_screen_data_command_000e:
    seq:
      - id: variable
        type: u2
      - id: value
        type: u2

  # screen
  t_screen_data_command_000f:
    seq:
      - id: id
        type: u2

  # keybutt
  t_screen_data_command_0011:
    seq:
      - id: topleft_x
        type: u2
      - id: topleft_y
        type: u2
      - id: image
        type: u2
      - id: foo
        type: u2
      - id: scancode
        type: u2

  # getchar
  t_screen_data_command_0012:
    seq:
      - id: id
        type: u2

  # pic
  t_screen_data_command_0013:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2
      - id: foo_3
        type: u2

  # demo
  t_screen_data_command_0014:
    seq:
      - id: textfile_length
        type: u1
      - id: textfile
        size: textfile_length
      - id: foo
        type: u1

  # reklama
  t_screen_data_command_0015:
    seq:
      - id: topleft_x
        type: u2
      - id: topleft_y
        type: u2
      - id: bottomright_x
        type: u2
      - id: bottomright_y
        type: u2
      - id: image
        type: u2
      - id: id
        type: u2

  # keyevent
  t_screen_data_command_0016:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2
      - id: foo_3
        type: u1

  # snap
  t_screen_data_command_0017:
    seq:
      - id: foo
        type: u1

  # playwav
  t_screen_data_command_0018:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u1

  # image
  t_screen_data_command_0020:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2
      - id: foo_3
        type: u2
      - id: foo_4
        type: u1

  # curhelp
  t_screen_data_command_0023:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2
      - id: foo_3
        type: u2
      - id: foo_4
        type: u2
      - id: text_length
        type: u1
      - id: text
        size: text_length
      - id: foo_5
        type: u1

  # if
  t_screen_data_command_0063:
    seq:
      - id: data_length_1
        type: u2
      - id: data_length_2
        type: u2
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2
      - id: branches
        type:
          switch-on: mode
          cases:
            1: t_screen_data_command_0063_mode_if_else
            _: t_screen_data_command_0063_mode_if_only
    instances:
      mode:
        value: 1
        if: data_length_2 != 0

  t_screen_data_command_0063_mode_if_else:
    seq:
      - id: branch_if
        type: t_screen_data_branch_if
        size: _parent.data_length_2 - 8
      - id: branch_else
        type: t_screen_data_branch_else
        size: _parent.data_length_1 - _parent.data_length_2

  t_screen_data_command_0063_mode_if_only:
    seq:
      - id: branch_if
        type: t_screen_data_branch_if
        size: _parent.data_length_1 - 8

  t_screen_data_branch_if:
    seq:
      - id: value_1
        type: u2
      - id: condition
        type: u2
      - id: value_2
        type: u2
      - id: commands
        type: t_screen_data_command
        repeat: eos

  t_screen_data_branch_else:
    seq:
      - id: commands
        type: t_screen_data_command
        repeat: eos

  t_screen_data_event_content:
    seq:
      - id: data_length
        type: u2
      - id: data
        type: t_screen_data_event_commands
        size: data_length - 4

  t_screen_data_event_commands:
    seq:
      - id: commands
        type: t_screen_data_command
        repeat: eos
