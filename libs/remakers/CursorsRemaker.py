import os, sys, pprint

from objdict import ObjDict
from PIL import Image

from CommonRemaker import CommonRemaker



class CursorsRemaker(CommonRemaker):

	def export_assets(self):
		for frame_index, frame in self.meta.data.frames.iteritems():
			if frame.content:
				with open(self.meta.data.colortables[str(frame.content.id)].content.data.replace("blobs://", self.ROOT_BLOBS), "rb") as f:
					frame_colormap = f.read()

				with open(frame.content.data.replace("blobs://", self.ROOT_BLOBS), "rb") as f:
					frame_content = f.read()

					i = Image.frombytes("P", (32, 32), frame_content)
					i.putpalette(frame_colormap)
					i.save("%s%02d.png" % (self.PATH_ASSETS, int(frame_index)))



	def fill_scheme(self):
		super(CursorsRemaker, self).fill_scheme()

		self.scheme.frames = ObjDict()

		for frame_index, frame in self.meta.data.frames.iteritems():
			if frame.content:
				data_frame = ObjDict()
				data_frame.asset = "assets://%s/%s/%02d.png" % (self.issue, self.source, int(frame_index))

				self.scheme.frames[frame_index] = data_frame
