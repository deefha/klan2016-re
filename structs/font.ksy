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
      - id: font_offset
        type: u4
    instances:
      body:
        type: t_font_body
        pos: font_offset
        if: font_offset != 0

  t_font_body:
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
        type: t_matrices
        size: matrices_size

  t_matrices:
    seq:
      - id: matrices
        type: t_matrice(_parent.characters[_index].offset, _parent.characters[_index].width, _parent.height)
        repeat: expr
        repeat-expr: 256

  t_matrice:
    params:
      - id: matrice_offset
        type: u4
      - id: matrice_width
        type: u4
      - id: matrice_height
        type: u4
    instances:
      body:
        pos: matrice_offset
        size: matrice_width * matrice_height
        if: matrice_width != 0

  t_character:
    seq:
      - id: offset_and_width
        type: u4
    instances:
      offset:
        value: offset_and_width & 0xffffff
      width:
        value: offset_and_width >> 0x18
