meta:
  id: klan_imgs
  file-extension: lib
  title: KLAN imgs library
  application: KLAN discmag engine
  endian: le
  encoding: ASCII
  imports:
    - common_header

doc-ref: https://wiki.klan2016.cz/knihovny/obrazky.html

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
        repeat-expr: 8195

  t_data:
    instances:
      images:
        type: t_image(_parent.fat.offsets[_index])
        repeat: expr
        repeat-expr: 8195
      
  t_image:
    params:
      - id: param_offset
        type: u4
    instances:
      content:
        type: t_image_content
        pos: param_offset
        if: param_offset != 0

  t_image_content:
    seq:
      - id: data_size
        type: u4
      - id: width
        type: u2
      - id: height
        type: u2
      - id: mode
        type: u2
      - id: foo
        size: 6
      - id: data
        type:
          switch-on: mode
          cases:
            1: t_image_data_indexed(data_size)
            256: t_image_data_indexed(data_size)
#      - id: colormap
#        size: 768
#      - id: characters
#        type: t_character
#        repeat: expr
#        repeat-expr: 256
#      - id: matrices
#        type: t_matrice(computed_matrices_offset + characters[_index].computed_offset, characters[_index].computed_width, height)
#        repeat: expr
#        repeat-expr: 256
#    instances:
#      computed_matrices_offset:
#        value: _parent.param_offset + 4 + 4 + 768 + (256 * 4)

  t_image_data_indexed:
    params:
      - id: param_data_size
        type: u4
    seq:
      - id: colormap
        size: 768
      - id: content
        size: param_data_size - 768

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
