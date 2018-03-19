# -*- coding: utf-8 -*-

# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
from CommonDecompiler import CommonDecompiler



class FontsDecompiler(CommonDecompiler):

	PATTERN_PATH_MATRICES = "%s%02d/matrices/"

	PATTERN_FILE_COLORMAP = "%s%02d/colormap.bin"
	PATTERN_FILE_MATRIX = "%s%03d.bin"

	PATTERN_DECOMPILED_COLORMAP = "decompiled://%s/%s/%s/%02d/colormap.bin"
	PATTERN_DECOMPILED_MATRIX = "decompiled://%s/%s/%s/%02d/matrices/%03d.bin"



	def fill_meta_data(self):
		super(FontsDecompiler, self).fill_meta_data()

		self.meta.data.fonts = ObjDict()

		for font_index, font in enumerate(tqdm(self.library.data.fonts, desc="data.fonts", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
			data_font = ObjDict()
			data_font.param_offset = font.param_offset
			data_font.content = ObjDict()

			if font.content:
				#print "Font #%d: param_offset=%d, matrices_size=%d, height=%d, computed_matrices_offset=%d" % (font_index, font.param_offset, font.content.matrices_size, font.content.height, font.content.computed_matrices_offset)

				file_colormap = self.PATTERN_FILE_COLORMAP % (self.PATH_DATA, font_index)

				path_matrices = self.PATTERN_PATH_MATRICES % (self.PATH_DATA, font_index)

				if not os.path.exists(path_matrices):
					os.makedirs(path_matrices)

				data_font.content.matrices_size = font.content.matrices_size
				data_font.content.height = font.content.height
				data_font.content.computed_matrices_offset = font.content.computed_matrices_offset
				data_font.content.colormap = self.PATTERN_DECOMPILED_COLORMAP % (self.issue.number, self.source.library, self.source_index, font_index)
				data_font.content.characters = ObjDict()
				data_font.content.matrices = ObjDict()

				#print "\tColormap"
				with open(file_colormap, "wb") as f:
					f.write(font.content.colormap)

				#print "\tCharacters"
				#for character_index, character in enumerate(tqdm(font.content.characters, desc="font.content.characters", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
				for character_index, character in enumerate(font.content.characters):
					data_character = ObjDict()
					data_character.offset_and_width = character.offset_and_width
					data_character.computed_offset = character.computed_offset
					data_character.computed_width = character.computed_width

					#print "\t\tCharacter #%d: offset_and_width=%d, computed_offset=%d, computed_width=%d" % (character_index, character.offset_and_width, character.computed_offset, character.computed_width)

					data_font.content.characters[str(character_index)] = data_character

				#print "\tMatrices"
				#for matrix_index, matrix in enumerate(tqdm(font.content.matrices, desc="font.content.matrices", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
				for matrix_index, matrix in enumerate(font.content.matrices):
					data_matrix = ObjDict()
					data_matrix.param_offset = matrix.param_offset
					data_matrix.param_width = matrix.param_width
					data_matrix.param_height = matrix.param_height

					if matrix.content:
						#print "\t\tMatrix #%d: param_offset=%d, param_width=%d, param_height=%d" % (matrix_index, matrix.param_offset, matrix.param_width, matrix.param_height)

						data_matrix.content = self.PATTERN_DECOMPILED_MATRIX % (self.issue.number, self.source.library, self.source_index, font_index, matrix_index)

						file_matrix = self.PATTERN_FILE_MATRIX % (path_matrices, matrix_index)

						with open(file_matrix, "wb") as f:
							f.write(matrix.content)

					else:
						#print "\t\tMatrix #%d: param_offset=%d, param_width=%d, param_height=%d, no content" % (matrix_index, matrix.param_offset, matrix.param_width, matrix.param_height)

						data_matrix.content = ""

					data_font.content.matrices[str(matrix_index)] = data_matrix

			#else:
				#print "Font #%d: param_offset=%d, no content" % (font_index, font.param_offset)

			self.meta.data.fonts[str(font_index)] = data_font
