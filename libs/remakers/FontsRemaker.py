# common imports
import os, sys, datetime
from objdict import ObjDict

# specific imports
from PIL import Image
from CommonRemaker import CommonRemaker



class FontsRemaker(CommonRemaker):

	def export_assets(self):
		for font_index, font in self.meta_decompiled.data.fonts.iteritems():
			if font.content:
				path_characters = "%s%02d/characters/" % (self.PATH_DATA_REMAKED, int(font_index))

				if not os.path.exists(path_characters):
					os.makedirs(path_characters)

				with open(font.content.colormap.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
					font_colormap = f.read()

				i_font = Image.new("RGBA", (16 * font.content.height, 16 * font.content.height), (255, 255, 255, 0))

				for matrix_index, matrix in font.content.matrices.iteritems():
					if matrix.content:
						with open(matrix.content.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
							matrix_content = f.read()

						i_character = Image.frombytes("P", (font.content.characters[matrix_index].computed_width, font.content.height), matrix_content)
						i_character.putpalette(font_colormap)
						i_character.save("%s%03d.gif" % (path_characters, int(matrix_index)))
						i_character.convert("RGBA")

						i_font.paste(i_character, ((int(matrix_index) % 16) * font.content.height, (int(matrix_index) // 16) * font.content.height))

				i_font.save("%s%02d/%s.gif" % (self.PATH_DATA_REMAKED, int(font_index), self.source.library), transparency = 0) # TODO path
				i_font.save("%s%02d/%s.png" % (self.PATH_DATA_REMAKED, int(font_index), self.source.library)) # TODO path



	def fill_meta(self):
		super(FontsRemaker, self).fill_meta()

		self.meta_remaked.fonts = ObjDict()

		for font_index, font in self.meta_decompiled.data.fonts.iteritems():
			if font.content:
				path_characters = "remaked://%s/%s/%s/%02d/characters/" % (self.issue.number, self.source.library, self.source_index, int(font_index))

				data_font = ObjDict()
				data_font.height = font.content.height
				data_font.asset = "remaked://%s/%s/%s/%02d/font.gif" % (self.issue.number, self.source.library, self.source_index, int(font_index))
				data_font.characters = ObjDict()

				for matrix_index, matrix in font.content.matrices.iteritems():
					if matrix.content:
						data_matrix = ObjDict()
						data_matrix.width = font.content.characters[matrix_index].computed_width
						data_matrix.asset = "%s%03d.gif" % (path_characters, int(matrix_index))

						data_font.characters[matrix_index] = data_matrix

				self.meta_remaked.fonts[font_index] = data_font
