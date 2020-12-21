# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
import collections
from .CommonDecompiler import CommonDecompiler


class ScreensDecompiler(CommonDecompiler):

	def __init__(self, issue, source, source_index):
		super(ScreensDecompiler, self).__init__(issue, source, source_index)

		self.PATTERN_FILE_SCREEN = "%s%03d.json"

		self.PATTERN_DECOMPILED_SCREEN = "decompiled://%s/%s/%s/%03d.json"

		self.counts = ObjDict()


	def fill_meta_data(self):
		super(ScreensDecompiler, self).fill_meta_data()

		self.meta.data.screens = ObjDict()

		for self.screen_index, self.screen in enumerate(tqdm(self.library.data.screens, desc="data.screens", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
			data_screen = ObjDict()
			data_screen.param_offset = self.screen.param_offset
			data_screen.content = ObjDict()

			if self.screen.content:
				data_screen.content.type_1 = self.screen.content.type_1
				data_screen.content.type_2 = self.screen.content.type_2
				data_screen.content.foo = self.screen.content.foo

				data_screen.content.data = ObjDict()
				data_screen.content.data.macros = ObjDict()
				data_screen.content.data.events = ObjDict()

				for self.macro_index, self.macro in enumerate(self.screen.content.data.macros):
					data_macro = self._parse_macro(self.macro)
					data_screen.content.data.macros[str(self.macro_index)] = data_macro

				for self.event_index, self.event in enumerate(self.screen.content.data.events):
					data_event = ObjDict()
					data_event.binding = self.event.binding

					if hasattr(self.event, "content"):
						data_event.content = ObjDict()
						data_event.content.data_length = self.event.content.data_length
						data_event.content.data = ObjDict()
						data_event.content.data.macros = ObjDict()

						for self.macro_index, self.macro in enumerate(self.event.content.data.macros):
							data_macro = self._parse_macro(self.macro)
							data_event.content.data.macros[str(self.macro_index)] = data_macro

					data_screen.content.data.events[str(self.event_index)] = data_event

				with open(self.PATTERN_FILE_SCREEN % (self.PATH_DATA, self.screen_index + 1), "w") as f:
					f.write(data_screen.dumps())

				self.meta.data.screens[str(self.screen_index + 1)] = self.PATTERN_DECOMPILED_SCREEN % (self.issue.number, self.source.library, self.source_index, self.screen_index + 1)

			else:
				self.meta.data.screens[str(self.screen_index + 1)] = None

		for count_index, count in collections.OrderedDict(sorted(self.counts.items())).items():
			print("Type %s: %s" % (count_index, count))


	def fill_meta_header(self):
		self.meta.header = ObjDict()
		self.meta.header.version = self.library.header.version
		self.meta.header.foo = self.library.header.foo


	def fill_meta_fat(self):
		self.meta.fat = ObjDict()
		self.meta.fat.offsets = ObjDict()

		for offset_index, offset in enumerate(tqdm(self.library.fat.offsets, desc="fat.offsets", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
			self.meta.fat.offsets[str(offset_index + 1)] = offset
