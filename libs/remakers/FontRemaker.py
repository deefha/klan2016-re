import os, sys, pprint

from objdict import ObjDict
from CommonRemaker import CommonRemaker



class FontRemaker(CommonRemaker):

	PATTERN_PATH_MATRICES = "%s%02d/matrices/"
	PATTERN_FILE_COLORMAP = "%s%02d/colormap.bin"
	PATTERN_FILE_MATRIX = "%s%03d.bin"

	def export_objects(self):
		#print self.meta.header

		#for item, value in self.meta.header.iteritems():
			#print item, value

		#print self.meta.fat.offsets

		#for offset_index, offset in self.meta.fat.offsets.iteritems():
			#print offset

		for font_index, font in self.meta.data.fonts.iteritems():
			if font.content:
				print font.content.colormap
