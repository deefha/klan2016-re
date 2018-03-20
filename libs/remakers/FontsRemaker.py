# -*- coding: utf-8 -*-

# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
from PIL import Image
from CommonRemaker import CommonRemaker



class FontsRemaker(CommonRemaker):

	def __init__(self, issue, source, source_index):
		super(FontsRemaker, self).__init__(issue, source, source_index)

		self.PATTERN_PATH_FONT_NORMAL = "%s%s" % (self.PATH_DATA_REMAKED, "%02d/normal/")
		self.PATTERN_PATH_FONT_NORMAL_LINK = "%s%s" % (self.PATH_DATA_REMAKED, "%02d/normal_link/")
		self.PATTERN_PATH_FONT_BOLD = "%s%s" % (self.PATH_DATA_REMAKED, "%02d/bold/")
		self.PATTERN_PATH_FONT_BOLD_LINK = "%s%s" % (self.PATH_DATA_REMAKED, "%02d/bold_link/")
		self.PATTERN_PATH_FONT_ITALIC = "%s%s" % (self.PATH_DATA_REMAKED, "%02d/italic/")
		self.PATTERN_PATH_FONT_ITALIC_LINK = "%s%s" % (self.PATH_DATA_REMAKED, "%02d/italic_link/")

		self.PATTERN_FILE_FONT_NORMAL = "%s%s" % (self.PATH_DATA_REMAKED, "%02d/normal.png")
		self.PATTERN_FILE_FONT_NORMAL_LINK = "%s%s" % (self.PATH_DATA_REMAKED, "%02d/normal_link.png")
		self.PATTERN_FILE_FONT_BOLD = "%s%s" % (self.PATH_DATA_REMAKED, "%02d/bold.png")
		self.PATTERN_FILE_FONT_BOLD_LINK = "%s%s" % (self.PATH_DATA_REMAKED, "%02d/bold_link.png")
		self.PATTERN_FILE_FONT_ITALIC = "%s%s" % (self.PATH_DATA_REMAKED, "%02d/italic.png")
		self.PATTERN_FILE_FONT_ITALIC_LINK = "%s%s" % (self.PATH_DATA_REMAKED, "%02d/italic_link.png")
		self.PATTERN_FILE_CHARACTER = "%s%03d.png"



	def export_assets(self):
		for font_index, font in tqdm(self.meta_decompiled.data.fonts.iteritems(), total=len(self.meta_decompiled.data.fonts), desc="data.fonts", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"):
			if font.content:
				self.items_total += 1
				status = True

				path_font_normal = self.PATTERN_PATH_FONT_NORMAL % int(font_index)
				path_font_normal_link = self.PATTERN_PATH_FONT_NORMAL_LINK % int(font_index)
				path_font_bold = self.PATTERN_PATH_FONT_BOLD % int(font_index)
				path_font_bold_link = self.PATTERN_PATH_FONT_BOLD_LINK % int(font_index)
				path_font_italic = self.PATTERN_PATH_FONT_ITALIC % int(font_index)
				path_font_italic_link = self.PATTERN_PATH_FONT_ITALIC_LINK % int(font_index)

				if not os.path.exists(path_font_normal):
					os.makedirs(path_font_normal)

				if not os.path.exists(path_font_normal_link):
					os.makedirs(path_font_normal_link)

				if not os.path.exists(path_font_bold):
					os.makedirs(path_font_bold)

				if not os.path.exists(path_font_bold_link):
					os.makedirs(path_font_bold_link)

				if not os.path.exists(path_font_italic):
					os.makedirs(path_font_italic)

				if not os.path.exists(path_font_italic_link):
					os.makedirs(path_font_italic_link)

				with open(font.content.colormap.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
					font_colormap = f.read()

				transparent_r, transparent_g, transparent_b = bytearray(font_colormap)[765:768]

				i_font_normal = Image.new("RGBA", (16 * font.content.height, 16 * font.content.height), (255, 255, 255, 0))
				i_font_normal_link = Image.new("RGBA", (16 * font.content.height, 16 * font.content.height), (255, 255, 255, 0))
				i_font_bold = Image.new("RGBA", (16 * font.content.height, 16 * font.content.height), (255, 255, 255, 0))
				i_font_bold_link = Image.new("RGBA", (16 * font.content.height, 16 * font.content.height), (255, 255, 255, 0))
				i_font_italic = Image.new("RGBA", (16 * font.content.height, 16 * font.content.height), (255, 255, 255, 0))
				i_font_italic_link = Image.new("RGBA", (16 * font.content.height, 16 * font.content.height), (255, 255, 255, 0))

				for matrix_index, matrix in font.content.matrices.iteritems():
					if matrix.content:
						with open(matrix.content.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
							matrix_content = f.read()

						i_character = Image.frombytes("P", (font.content.characters[matrix_index].computed_width, font.content.height), matrix_content)
						i_character.putpalette(font_colormap)

						# normal
						i_character_normal = i_character.convert("RGBA")
						i_character_normal_pixels = i_character_normal.load()
						i_character_normal_width, i_character_normal_height = i_character_normal.size

						for x in range(i_character_normal_width):
							for y in range(i_character_normal_height):
								if i_character_normal_pixels[x, y] == (transparent_r, transparent_g, transparent_b, 255):
									i_character_normal_pixels[x, y] = (255, 255, 255, 0)

						i_character_normal.save(self.PATTERN_FILE_CHARACTER % (path_font_normal, int(matrix_index)))
						i_font_normal.paste(i_character_normal, ((int(matrix_index) % 16) * font.content.height, (int(matrix_index) // 16) * font.content.height))

						# normal link
						i_character_normal_link = Image.new("RGBA", (i_character_normal_width, i_character_normal_height), (255, 255, 255, 0))
						i_character_normal_link.paste(i_character_normal)
						i_character_normal_link_pixels = i_character_normal_link.load()
						i_character_normal_link_width, i_character_normal_link_height = i_character_normal_link.size

						for x in range(i_character_normal_link_width):
							for y in range(i_character_normal_link_height):
								pixel_r, pixel_g, pixel_b, pixel_a = i_character_normal_link_pixels[x, y]
								i_character_normal_link_pixels[x, y] = (pixel_r, 0, 0, pixel_a)

						i_character_normal_link.save(self.PATTERN_FILE_CHARACTER % (path_font_normal_link, int(matrix_index)))
						i_font_normal_link.paste(i_character_normal_link, ((int(matrix_index) % 16) * font.content.height, (int(matrix_index) // 16) * font.content.height))

						# bold
						i_character_bold = Image.new("RGBA", (i_character_normal_width, i_character_normal_height), (255, 255, 255, 0))
						i_character_temp = Image.new("RGBA", (i_character_normal_width, i_character_normal_height), (255, 255, 255, 0))
						i_character_temp.paste(i_character_normal, (1, 0))
						i_character_bold = Image.alpha_composite(i_character_bold, i_character_temp)
						i_character_bold = Image.alpha_composite(i_character_bold, i_character_normal)
						i_character_bold.save(self.PATTERN_FILE_CHARACTER % (path_font_bold, int(matrix_index)))
						i_font_bold.paste(i_character_bold, ((int(matrix_index) % 16) * font.content.height, (int(matrix_index) // 16) * font.content.height))

						# bold link
						i_character_bold_link = Image.new("RGBA", (i_character_normal_width, i_character_normal_height), (255, 255, 255, 0))
						i_character_bold_link.paste(i_character_bold)
						i_character_bold_link_pixels = i_character_bold_link.load()
						i_character_bold_link_width, i_character_bold_link_height = i_character_bold_link.size

						for x in range(i_character_bold_link_width):
							for y in range(i_character_bold_link_height):
								pixel_r, pixel_g, pixel_b, pixel_a = i_character_bold_link_pixels[x, y]
								i_character_bold_link_pixels[x, y] = (pixel_r, 0, 0, pixel_a)

						i_character_bold_link.save(self.PATTERN_FILE_CHARACTER % (path_font_bold_link, int(matrix_index)))
						i_font_bold_link.paste(i_character_bold_link, ((int(matrix_index) % 16) * font.content.height, (int(matrix_index) // 16) * font.content.height))

						# italic
						i_character_italic = Image.new("RGBA", (i_character_normal_width, i_character_normal_height), (255, 255, 255, 0))
						i_character_temp = i_character_normal.crop((0, 0, i_character_normal_width, i_character_normal_height / 3))
						i_character_italic.paste(i_character_temp, (2, 0))
						i_character_temp = i_character_normal.crop((0, i_character_normal_height / 3, i_character_normal_width, (i_character_normal_height / 3) * 2))
						i_character_italic.paste(i_character_temp, (1, i_character_normal_height / 3))
						i_character_temp = i_character_normal.crop((0, (i_character_normal_height / 3) * 2, i_character_normal_width, (i_character_normal_height / 3) * 3))
						i_character_italic.paste(i_character_temp, (0, (i_character_normal_height / 3) * 2))
						i_character_italic.save(self.PATTERN_FILE_CHARACTER % (path_font_italic, int(matrix_index)))
						i_font_italic.paste(i_character_italic, ((int(matrix_index) % 16) * font.content.height, (int(matrix_index) // 16) * font.content.height))

						# italic link
						i_character_italic_link = Image.new("RGBA", (i_character_normal_width, i_character_normal_height), (255, 255, 255, 0))
						i_character_italic_link.paste(i_character_italic)
						i_character_italic_link_pixels = i_character_italic_link.load()
						i_character_italic_link_width, i_character_italic_link_height = i_character_italic_link.size

						for x in range(i_character_italic_link_width):
							for y in range(i_character_italic_link_height):
								pixel_r, pixel_g, pixel_b, pixel_a = i_character_italic_link_pixels[x, y]
								i_character_italic_link_pixels[x, y] = (pixel_r, 0, 0, pixel_a)

						i_character_italic_link.save(self.PATTERN_FILE_CHARACTER % (path_font_italic_link, int(matrix_index)))
						i_font_italic_link.paste(i_character_italic_link, ((int(matrix_index) % 16) * font.content.height, (int(matrix_index) // 16) * font.content.height))

				i_font_normal.save(self.PATTERN_FILE_FONT_NORMAL % int(font_index))
				i_font_normal_link.save(self.PATTERN_FILE_FONT_NORMAL_LINK % int(font_index))
				i_font_bold.save(self.PATTERN_FILE_FONT_BOLD % int(font_index))
				i_font_bold_link.save(self.PATTERN_FILE_FONT_BOLD_LINK % int(font_index))
				i_font_italic.save(self.PATTERN_FILE_FONT_ITALIC % int(font_index))
				i_font_italic_link.save(self.PATTERN_FILE_FONT_ITALIC_LINK % int(font_index))

				if status:
					self.items_hit += 1
				else:
					self.items_miss += 1



	def fill_meta(self):
		super(FontsRemaker, self).fill_meta()

		self.meta_remaked.fonts = ObjDict()

		for font_index, font in self.meta_decompiled.data.fonts.iteritems():
			if font.content:
				data_variants = ObjDict()

				path_font_normal = self.PATTERN_PATH_FONT_NORMAL % int(font_index)
				path_font_normal_link = self.PATTERN_PATH_FONT_NORMAL_LINK % int(font_index)
				path_font_bold = self.PATTERN_PATH_FONT_BOLD % int(font_index)
				path_font_bold_link = self.PATTERN_PATH_FONT_BOLD_LINK % int(font_index)
				path_font_italic = self.PATTERN_PATH_FONT_ITALIC % int(font_index)
				path_font_italic_link = self.PATTERN_PATH_FONT_ITALIC_LINK % int(font_index)

				data_font_normal = ObjDict()
				data_font_normal.height = font.content.height
				data_font_normal.asset = (self.PATTERN_FILE_FONT_NORMAL % int(font_index)).replace(self.PATH_PHASE_REMAKED, "remaked://")
				data_font_normal.characters = ObjDict()

				data_font_normal_link = ObjDict()
				data_font_normal_link.height = font.content.height
				data_font_normal_link.asset = (self.PATTERN_FILE_FONT_NORMAL_LINK % int(font_index)).replace(self.PATH_PHASE_REMAKED, "remaked://")
				data_font_normal_link.characters = ObjDict()

				data_font_bold = ObjDict()
				data_font_bold.height = font.content.height
				data_font_bold.asset = (self.PATTERN_FILE_FONT_BOLD % int(font_index)).replace(self.PATH_PHASE_REMAKED, "remaked://")
				data_font_bold.characters = ObjDict()

				data_font_bold_link = ObjDict()
				data_font_bold_link.height = font.content.height
				data_font_bold_link.asset = (self.PATTERN_FILE_FONT_BOLD_LINK % int(font_index)).replace(self.PATH_PHASE_REMAKED, "remaked://")
				data_font_bold_link.characters = ObjDict()

				data_font_italic = ObjDict()
				data_font_italic.height = font.content.height
				data_font_italic.asset = (self.PATTERN_FILE_FONT_ITALIC % int(font_index)).replace(self.PATH_PHASE_REMAKED, "remaked://")
				data_font_italic.characters = ObjDict()

				data_font_italic_link = ObjDict()
				data_font_italic_link.height = font.content.height
				data_font_italic_link.asset = (self.PATTERN_FILE_FONT_ITALIC_LINK % int(font_index)).replace(self.PATH_PHASE_REMAKED, "remaked://")
				data_font_italic_link.characters = ObjDict()

				for matrix_index, matrix in font.content.matrices.iteritems():
					if matrix.content:
						data_matrix_normal = ObjDict()
						data_matrix_normal.width = font.content.characters[matrix_index].computed_width
						data_matrix_normal.asset = (self.PATTERN_FILE_CHARACTER % (path_font_normal, int(matrix_index))).replace(self.PATH_PHASE_REMAKED, "remaked://")

						data_matrix_normal_link = ObjDict()
						data_matrix_normal_link.width = font.content.characters[matrix_index].computed_width
						data_matrix_normal_link.asset = (self.PATTERN_FILE_CHARACTER % (path_font_normal_link, int(matrix_index))).replace(self.PATH_PHASE_REMAKED, "remaked://")

						data_matrix_bold = ObjDict()
						data_matrix_bold.width = font.content.characters[matrix_index].computed_width
						data_matrix_bold.asset = (self.PATTERN_FILE_CHARACTER % (path_font_bold, int(matrix_index))).replace(self.PATH_PHASE_REMAKED, "remaked://")

						data_matrix_bold_link = ObjDict()
						data_matrix_bold_link.width = font.content.characters[matrix_index].computed_width
						data_matrix_bold_link.asset = (self.PATTERN_FILE_CHARACTER % (path_font_bold_link, int(matrix_index))).replace(self.PATH_PHASE_REMAKED, "remaked://")

						data_matrix_italic = ObjDict()
						data_matrix_italic.width = font.content.characters[matrix_index].computed_width
						data_matrix_italic.asset = (self.PATTERN_FILE_CHARACTER % (path_font_italic, int(matrix_index))).replace(self.PATH_PHASE_REMAKED, "remaked://")

						data_matrix_italic_link = ObjDict()
						data_matrix_italic_link.width = font.content.characters[matrix_index].computed_width
						data_matrix_italic_link.asset = (self.PATTERN_FILE_CHARACTER % (path_font_italic_link, int(matrix_index))).replace(self.PATH_PHASE_REMAKED, "remaked://")

						data_font_normal.characters[matrix_index] = data_matrix_normal
						data_font_normal_link.characters[matrix_index] = data_matrix_normal_link
						data_font_bold.characters[matrix_index] = data_matrix_bold
						data_font_bold_link.characters[matrix_index] = data_matrix_bold_link
						data_font_italic.characters[matrix_index] = data_matrix_italic
						data_font_italic_link.characters[matrix_index] = data_matrix_italic_link

				data_variants.normal = data_font_normal
				data_variants.normal_link = data_font_normal_link
				data_variants.bold = data_font_bold
				data_variants.bold_link = data_font_bold_link
				data_variants.italic = data_font_italic
				data_variants.italic_link = data_font_italic_link

				self.meta_remaked.fonts[font_index] = data_variants
