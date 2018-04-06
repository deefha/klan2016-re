meta:
  id: t_macros_v2
  endian: le
  encoding: ASCII

doc-ref: https://wiki.klan2016.cz

seq:
  - id: type
    type: u2
  - id: content
    type:
      switch-on: type
      cases:
        0x0001: t_macros_v2_macro_0001 # doit
        0x0004: t_macros_v2_macro_0004 # text
        0x0005: t_macros_v2_macro_0005 # video
        0x0006: t_macros_v2_macro_0006 # obrazky
        0x0007: t_macros_v2_macro_0007 # zvuk
        0x0009: t_macros_v2_macro_0009 # button
        0x000a: t_macros_v2_macro_000a # area
        0x000b: t_macros_v2_macro_000b # event
        0x000c: t_macros_v2_macro_000c # gotopage
        0x000d: t_macros_v2_macro_000d # svar
        0x000e: t_macros_v2_macro_000e # ivar / mov
        0x000f: t_macros_v2_macro_000f # screen
        #0x0010: t_macros_v2_macro_0010 # woknoshit (no content)
        0x0011: t_macros_v2_macro_0011 # keybutt
        0x0012: t_macros_v2_macro_0012 # getchar
        0x0013: t_macros_v2_macro_0013 # pic
        0x0014: t_macros_v2_macro_0014 # demo
        0x0015: t_macros_v2_macro_0015 # reklama
        0x0016: t_macros_v2_macro_0016 # keyevent
        0x0017: t_macros_v2_macro_0017 # snap
        0x0018: t_macros_v2_macro_0018 # playwav
        0x0020: t_macros_v2_macro_0020 # image
        0x0021: t_macros_v2_macro_0021 # ???
        0x0022: t_macros_v2_macro_0022 # ???
        0x0023: t_macros_v2_macro_0023 # curhelp
        0x0024: t_macros_v2_macro_0024 # ???
        0x0025: t_macros_v2_macro_0025 # ???
        0x0026: t_macros_v2_macro_0026 # ???
        0x0027: t_macros_v2_macro_0027 # ???
        0x0028: t_macros_v2_macro_0028 # ???
        0x0029: t_macros_v2_macro_0029 # ???
        #0x002a: t_macros_v2_macro_002a # ??? (no content)
        0x002b: t_macros_v2_macro_002b # ???
        0x002c: t_macros_v2_macro_002c # ???
        0x002d: t_macros_v2_macro_002d # ???
        0x0033: t_macros_v2_macro_0033 # link?
        0x0035: t_macros_v2_macro_0035 # ???
        0x0036: t_macros_v2_macro_0036 # ???
        0x0037: t_macros_v2_macro_0037 # ???
        0x0038: t_macros_v2_macro_0038 # ???
        #0x003a: t_macros_v2_macro_003a # ??? (no content)
        0x0063: t_macros_v2_macro_0063 # if
        0x00f0: t_macros_v2_macro_00f0 # #07/texts/184/linktable error
        0x414d: t_macros_v2_macro_414d # #10/texts/202/linktable error
        0x4f4e: t_macros_v2_macro_4f4e # nokeys
        0xc0ff: t_macros_v2_macro_c0ff # #08/texts/211/linktable error

