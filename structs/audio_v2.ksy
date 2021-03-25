meta:
  id: klan_audio_v2
  file-extension: lib
  title: KLAN audio library v2
  application: KLAN discmag engine
  endian: le
  encoding: ASCII
  imports:
    - common_header

doc-ref: https://wiki.klan2016.cz/knihovny/zvuky.html

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
      - id: foo_1
        type: u4
      - id: foo_2
        type: u4
      - id: foo_3
        type: u4
      - id: offsets
        type: u4
        repeat: expr
        repeat-expr: 8192

  t_data:
    instances:
      waves:
        type: t_wave(_parent.fat.offsets[_index])
        repeat: expr
        repeat-expr: 8192

  t_wave:
    params:
      - id: param_offset
        type: u4
    instances:
      content:
        type: t_wave_content
        pos: param_offset
        if: param_offset != 0

  t_wave_content:
    seq:
      - id: data_size
        type: u4
      - id: wave_size
        type: u4
      - id: mode
        type: u1
      - id: stereo
        type: u1
      - id: cache
        type: u1
      - id: foo_1
        type: u1
      - id: foo_2
        type: u4
      - id: data
        type: t_wave_data(data_size)

  t_wave_data:
    params:
      - id: param_data_size
        type: u4
    seq:
      - id: title
        size: 32
      - id: content
        size: param_data_size
