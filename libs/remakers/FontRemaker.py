import os, sys, pprint

from objdict import ObjDict
from PIL import Image

from CommonRemaker import CommonRemaker



class FontRemaker(CommonRemaker):

	PATTERN_PATH_MATRICES = "%s%02d/matrices/"
	PATTERN_FILE_COLORMAP = "%s%02d/colormap.bin"
	PATTERN_FILE_MATRIX = "%s%03d.bin"

	def export_assets(self):
		for font_index, font in self.meta.data.fonts.iteritems():
			if font.content:
				path_characters = "%s%02d/characters/" % (self.PATH_ASSETS, int(font_index))

				if not os.path.exists(path_characters):
					os.makedirs(path_characters)

				with open(font.content.colormap.replace("blobs://", self.ROOT_BLOBS), "rb") as f:
					font_colormap = f.read()

				i_font = Image.new("RGBA", (16 * font.content.height, 16 * font.content.height), (255, 255, 255, 0))

				for matrix_index, matrix in font.content.matrices.iteritems():
					if matrix.content:
						with open(matrix.content.replace("blobs://", self.ROOT_BLOBS), "rb") as f:
							matrix_content = f.read()

						i_character = Image.frombytes("P", (font.content.characters[matrix_index].computed_width, font.content.height), matrix_content)
						i_character.putpalette(font_colormap)
						i_character.save("%s%03d.gif" % (path_characters, int(matrix_index)))
						i_character.convert("RGBA")

						i_font.paste(i_character, ((int(matrix_index) % 16) * font.content.height, (int(matrix_index) // 16) * font.content.height))

				i_font.save("%s%02d/font.gif" % (self.PATH_ASSETS, int(font_index)), transparency = 0)
				i_font.save("%s%02d/font.png" % (self.PATH_ASSETS, int(font_index)))



	def fill_scheme(self):
		super(FontRemaker, self).fill_scheme()

		self.scheme.fonts = ObjDict()

		for font_index, font in self.meta.data.fonts.iteritems():
			if font.content:
				path_characters = "assets://%s/font/%02d/characters/" % (self.issue, int(font_index))

				data_font = ObjDict()
				data_font.asset = "assets://%s/font/%02d/font.gif" % (self.issue, int(font_index))
				data_font.characters = ObjDict()
				data_font.height = font.content.height

				for matrix_index, matrix in font.content.matrices.iteritems():
					if matrix.content:
						data_matrix = ObjDict()
						data_matrix.width = font.content.characters[matrix_index].computed_width
						data_matrix.asset = "%s%03d.gif" % (path_characters, int(matrix_index))

						data_font.characters[matrix_index] = data_matrix

				self.scheme.fonts[font_index] = data_font
