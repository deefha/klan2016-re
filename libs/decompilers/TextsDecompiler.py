# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
import collections, gc, humanize, re, struct
from .CommonDecompiler import CommonDecompiler

# structs imports
from structs.klan_text_v1 import KlanTextV1
from structs.klan_text_v2 import KlanTextV2
from structs.klan_text_v3 import KlanTextV3
from structs.klan_text_v4 import KlanTextV4
from structs.klan_text_v5 import KlanTextV5
from structs.klan_text_v6 import KlanTextV6


class TextsDecompiler(CommonDecompiler):

	def __init__(self, issue, source, source_index):
		super(TextsDecompiler, self).__init__(issue, source, source_index)

		self.PATTERN_PATH_PALETTETABLE = "%s%03d/%d/palettetable/%04d/"
		self.PATTERN_PATH_ROW = "%s%03d/%d/linetable/%04d/pieces/%04d/rows/"
		self.PATTERN_PATH_TITLE = "%s%03d/%d/title/"
		self.PATTERN_PATH_CONTENT = "%s%03d/%d/"

		self.PATTERN_FILE_PALETTETABLE = "%s%03d/%d/palettetable/%04d/content.bin"
		self.PATTERN_FILE_ROW = "%s%03d/%d/linetable/%04d/pieces/%04d/rows/%02d.bin"
		self.PATTERN_FILE_TITLE = "%s%03d/%d/title/content.bin"
		self.PATTERN_FILE_DATA = "%s%03d/%d/content.bin"
		self.PATTERN_FILE_TEXT = "%s%03d.json"

		self.PATTERN_DECOMPILED_PALETTETABLE = "decompiled://%s/%s/%s/%03d/%d/palettetable/%04d/content.bin"
		self.PATTERN_DECOMPILED_ROW = "decompiled://%s/%s/%s/%03d/%d/linetable/%04d/pieces/%04d/rows/%02d.bin"
		self.PATTERN_DECOMPILED_TITLE = "decompiled://%s/%s/%s/%03d/%d/title/content.bin"
		self.PATTERN_DECOMPILED_DATA = "decompiled://%s/%s/%s/%03d/%d/content.bin"
		self.PATTERN_DECOMPILED_TEXT = "decompiled://%s/%s/%s/%03d.json"

		self.counts = ObjDict()


	def _variant_content_init(self):
		self.data_variant.content.offset_linktable = self.variant_content.offset_linktable
		self.data_variant.content.count_linktable = self.variant_content.count_linktable
		self.data_variant.content.linktable_meta = ObjDict()
		self.data_variant.content.linktable = ObjDict()
		self.data_variant.content.count_linetable_meta = self.variant_content.count_linetable_meta
		self.data_variant.content.offset_linetable_meta = self.variant_content.offset_linetable_meta
		self.data_variant.content.linetable_meta = ObjDict()
		self.data_variant.content.count_palettetable = self.variant_content.count_palettetable
		self.data_variant.content.offset_palettetable = self.variant_content.offset_palettetable
		self.data_variant.content.palettetable = ObjDict()
		self.data_variant.content.linetable = ObjDict()


	def _variant_content_linktable_meta(self):
		if self.variant_content.linktable_meta:
			for linktable_meta_index, linktable_meta in enumerate(tqdm(self.variant_content.linktable_meta, desc="linktable_meta", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
				data_linktable_meta = ObjDict()
				data_linktable_meta.param_offset = linktable_meta.param_offset
				data_linktable_meta.content = ObjDict()

				data_linktable_meta.content.topleft_x = linktable_meta.content.topleft_x
				data_linktable_meta.content.topleft_y = linktable_meta.content.topleft_y
				data_linktable_meta.content.bottomright_x = linktable_meta.content.bottomright_x
				data_linktable_meta.content.bottomright_y = linktable_meta.content.bottomright_y
				data_linktable_meta.content.offset = linktable_meta.content.offset

				self.data_variant.content.linktable_meta[str(linktable_meta_index)] = data_linktable_meta


	def _variant_content_linktable(self):
		if self.variant_content.linktable:
			for linktable_index, linktable in enumerate(tqdm(self.variant_content.linktable, desc="linktable", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
				data_linktable = ObjDict()
				data_linktable.param_offset = linktable.param_offset
				data_linktable.param_length = linktable.param_length
				data_linktable.content = ObjDict()
				data_linktable.content.macros = ObjDict()

				#if self.source.version <= 4:
					#data_linktable.content.events = linktable.content.events

				if linktable.content:
					for linktable_content_macro_index, linktable_content_macro in enumerate(linktable.content.macros):
						self.macro_index = linktable_content_macro_index
						data_linktable_content_macro = self._parse_macro(linktable_content_macro)
						data_linktable.content.macros[str(linktable_content_macro_index)] = data_linktable_content_macro

				self.data_variant.content.linktable[str(linktable_index)] = data_linktable


	def _variant_content_linetable_meta(self):
		if self.variant_content.linetable_meta:
			for linetable_meta_index, linetable_meta in enumerate(tqdm(self.variant_content.linetable_meta, desc="linetable_meta", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
				data_linetable_meta = ObjDict()
				data_linetable_meta.param_offset = linetable_meta.param_offset
				data_linetable_meta.content = ObjDict()

				data_linetable_meta.content.offset = linetable_meta.content.offset
				data_linetable_meta.content.height = linetable_meta.content.height
				data_linetable_meta.content.top = linetable_meta.content.top
				#data_linetable_meta.content.foo = linetable_meta.content.foo # TODO
				data_linetable_meta.content.foo = ''

				self.data_variant.content.linetable_meta[str(linetable_meta_index)] = data_linetable_meta


	def _variant_content_palettetable(self):
		if self.variant_content.palettetable:
			for palettetable_index, palettetable in enumerate(tqdm(self.variant_content.palettetable, desc="palettetable", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
				data_palettetable = ObjDict()
				data_palettetable.param_offset = palettetable.param_offset
				data_palettetable.content = ObjDict()

				file_palettetable = self.PATTERN_FILE_PALETTETABLE % (self.PATH_DATA, self.text_index, self.variant_index, palettetable_index)

				path_palettetable = self.PATTERN_PATH_PALETTETABLE % (self.PATH_DATA, self.text_index, self.variant_index, palettetable_index)

				if not os.path.exists(path_palettetable):
					os.makedirs(path_palettetable)

				data_palettetable.content.data = self.PATTERN_DECOMPILED_PALETTETABLE % (self.issue.number, self.source.library, self.source_index, self.text_index, self.variant_index, palettetable_index)

				with open(file_palettetable, "wb") as f:
					f.write(palettetable.content)

				self.data_variant.content.palettetable[str(palettetable_index)] = data_palettetable


	def _variant_content_linetable(self):
		if self.variant_content.linetable:
			for linetable_index, linetable in enumerate(tqdm(self.variant_content.linetable, desc="linetable", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
				data_linetable = ObjDict()
				data_linetable.param_offset = linetable.param_offset
				data_linetable.param_length = linetable.param_length
				data_linetable.content = ObjDict()
				data_linetable.content.pieces = ObjDict()

				for linetable_content_piece_index, linetable_content_piece in enumerate(linetable.content.pieces):
					data_linetable_content_piece = ObjDict()
					data_linetable_content_piece.raw = linetable_content_piece.raw

					if hasattr(linetable_content_piece, "data"):
						data_linetable_content_piece.data = ObjDict()

						if data_linetable_content_piece.raw == 1:
							data_linetable_content_piece.data.mode = linetable_content_piece.data.mode

						elif data_linetable_content_piece.raw == 8 or data_linetable_content_piece.raw == 10 or data_linetable_content_piece.raw == 11 or data_linetable_content_piece.raw == 12:
							data_linetable_content_piece.data.table = linetable_content_piece.data.table
							data_linetable_content_piece.data.width = linetable_content_piece.data.width
							data_linetable_content_piece.data.height = linetable_content_piece.data.height
							data_linetable_content_piece.data.rows = ObjDict()

							for row_index, row in enumerate(linetable_content_piece.data.rows):
								file_row = self.PATTERN_FILE_ROW % (self.PATH_DATA, self.text_index, self.variant_index, linetable_index, linetable_content_piece_index, row_index)

								path_row = self.PATTERN_PATH_ROW % (self.PATH_DATA, self.text_index, self.variant_index, linetable_index, linetable_content_piece_index)

								if not os.path.exists(path_row):
									os.makedirs(path_row)

								data_linetable_content_piece.data.rows[str(row_index)] = self.PATTERN_DECOMPILED_ROW % (self.issue.number, self.source.library, self.source_index, self.text_index, self.variant_index, linetable_index, linetable_content_piece_index, row_index)

								row_content_data = []
								for row_content in row.content:
									row_content_data.append(row_content.data)
									if hasattr(row_content, "addon"):
										row_content_data.append(row_content.addon)

								with open(file_row, "wb") as f:
									f.write(struct.pack("%sB" % len(row_content_data), *row_content_data))

						elif data_linetable_content_piece.raw == 9:
							data_linetable_content_piece.data.id = linetable_content_piece.data.id

						elif data_linetable_content_piece.raw == 32:
							data_linetable_content_piece.data.length = linetable_content_piece.data.length

					data_linetable.content.pieces[str(linetable_content_piece_index)] = data_linetable_content_piece

				self.data_variant.content.linetable[str(linetable_index)] = data_linetable


	def _variant_content_title(self):
		if self.source.version > 3:
			file_title = self.PATTERN_FILE_TITLE % (self.PATH_DATA, self.text_index, self.variant_index)
			path_title = self.PATTERN_PATH_TITLE % (self.PATH_DATA, self.text_index, self.variant_index)
			if not os.path.exists(path_title):
				os.makedirs(path_title)

			self.data_variant.content.title = self.PATTERN_DECOMPILED_TITLE % (self.issue.number, self.source.library, self.source_index, self.text_index, self.variant_index)

			with open(file_title, "wb") as f:
				f.write(self.variant_content.title)


	def _variant_content_data(self):
		file_data = self.PATTERN_FILE_DATA % (self.PATH_DATA, self.text_index, self.variant_index)
		path_data = self.PATTERN_PATH_CONTENT % (self.PATH_DATA, self.text_index, self.variant_index)
		if not os.path.exists(path_data):
			os.makedirs(path_data)

		self.data_variant.content.data = self.PATTERN_DECOMPILED_DATA % (self.issue.number, self.source.library, self.source_index, self.text_index, self.variant_index)

		with open(file_data, "wb") as f:
			f.write(self.variant_content.data)


	def fill_meta_data(self):
		if self.source.version == 1:
			if not hasattr(self.meta, "data"):
				self.meta.data = ObjDict()

			if not hasattr(self.meta.data, "texts"):
				self.meta.data.texts = ObjDict()
		else:
			super(TextsDecompiler, self).fill_meta_data()
			self.meta.data.texts = ObjDict()

		if self.source.version == 1:
			self.text_index = self.iso_path_index
			self.data_variant = ObjDict()
			self.data_variant.content = ObjDict()
			self.variant_content = self.library
			self.variant_index = 0

			self._variant_content_init()
			self._variant_content_linktable_meta()
			self._variant_content_linktable()
			self._variant_content_linetable_meta()
			self._variant_content_palettetable()
			self._variant_content_linetable()
			self._variant_content_title()

			with open(self.PATTERN_FILE_TEXT % (self.PATH_DATA, self.text_index), "w") as f:
				f.write(self.data_variant.content.dumps())

			self.meta.data.texts[str(self.text_index)] = self.PATTERN_DECOMPILED_TEXT % (self.issue.number, self.source.library, self.source_index, self.text_index)

		else:
			for text_index, text in enumerate(tqdm(self.library.data.texts, desc="data.texts", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
				data_text = ObjDict()
				data_text.param_offset_1 = text.param_offset_1
				data_text.param_offset_2 = text.param_offset_2
				data_text.param_offset_3 = text.param_offset_3
				data_text.param_offset_4 = text.param_offset_4
				data_text.variants = ObjDict()

				for variant_index, variant in enumerate(text.variants):
					self.text_index = text_index
					self.data_variant = ObjDict()
					self.data_variant.param_offset = variant.param_offset
					self.data_variant.param_offset = variant.param_length
					self.data_variant.content = ObjDict()

					if variant.content:
						self.variant_index = variant_index

						#self.variant_content = variant.content
						#self._variant_content_data()

						if self.variant_index == 0 or self.variant_index == 1:
							if self.source.version == 2:
								self.variant_content = KlanTextV1.from_bytes(variant.content.data)
							if self.source.version == 3:
								self.variant_content = KlanTextV2.from_bytes(variant.content.data)
							if self.source.version == 4:
								self.variant_content = KlanTextV3.from_bytes(variant.content.data)
							if self.source.version == 5:
								self.variant_content = KlanTextV4.from_bytes(variant.content.data)
							if self.source.version == 6:
								self.variant_content = KlanTextV5.from_bytes(variant.content.data)
							if self.source.version == 7:
								self.variant_content = KlanTextV6.from_bytes(variant.content.data)

							self._variant_content_init()
							self._variant_content_linktable_meta()
							self._variant_content_linktable()
							self._variant_content_linetable_meta()
							self._variant_content_palettetable()
							self._variant_content_linetable()
							self._variant_content_title()
						else:
							self.variant_content = variant.content
							self._variant_content_data()

						data_text.variants[str(variant_index)] = self.data_variant

				if data_text.variants:
					with open(self.PATTERN_FILE_TEXT % (self.PATH_DATA, text_index), "w") as f:
						f.write(data_text.dumps())

					self.meta.data.texts[str(text_index)] = self.PATTERN_DECOMPILED_TEXT % (self.issue.number, self.source.library, self.source_index, text_index)
				else:
					self.meta.data.texts[str(text_index)] = None

		for count_index, count in collections.OrderedDict(sorted(self.counts.items())).items():
			print("Type %s: %s" % (count_index, count))


	def fill_meta_header(self):
		if self.source.version == 1:
			self.meta.header = ObjDict()
		else:
			super(TextsDecompiler, self).fill_meta_header()


	def fill_meta_fat(self):
		if self.source.version == 1:
			if not hasattr(self.meta, "fat"):
				self.meta.fat = ObjDict()

			data_fat = ObjDict()

			regex = re.compile("^\/(.*);1$")
			data_fat.name = re.search(regex, self.iso_path).group(1)

			self.meta.fat[str(self.iso_path_index)] = data_fat
		else:
			self.meta.fat = ObjDict()
			self.meta.fat.count = self.library.fat.count
			self.meta.fat.offsets = ObjDict()

			#all_bytes = maketrans("", "")

			for offset_index, offset in enumerate(tqdm(self.library.fat.offsets, desc="fat.offsets", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
				data_offset = ObjDict()
				#data_offset.name = offset.name.decode('utf-8').translate(all_bytes, all_bytes[:32])
				data_offset.name = offset.name.decode().rstrip('\x00')
				data_offset.offset_1 = offset.offset_1
				data_offset.offset_2 = offset.offset_2
				data_offset.offset_3 = offset.offset_3
				data_offset.offset_4 = offset.offset_4

				self.meta.fat.offsets[str(offset_index)] = data_offset
