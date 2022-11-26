meta:
  id: klan_video
  file-extension: lib
  title: KLAN video library
  application: KLAN discmag engine
  endian: le
  encoding: ASCII
  imports:
    - common_header

doc-ref: https://wiki.klan2016.cz/knihovny/video.html

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
        repeat-expr: 1024

  t_data:
    instances:
      anims:
        type: t_anim(_parent.fat.offsets[_index])
        repeat: expr
        repeat-expr: 1024

  t_anim:
    params:
      - id: param_offset
        type: u4
    instances:
      content:
        type: t_anim_content
        pos: param_offset
        if: param_offset != 0

  t_anim_content:
    seq:
      - id: data_size
        type: u4
      - id: count_frames
        type: u4
      - id: width
        type: u4
      - id: height
        type: u4
      - id: foo_1
        type: u4
      - id: foo_2
        type: u4
      - id: foo_3
        type: u4
      - id: foo_4
        type: u4
      - id: data
        type: t_anim_data(count_frames)

  t_anim_data:
    params:
      - id: param_count_frames
        type: u4
    seq:
      - id: frames
        type: t_frame
        repeat: expr
        repeat-expr: param_count_frames

  t_frame:
    seq:
      - id: data_size
        type: u4
      - id: id
        type: u2
      - id: count_actions
        type: u2
      - id: actions
        type: t_action
        repeat: expr
        repeat-expr: count_actions

  t_action:
    seq:
      - id: data_size
        type: u4
      - id: id
        type: u2
      - id: mode
        type: u2
      - id: data
        size: data_size
