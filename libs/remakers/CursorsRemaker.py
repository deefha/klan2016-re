# common imports
import os, sys, datetime
from objdict import ObjDict

# specific imports
from PIL import Image
from CommonRemaker import CommonRemaker



class CursorsRemaker(CommonRemaker):

	PATTERN_REMAKED_ASSET = "remaked://%s/%s/%s/%02d.png"

	def export_assets(self):
		for frame_index, frame in self.meta_decompiled.data.frames.iteritems():
			if frame.content:
				with open(self.meta_decompiled.data.colortables[str(frame.content.id)].content.data.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
					frame_colormap = f.read()

				with open(frame.content.data.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
					frame_content = f.read()

					i = Image.frombytes("P", (32, 32), frame_content)
					i.putpalette(frame_colormap)
					i.save("%s%02d.png" % (self.PATH_DATA_REMAKED, int(frame_index)))



	def fill_meta(self):
		super(CursorsRemaker, self).fill_meta()

		self.meta_remaked.frames = ObjDict()

		for frame_index, frame in self.meta_decompiled.data.frames.iteritems():
			if frame.content:
				data_frame = ObjDict()
				data_frame.asset = self.PATTERN_REMAKED_ASSET % (self.issue.number, self.source.library, self.source_index, int(frame_index))

				self.meta_remaked.frames[frame_index] = data_frame
