meta:
  id: klan_music_v1
  file-extension: lib
  title: KLAN music library v1
  application: KLAN discmag engine
  endian: le
  encoding: ASCII
  imports:
    - common_header

doc-ref: https://wiki.klan2016.cz/knihovny/hudba.html

seq:
  - id: header
    type: t_header
  - id: header2
    type: t_header2
  - id: fat_mods
    type: t_fat_mods
  - id: fat_samples
    type: t_fat_samples
  - id: data
    type: t_data

types:
  t_header2:
    seq:
      - id: count_mods
        type: u4
      - id: count_samples
        type: u4
      - id: foo
        size: 24

  t_fat_mods:
    seq:
      - id: offsets
        type: u4
        repeat: expr
        repeat-expr: 130

  t_fat_samples:
    seq:
      - id: offsets
        type: u4
        repeat: expr
        repeat-expr: 520

  t_data:
    seq:
      - id: names
        size: 32
        repeat: expr
        repeat-expr: 128
    instances:
      mods:
        type: t_mod(_parent.fat_mods.offsets[_index])
        repeat: expr
        repeat-expr: 130
      samples:
        type: t_sample(_parent.fat_samples.offsets[_index])
        repeat: expr
        repeat-expr: 520
      
  t_mod:
    params:
      - id: param_offset
        type: u4
    instances:
      content:
        type: t_mod_content
        pos: param_offset
        if: param_offset != 0

  t_mod_content:
    seq:
      - id: name
        size: 32
      - id: count_sequences
        type: u2
      - id: count_patterns
        type: u2
      - id: count_samples
        type: u2
      - id: foo_1
        type: u2
      - id: size_patterns
        type: u4
      - id: foo_2
        type: u4
      - id: data
        type: t_mod_data(count_patterns)

  t_mod_data:
    params:
      - id: param_count_patterns
        type: u4
    seq:
      - id: samples
        type: u2
        repeat: expr
        repeat-expr: 32
      - id: sequences
        type: u1
        repeat: expr
        repeat-expr: 128
      - id: patterns
        size: 2048
        repeat: expr
        repeat-expr: param_count_patterns

  t_sample:
    params:
      - id: param_offset
        type: u4
    instances:
      content:
        type: t_sample_content
        pos: param_offset
        if: param_offset != 0

  t_sample_content:
    seq:
      - id: data_size
        type: u4
      - id: loop_start
        type: u4
      - id: loop_end
        type: u4
      - id: foo
        size: 4
      - id: data
        type: t_sample_data(data_size)

  t_sample_data:
    params:
      - id: param_data_size
        type: u4
    seq:
      - id: content
        size: param_data_size
