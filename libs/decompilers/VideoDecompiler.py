# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
from .CommonDecompiler import CommonDecompiler


class VideoDecompiler(CommonDecompiler):

  PATTERN_PATH_ACTION = "%s%04d/frames/%04d/actions/%02d/"
  PATTERN_FILE_ACTION = "%s%04d/frames/%04d/actions/%02d/content.bin"
  PATTERN_DECOMPILED_ACTION = "decompiled://%s/%s/%s/%04d/frames/%04d/actions/%02d/content.bin"


  def fill_meta_data(self):
    super(VideoDecompiler, self).fill_meta_data()

    self.meta.data.anims = ObjDict()

    for anim_index, anim in enumerate(tqdm(self.library.data.anims, desc="data.anims", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
      data_anim = ObjDict()
      data_anim.param_offset = anim.param_offset
      data_anim.content = ObjDict()

      if anim.content:
        #print "Wave #%d: param_offset=%d, data_size=%d, anim_size=%d, mode=%d" % (anim_index, anim.param_offset, anim.content.data_size, anim.content.anim_size, anim.content.mode)

        data_anim.content.data_size = anim.content.data_size
        data_anim.content.count_frames = anim.content.count_frames
        data_anim.content.width = anim.content.width
        data_anim.content.height = anim.content.height
        data_anim.content.foo_1 = anim.content.foo_1
        data_anim.content.foo_2 = anim.content.foo_2
        data_anim.content.foo_3 = anim.content.foo_3
        data_anim.content.foo_4 = anim.content.foo_4

        data_anim.content.data = ObjDict()
        data_anim.content.data.param_count_frames = anim.content.data.param_count_frames
        data_anim.content.data.frames = ObjDict()

        for frame_index, frame in enumerate(tqdm(anim.content.data.frames, desc="admin.content.data.frames", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
          data_frame = ObjDict()
          data_frame.data_size = frame.data_size
          data_frame.id = frame.id
          data_frame.count_actions = frame.count_actions
          data_frame.actions = ObjDict()

          for action_index, action in enumerate(tqdm(frame.actions, desc="frame.actions", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
            path_action = self.PATTERN_PATH_ACTION % (self.PATH_DATA, anim_index, frame_index, action_index)

            if not os.path.exists(path_action):
                os.makedirs(path_action)

            data_action = ObjDict()
            data_action.data_size = action.data_size
            data_action.id = action.id
            data_action.mode = action.mode

            file_action = self.PATTERN_FILE_ACTION % (self.PATH_DATA, anim_index, frame_index, action_index)

            data_action.data = self.PATTERN_DECOMPILED_ACTION % (self.issue.number, self.source.library, self.source_index, anim_index, frame_index, action_index)

            #print "\tAction #%d" % action_index
            with open(file_action, "wb") as f:
                f.write(action.data)

            data_frame.actions[str(action_index)] = data_action

          data_anim.content.data.frames[str(frame_index)] = data_frame
       #else:
        #print "Wave #%d: param_offset=%d, no content" % (anim_index, anim.param_offset)

      self.meta.data.anims[str(anim_index)] = data_anim
