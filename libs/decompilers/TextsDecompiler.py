# common imports
import datetime, os, re, struct, sys
from objdict import ObjDict
from tqdm import tqdm

# specific imports
from CommonDecompiler import CommonDecompiler



class TextsDecompiler(CommonDecompiler):

	PATTERN_PATH_PALETTETABLE = "%s%04d/palettetable/%04d/"
	PATTERN_PATH_ROW = "%s%04d/linetable/%04d/items/%04d/rows/"

	PATTERN_FILE_PALETTETABLE = "%s%04d/palettetable/%04d/content.bin"
	PATTERN_FILE_ROW = "%s%04d/linetable/%04d/items/%04d/rows/%02d.bin"

	PATTERN_DECOMPILED_PALETTETABLE = "decompiled://%s/%s/%s/%04d/palettetable/%04d/content.bin"
	PATTERN_DECOMPILED_ROW = "decompiled://%s/%s/%s/%04d/linetable/%04d/items/%04d/rows/%02d.bin"



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
			data_text = ObjDict()

			data_text.offset_linktable = self.library.offset_linktable
			data_text.count_linktable = self.library.count_linktable
			data_text.linktable_meta = ObjDict()
			data_text.linktable = ObjDict()
			data_text.count_linetable_meta = self.library.count_linetable_meta
			data_text.offset_linetable_meta = self.library.offset_linetable_meta
			data_text.linetable_meta = ObjDict()
			data_text.count_palettetable = self.library.count_palettetable
			data_text.offset_palettetable = self.library.offset_palettetable
			data_text.palettetable = ObjDict()
			data_text.linetable = ObjDict()

			if self.library.linktable_meta:
				for linktable_meta_index, linktable_meta in enumerate(tqdm(self.library.linktable_meta, desc="linktable_meta", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
					data_linktable_meta = ObjDict()
					data_linktable_meta.param_offset = linktable_meta.param_offset
					data_linktable_meta.content = ObjDict()

					data_linktable_meta.content.topleft_x = linktable_meta.content.topleft_x
					data_linktable_meta.content.topleft_y = linktable_meta.content.topleft_y
					data_linktable_meta.content.bottomright_x = linktable_meta.content.bottomright_x
					data_linktable_meta.content.bottomright_y = linktable_meta.content.bottomright_y
					data_linktable_meta.content.offset = linktable_meta.content.offset

					data_text.linktable_meta[str(linktable_meta_index)] = data_linktable_meta

			if self.library.linktable:
				for linktable_index, linktable in enumerate(tqdm(self.library.linktable, desc="linktable", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
					data_linktable = ObjDict()
					data_linktable.param_offset = linktable.param_offset
					data_linktable.param_length = linktable.param_length
					data_linktable.content = ObjDict()
					data_linktable.content.items = ObjDict()

					for linktable_content_item_index, linktable_content_item in enumerate(linktable.content.items):
						data_linktable_content_item = ObjDict()
						data_linktable_content_item.mode = linktable_content_item.mode
						data_linktable_content_item.data = ObjDict()

						if data_linktable_content_item.mode == 4:
							data_linktable_content_item.data.topleft_x = linktable_content_item.data.topleft_x
							data_linktable_content_item.data.topleft_y = linktable_content_item.data.topleft_y
							data_linktable_content_item.data.width = linktable_content_item.data.width
							data_linktable_content_item.data.height = linktable_content_item.data.height
							data_linktable_content_item.data.slider_topleft_x = linktable_content_item.data.slider_topleft_x
							data_linktable_content_item.data.slider_topleft_y = linktable_content_item.data.slider_topleft_y
							data_linktable_content_item.data.textfile_length = linktable_content_item.data.textfile_length
							data_linktable_content_item.data.textfile = linktable_content_item.data.textfile

						elif data_linktable_content_item.mode == 6:
							#data_linktable_content_item.data.foo = linktable_content_item.data.foo # TODO
							data_linktable_content_item.data.foo = ""

						elif data_linktable_content_item.mode == 12:
							data_linktable_content_item.data.foo_1 = linktable_content_item.data.foo_1
							data_linktable_content_item.data.foo_2 = linktable_content_item.data.foo_2

						elif data_linktable_content_item.mode == 13:
							data_linktable_content_item.data.id = linktable_content_item.data.id
							data_linktable_content_item.data.textfile_length = linktable_content_item.data.textfile_length
							data_linktable_content_item.data.textfile = linktable_content_item.data.textfile

						elif data_linktable_content_item.mode == 14:
							data_linktable_content_item.data.id = linktable_content_item.data.id
							data_linktable_content_item.data.value = linktable_content_item.data.value

						data_linktable.content.items[str(linktable_content_item_index)] = data_linktable_content_item

					data_text.linktable[str(linktable_index)] = data_linktable

			if self.library.linetable_meta:
				for linetable_meta_index, linetable_meta in enumerate(tqdm(self.library.linetable_meta, desc="linetable_meta", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
					data_linetable_meta = ObjDict()
					data_linetable_meta.param_offset = linetable_meta.param_offset
					data_linetable_meta.content = ObjDict()

					data_linetable_meta.content.offset = linetable_meta.content.offset
					data_linetable_meta.content.height = linetable_meta.content.height
					data_linetable_meta.content.top = linetable_meta.content.top
					data_linetable_meta.content.foo = ''
					#data_linetable_meta.content.foo = linetable_meta.content.foo # TODO

					data_text.linetable_meta[str(linetable_meta_index)] = data_linetable_meta

			if self.library.palettetable:
				for palettetable_index, palettetable in enumerate(tqdm(self.library.palettetable, desc="palettetable", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
					data_palettetable = ObjDict()
					data_palettetable.param_offset = palettetable.param_offset
					data_palettetable.content = ObjDict()

					file_palettetable = self.PATTERN_FILE_PALETTETABLE % (self.PATH_DATA, self.iso_path_index, palettetable_index)

					path_palettetable = self.PATTERN_PATH_PALETTETABLE % (self.PATH_DATA, self.iso_path_index, palettetable_index)

					if not os.path.exists(path_palettetable):
						os.makedirs(path_palettetable)

					data_palettetable.content.data = self.PATTERN_DECOMPILED_PALETTETABLE % (self.issue.number, self.source.library, self.source_index, self.iso_path_index, palettetable_index)

					with open(file_palettetable, "wb") as f:
						f.write(palettetable.content)

					data_text.palettetable[str(palettetable_index)] = data_palettetable

			if self.library.linetable:
				for linetable_index, linetable in enumerate(tqdm(self.library.linetable, desc="linetable", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
					data_linetable = ObjDict()
					data_linetable.param_offset = linetable.param_offset
					data_linetable.param_length = linetable.param_length
					data_linetable.content = ObjDict()
					data_linetable.content.items = ObjDict()

					for linetable_content_item_index, linetable_content_item in enumerate(linetable.content.items):
						data_linetable_content_item = ObjDict()
						data_linetable_content_item.raw = linetable_content_item.raw

						if hasattr(linetable_content_item, "data"):
							data_linetable_content_item.data = ObjDict()

							if data_linetable_content_item.raw == 1:
								data_linetable_content_item.data.mode = linetable_content_item.data.mode

							elif data_linetable_content_item.raw == 8:
								data_linetable_content_item.data.table = linetable_content_item.data.table
								data_linetable_content_item.data.width = linetable_content_item.data.width
								data_linetable_content_item.data.height = linetable_content_item.data.height
								data_linetable_content_item.data.rows = ObjDict()

								for row_index, row in enumerate(linetable_content_item.data.rows):
									file_row = self.PATTERN_FILE_ROW % (self.PATH_DATA, self.iso_path_index, linetable_index, linetable_content_item_index, row_index)

									path_row = self.PATTERN_PATH_ROW % (self.PATH_DATA, self.iso_path_index, linetable_index, linetable_content_item_index)

									if not os.path.exists(path_row):
										os.makedirs(path_row)

									data_linetable_content_item.data.rows[str(row_index)] = self.PATTERN_DECOMPILED_ROW % (self.issue.number, self.source.library, self.source_index, self.iso_path_index, linetable_index, linetable_content_item_index, row_index)

									row_content_data = []
									for row_content in row.content:
										row_content_data.append(row_content.data)
										if hasattr(row_content, "addon"):
											row_content_data.append(row_content.addon)

									with open(file_row, "wb") as f:
										f.write(struct.pack("%sB" % len(row_content_data), *row_content_data))

							elif data_linetable_content_item.raw == 9:
								data_linetable_content_item.data.id = linetable_content_item.data.id

							elif data_linetable_content_item.raw == 32:
								data_linetable_content_item.data.length = linetable_content_item.data.length

						data_linetable.content.items[str(linetable_content_item_index)] = data_linetable_content_item

					data_text.linetable[str(linetable_index)] = data_linetable

			self.meta.data.texts[str(self.iso_path_index)] = data_text



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
			super(TextsDecompiler, self).fill_meta_fat()
