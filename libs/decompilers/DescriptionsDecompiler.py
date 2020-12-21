# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
from .CommonDecompiler import CommonDecompiler


class DescriptionsDecompiler(CommonDecompiler):

	PATTERN_PATH_DESCRIPTION = "%s%04d/"
	PATTERN_PATH_TITLE = "%s%04d/title/"

	PATTERN_FILE_TITLE = "%s%04d/title/content.bin"

	PATTERN_DECOMPILED_TITLE = "decompiled://%s/%s/%s/%04d/title/content.bin"


	def fill_meta_fat(self):
		self.meta.fat = ObjDict()
		self.meta.fat.foo_1 = self.library.fat.foo_1
		self.meta.fat.foo_2 = self.library.fat.foo_2
		self.meta.fat.foo_3 = self.library.fat.foo_3
		self.meta.fat.foo_4 = self.library.fat.foo_4
		self.meta.fat.offsets = ObjDict()

		for offset_index, offset in enumerate(tqdm(self.library.fat.offsets, desc="fat.offsets", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
			self.meta.fat.offsets[str(offset_index)] = offset


	def fill_meta_data(self):
		super(DescriptionsDecompiler, self).fill_meta_data()

		self.meta.data.descriptions = ObjDict()

		for description_index, description in enumerate(tqdm(self.library.data.descriptions, desc="data.descriptions", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
			data_description = ObjDict()
			data_description.param_offset = description.param_offset
			data_description.content = ObjDict()

			if description.content:
				path_description = self.PATTERN_PATH_DESCRIPTION % (self.PATH_DATA, description_index)

				if not os.path.exists(path_description):
					os.makedirs(path_description)

				data_description.content.data = ObjDict()

				file_title = self.PATTERN_FILE_TITLE % (self.PATH_DATA, description_index)
				path_title = self.PATTERN_PATH_TITLE % (self.PATH_DATA, description_index)
				if not os.path.exists(path_title):
					os.makedirs(path_title)

				data_description.content.data.title = self.PATTERN_DECOMPILED_TITLE % (self.issue.number, self.source.library, self.source_index, description_index)

				with open(file_title, "wb") as f:
					f.write(description.content.data.title)

			self.meta.data.descriptions[str(description_index)] = data_description
