# common imports
import os, sys, datetime
from objdict import ObjDict
from tqdm import tqdm

# specific imports
from CommonDecompiler import CommonDecompiler



class TextsDecompiler(CommonDecompiler):

	PATTERN_PATH_LINKTABLE = "%s%04d/linktable/%04d/"
	PATTERN_PATH_PALETTETABLE = "%s%04d/palettetable/%04d/"

	PATTERN_FILE_LINKTABLE = "%s%04d/linktable/%04d/content.bin"
	PATTERN_FILE_PALETTETABLE = "%s%04d/palettetable/%04d/content.bin"

	PATTERN_DECOMPILED_LINKTABLE = "decompiled://%s/%s/%s/%04d/linktable/%04d/content.bin"
	PATTERN_DECOMPILED_PALETTETABLE = "decompiled://%s/%s/%s/%04d/palettetable/%04d/content.bin"

	def fill_meta_data(self):
		if self.source.version == 1:
			if not hasattr(self.meta, 'data'):
				self.meta.data = ObjDict()

			if not hasattr(self.meta.data, 'texts'):
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

			if self.library.linktable_meta:
				for linktable_meta_index, linktable_meta in enumerate(self.library.linktable_meta):
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
				for linktable_index, linktable in enumerate(self.library.linktable):
					data_linktable = ObjDict()
					data_linktable.param_offset = linktable.param_offset
					data_linktable.param_length = linktable.param_length
					data_linktable.content = ObjDict()

					file_linktable = self.PATTERN_FILE_LINKTABLE % (self.PATH_DATA, self.iso_path_index, linktable_index)

					path_linktable = self.PATTERN_PATH_LINKTABLE % (self.PATH_DATA, self.iso_path_index, linktable_index)

					if not os.path.exists(path_linktable):
						os.makedirs(path_linktable)

					data_linktable.content.data = self.PATTERN_DECOMPILED_LINKTABLE % (self.issue.number, self.source.library, self.source_index, self.iso_path_index, linktable_index)

					with open(file_linktable, "wb") as f:
						f.write(linktable.content)

					data_text.linktable[str(linktable_index)] = data_linktable

			if self.library.linetable_meta:
				for linetable_meta_index, linetable_meta in enumerate(self.library.linetable_meta):
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
				for palettetable_index, palettetable in enumerate(self.library.palettetable):
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

			self.meta.data.texts[str(self.iso_path_index)] = data_text

		#for image_index, image in enumerate(tqdm(self.library.data.images, desc="data.images", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
			#data_image = ObjDict()
			#data_image.param_offset = image.param_offset
			#data_image.content = ObjDict()

			#if image.content:
				##print "Image #%d: param_offset=%d, data_size=%d, width=%d, height=%d, mode=%d" % (image_index, image.param_offset, image.content.data_size, image.content.width, image.content.height, image.content.mode)

				#file_colormap = self.PATTERN_FILE_COLORMAP % (self.PATH_DATA, image_index)
				#file_content = self.PATTERN_FILE_CONTENT % (self.PATH_DATA, image_index)
				#file_header = self.PATTERN_FILE_HEADER % (self.PATH_DATA, image_index)

				#path_image = self.PATTERN_PATH_IMAGE % (self.PATH_DATA, image_index)

				#if not os.path.exists(path_image):
					#os.makedirs(path_image)

				#data_image.content.data_size = image.content.data_size
				#data_image.content.width = image.content.width
				#data_image.content.height = image.content.height
				#data_image.content.mode = image.content.mode
				#data_image.content.data = ObjDict()
				#data_image.content.data.param_data_size = image.content.data.param_data_size

				#if image.content.mode == 1 or image.content.mode == 256 or image.content.mode == 257:
					#data_image.content.data.colormap = self.PATTERN_DECOMPILED_COLORMAP % (self.issue.number, self.source.library, self.source_index, image_index)

					##print "\tColormap"
					#with open(file_colormap, "wb") as f:
						#f.write(image.content.data.colormap)

				#elif image.content.mode == 4:
					#data_image.content.data.foo = image.content.data.foo
					#data_image.content.data.header_size = image.content.data.header_size
					#data_image.content.data.header = self.PATTERN_DECOMPILED_HEADER % (self.issue.number, self.source.library, self.source_index, image_index)

					##print "\tHeader"
					#with open(file_header, "wb") as f:
						#f.write(image.content.data.header)

				#data_image.content.data.content = self.PATTERN_DECOMPILED_CONTENT % (self.issue.number, self.source.library, self.source_index, image_index)

				##print "\tContent"
				#with open(file_content, "wb") as f:
					#f.write(image.content.data.content)

			##else:
				##print "Image #%d: param_offset=%d, no content" % (image_index, image.param_offset)

			#self.meta.data.images[str(image_index)] = data_image



	def fill_meta_header(self):
		if self.source.version == 1:
			self.meta.header = ObjDict()
		else:
			super(TextsDecompiler, self).fill_meta_header()



	def fill_meta_fat(self):
		if self.source.version == 1:
			self.meta.fat = ObjDict()
		else:
			super(TextsDecompiler, self).fill_meta_fat()
