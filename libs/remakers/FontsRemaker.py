# common imports
import os, sys, datetime
from objdict import ObjDict
from pprint import pprint

# specific imports
from PIL import Image
from CommonRemaker import CommonRemaker



class FontsRemaker(CommonRemaker):

	def export_assets(self):
		for font_index, font in self.meta_decompiled.data.fonts.iteritems():
			if font.content:
				self.items_total += 1
				status = True

				path_characters = "%s%02d/characters/" % (self.PATH_DATA_REMAKED, int(font_index))

				if not os.path.exists(path_characters):
					os.makedirs(path_characters)

				with open(font.content.colormap.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
					font_colormap = f.read()

				transparent_r, transparent_g, transparent_b = bytearray(font_colormap)[765:768]

				i_font = Image.new("RGBA", (16 * font.content.height, 16 * font.content.height), (255, 255, 255, 0))

				for matrix_index, matrix in font.content.matrices.iteritems():
					if matrix.content:
						with open(matrix.content.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
							matrix_content = f.read()

						i_character = Image.frombytes("P", (font.content.characters[matrix_index].computed_width, font.content.height), matrix_content)
						i_character.putpalette(font_colormap)

						i_character_new = i_character.convert("RGBA")
						i_character_new_pixels = i_character_new.load()
						i_character_new_width, i_character_new_height = i_character_new.size

						for x in range(i_character_new_width):
							for y in range(i_character_new_height):
								if i_character_new_pixels[x, y] == (transparent_r, transparent_g, transparent_b, 255):
									i_character_new_pixels[x, y] = (255, 255, 255, 0)

						i_character_new.save("%s%03d.png" % (path_characters, int(matrix_index)))
						i_font.paste(i_character_new, ((int(matrix_index) % 16) * font.content.height, (int(matrix_index) // 16) * font.content.height))

				i_font.save("%s%02d/%s.png" % (self.PATH_DATA_REMAKED, int(font_index), self.source.library)) # TODO path

				if status:
					self.items_hit += 1
				else:
					self.items_miss += 1



	def fill_meta(self):
		super(FontsRemaker, self).fill_meta()

		self.meta_remaked.fonts = ObjDict()

		for font_index, font in self.meta_decompiled.data.fonts.iteritems():
			if font.content:
				path_characters = "remaked://%s/%s/%s/%02d/characters/" % (self.issue.number, self.source.library, self.source_index, int(font_index))

				data_font = ObjDict()
				data_font.height = font.content.height
				data_font.asset = "remaked://%s/%s/%s/%02d/font.png" % (self.issue.number, self.source.library, self.source_index, int(font_index))
				data_font.characters = ObjDict()

				for matrix_index, matrix in font.content.matrices.iteritems():
					if matrix.content:
						data_matrix = ObjDict()
						data_matrix.width = font.content.characters[matrix_index].computed_width
						data_matrix.asset = "%s%03d.png" % (path_characters, int(matrix_index))

						data_font.characters[matrix_index] = data_matrix

				self.meta_remaked.fonts[font_index] = data_font
