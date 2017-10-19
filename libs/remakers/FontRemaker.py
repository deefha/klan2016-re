import os, sys, pprint

from objdict import ObjDict
from PIL import Image

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
				path_characters = "%s%02d/characters/" % (self.PATH_OBJECTS, int(font_index))

				if not os.path.exists(path_characters):
					os.makedirs(path_characters)

				with open(font.content.colormap.replace("blobs://", self.ROOT_BLOBS), "rb") as f:
					font_colormap = f.read()

				for matrix_index, matrix in font.content.matrices.iteritems():
					if matrix.content:
						with open(matrix.content.replace("blobs://", self.ROOT_BLOBS), "rb") as f:
							matrix_content = f.read()

						i = Image.frombytes("P", (font.content.characters[matrix_index].computed_width, font.content.height), matrix_content)
						i.putpalette(font_colormap)
						i.save("%s%03d.gif" % (path_characters, int(matrix_index)))