types:
  # doit
  t_macros_v2_macro_0001:
    seq:
      - id: id
        type: u2

  # text
  t_macros_v2_macro_0004:
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
  t_macros_v2_macro_0005:
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
  t_macros_v2_macro_0006:
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
  t_macros_v2_macro_0007:
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
  t_macros_v2_macro_0009:
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
  t_macros_v2_macro_000a:
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
  t_macros_v2_macro_000b:
    seq:
      - id: id
        type: u2

  # gotopage
  t_macros_v2_macro_000c:
    seq:
      - id: id
        type: u2

  # svar
  t_macros_v2_macro_000d:
    seq:
      - id: variable
        type: u2
      - id: value_length
        type: u1
      - id: value
        size: value_length

  # ivar / mov
  t_macros_v2_macro_000e:
    seq:
      - id: variable
        type: u2
      - id: value
        type: u2

  # screen
  t_macros_v2_macro_000f:
    seq:
      - id: id
        type: u2

  # keybutt
  t_macros_v2_macro_0011:
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
  t_macros_v2_macro_0012:
    seq:
      - id: id
        type: u2

  # pic
  t_macros_v2_macro_0013:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2
      - id: foo_3
        type: u2

  # demo
  t_macros_v2_macro_0014:
    seq:
      - id: textfile_length
        type: u1
      - id: textfile
        size: textfile_length
      - id: foo
        type: u1

  # reklama
  t_macros_v2_macro_0015:
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
  t_macros_v2_macro_0016:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2
      - id: foo_3
        type: u1

  # snap
  t_macros_v2_macro_0017:
    seq:
      - id: foo
        type: u1

  # playwav
  t_macros_v2_macro_0018:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u1

  # image
  t_macros_v2_macro_0020:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2
      - id: foo_3
        type: u2
      - id: foo_4
        type: u1

  # ???
  t_macros_v2_macro_0021:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2
      - id: foo_3
        type: u2

  # ???
  t_macros_v2_macro_0022:
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

  # curhelp
  t_macros_v2_macro_0023:
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

  # ???
  t_macros_v2_macro_0024:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2

  # ???
  t_macros_v2_macro_0025:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2

  # ???
  t_macros_v2_macro_0026:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2

  # ???
  t_macros_v2_macro_0027:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2

  # ???
  t_macros_v2_macro_0028:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2
      - id: foo_3
        type: u1

  # ???
  t_macros_v2_macro_0029:
    seq:
      - id: foo
        type: u2

  # ???
  t_macros_v2_macro_002b:
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
        type: u2
      - id: foo_7
        type: u1

  # ???
  t_macros_v2_macro_002c:
    seq:
      - id: foo
        type: u2
      - id: textfile_length
        type: u1
      - id: textfile
        size: textfile_length

  # ???
  t_macros_v2_macro_002d:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u1

  # link?
  t_macros_v2_macro_0033:
    seq:
      - id: text_1_length
        type: u1
      - id: text_1
        size: text_1_length
      - id: text_2_length
        type: u1
      - id: text_2
        size: text_2_length
      - id: foo
        type: u1

  # ???
  t_macros_v2_macro_0035:
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
        type: u2
      - id: foo_7
        type: u2
      - id: foo_8
        type: u1

  # ???
  t_macros_v2_macro_0036:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2
      - id: foo_3
        type: u1

  # ???
  t_macros_v2_macro_0037:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2
      - id: foo_3
        type: u2
      - id: foo_4
        type: u2

  # ???
  t_macros_v2_macro_0038:
    seq:
      - id: foo
        type: u2

  # if
  t_macros_v2_macro_0063:
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
            1: t_macros_v2_macro_0063_mode_if_else
            _: t_macros_v2_macro_0063_mode_if_only
    instances:
      mode:
        value: 1
        if: data_length_2 != 0

  t_macros_v2_macro_0063_mode_if_else:
    seq:
      - id: branch_if
        type: t_macros_v2_macro_0063_branch_if(_parent.foo_1)
        size: _parent.data_length_2 - 8
      - id: branch_else
        type: t_macros_v2_macro_0063_branch_else
        size: _parent.data_length_1 - _parent.data_length_2

  t_macros_v2_macro_0063_mode_if_only:
    seq:
      - id: branch_if
        type: t_macros_v2_macro_0063_branch_if(_parent.foo_1)
        size: _parent.data_length_1 - 8

  t_macros_v2_macro_0063_branch_if:
    params:
      - id: param_foo_1
        type: u4
    seq:
      - id: value_1
        type: u2
      - id: condition
        type: u2
      - id: value_2
        type: u2
      - id: foo
        type: u1
        if: param_foo_1 == 1
      - id: macros
        type: t_macros_v2
        repeat: eos

  t_macros_v2_macro_0063_branch_else:
    seq:
      - id: macros
        type: t_macros_v2
        repeat: eos

  # #07/texts/184/linktable error
  t_macros_v2_macro_00f0:
    seq:
      - id: foo
        size: _io.size - 2

  # #10/texts/202/linktable error
  t_macros_v2_macro_414d:
    seq:
      - id: foo
        size: _io.size - 2

  # nokeys
  t_macros_v2_macro_4f4e:
    seq:
      - id: foo_1
        type: u2
      - id: foo_2
        type: u2

  # #08/texts/211/linktable error
  t_macros_v2_macro_c0ff:
    seq:
      - id: foo
        size: _io.size - 2
