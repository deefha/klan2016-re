# -*- coding: utf-8 -*-

# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
import string
from CommonRemaker import CommonRemaker



class ScreensRemaker(CommonRemaker):

	def __init__(self, issue, source, source_index):
		super(ScreensRemaker, self).__init__(issue, source, source_index)

		self.CHARTABLE = u"ČüéďäĎŤčěĚĹÍľĺÄÁÉžŽôöÓůÚýÖÜŠĽÝŘťáíóúňŇŮÔšřŕŔ¼§▴▾                           Ë   Ï                 ß         ë   ï ±  ®©  °   ™   "
		self.fonts = ObjDict()

		self.PATTERN_PATH_SCREEN = "%s%s" % (self.PATH_DATA_REMAKED, "%03d/")

		self.PATTERN_FILE_TEXT_ASSET = "%s%d.png"
		self.PATTERN_FILE_TEXT_ASSET_INVERSE = "%s%d_inverse.png"
		self.PATTERN_FILE_TEXT_PLAIN = "%s%d.txt"



	def export_assets(self):
		return



	def fill_meta(self):
		super(ScreensRemaker, self).fill_meta()

		self.meta_remaked.screens = ObjDict()

		for self.screen_index, self.screen in tqdm(self.meta_decompiled.data.screens.iteritems(), total=len(self.meta_decompiled.data.screens), desc="fill_meta", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"):
			if self.screen:
				with open(self.screen.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "r") as f:
					#content = f.read()
					lines = f.readlines() # TODO
					content = ''.join(lines) # TODO
					screen_content = ObjDict(content)

				data_screen = ObjDict()
				data_screen.type_1 = screen_content.content.type_1
				data_screen.type_2 = screen_content.content.type_2
				data_screen.foo = screen_content.content.foo
				data_screen.macros = ObjDict()
				data_screen.events = ObjDict()

				for self.macro_index, self.macro in screen_content.content.data.macros.iteritems():
					data_macro = self._parse_macro(self.macro)
					data_screen.macros[str(self.macro_index)] = data_macro

				for event_index, event in screen_content.content.data.events.iteritems():
					data_event = ObjDict()
					data_event.binding = event.binding
					data_event.macros = ObjDict()

					if hasattr(event, "content"):
						for self.macro_index, self.macro in event.content.data.macros.iteritems():
							data_macro = self._parse_macro(self.macro)
							data_event.macros[str(self.macro_index)] = data_macro

						data_screen.events[str(event_index)] = data_event

				self.meta_remaked.screens[str(self.screen_index)] = data_screen
