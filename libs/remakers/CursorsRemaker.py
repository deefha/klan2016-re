# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
from PIL import Image
from .CommonRemaker import CommonRemaker


class CursorsRemaker(CommonRemaker):

	PATTERN_REMAKED_ASSET = "remaked://%s/%s/%s/%02d.png"


	def export_assets(self):
		for frame_index, frame in self.meta_decompiled.data.frames.items():
			if frame.content:
				self.items_total += 1
				status = True

				with open(self.meta_decompiled.data.colortables[str(frame.content.id)].content.data.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
					frame_colormap = f.read()

				with open(frame.content.data.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
					frame_content = f.read()

					i = Image.frombytes("P", (32, 32), frame_content)
					i.putpalette(frame_colormap)
					i.save("%s%02d.png" % (self.PATH_DATA_REMAKED, int(frame_index)))

				if status:
					self.items_hit += 1
				else:
					self.items_miss += 1


	def fill_meta(self):
		super(CursorsRemaker, self).fill_meta()

		self.meta_remaked.frames = ObjDict()

		for frame_index, frame in self.meta_decompiled.data.frames.items():
			if frame.content:
				data_frame = ObjDict()
				data_frame.width = 32
				data_frame.height = 32
				data_frame.asset = self.PATTERN_REMAKED_ASSET % (self.issue.number, self.source.library, self.source_index, int(frame_index))

				self.meta_remaked.frames[frame_index] = data_frame
