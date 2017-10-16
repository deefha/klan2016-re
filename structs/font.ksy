meta:
  id: klan_font
  file-extension: lib
  title: KLAN font library
  application: KLAN discmag engine
  endian: le
  encoding: ASCII
  imports:
    - common_header

doc-ref: https://wiki.klan2016.cz/knihovny/fonty.html

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
        type: u4
      - id: offsets
        type: u4
        repeat: expr
        repeat-expr: 63

  t_data:
    instances:
      fonts:
        type: t_font(_parent.fat.offsets[_index])
        repeat: expr
        repeat-expr: 63
      
  t_font:
    params:
      - id: param_offset
        type: u4
    instances:
      content:
        type: t_font_content
        pos: param_offset
        if: param_offset != 0

  t_font_content:
    seq:
      - id: matrices_size
        type: u4
      - id: height
        type: u4
      - id: colormap
        size: 768
      - id: characters
        type: t_character
        repeat: expr
        repeat-expr: 256
      - id: matrices
        type: t_matrice(computed_matrices_offset + characters[_index].computed_offset, characters[_index].computed_width, height)
        repeat: expr
        repeat-expr: 256
    instances:
      computed_matrices_offset:
        value: _parent.param_offset + 4 + 4 + 768 + (256 * 4)

  t_character:
    seq:
      - id: offset_and_width
        type: u4
    instances:
      computed_offset:
        value: offset_and_width & 0xffffff
      computed_width:
        value: offset_and_width >> 0x18

  t_matrice:
    params:
      - id: param_offset
        type: u4
      - id: param_width
        type: u4
      - id: param_height
        type: u4
    instances:
      content:
        pos: param_offset
        size: param_width * param_height
        if: param_width != 0
