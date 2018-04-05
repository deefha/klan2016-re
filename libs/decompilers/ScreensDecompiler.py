# -*- coding: utf-8 -*-

# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
import collections
from CommonDecompiler import CommonDecompiler



class ScreensDecompiler(CommonDecompiler):

	def __init__(self, issue, source, source_index):
		super(ScreensDecompiler, self).__init__(issue, source, source_index)

		self.PATTERN_FILE_SCREEN = "%s%04d.json"

		self.PATTERN_DECOMPILED_SCREEN = "decompiled://%s/%s/%s/%04d.json"

		self.counts = ObjDict()



	def _parse_macro(self, macro):
		data_macro = ObjDict()
		data_macro.type = macro.type

		macro_type_hex = "{0:#0{1}x}".format(macro.type, 6)
		if hasattr(self.counts, macro_type_hex):
			self.counts[macro_type_hex] += 1
		else:
			self.counts[macro_type_hex] = 1

		if hasattr(macro, "content"):
			data_macro.content = ObjDict()

			# doit
			if macro.type == 0x0001:
				data_macro.content.id = macro.content.id

			# text
			elif macro.type == 0x0004:
				data_macro.content.topleft_x = macro.content.topleft_x
				data_macro.content.topleft_y = macro.content.topleft_y
				data_macro.content.width = macro.content.width
				data_macro.content.height = macro.content.height
				data_macro.content.slider_topleft_x = macro.content.slider_topleft_x
				data_macro.content.slider_topleft_y = macro.content.slider_topleft_y
				data_macro.content.textfile_length = macro.content.textfile_length
				data_macro.content.textfile = macro.content.textfile
				if self.source.version >= 3:
					data_macro.content.foo = macro.content.foo

			# video
			elif macro.type == 0x0005:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2
				data_macro.content.foo_3 = macro.content.foo_3
				data_macro.content.foo_4 = macro.content.foo_4
				data_macro.content.foo_5 = macro.content.foo_5
				data_macro.content.foo_6 = macro.content.foo_6

			# obrazky
			elif macro.type == 0x0006:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2
				data_macro.content.foo_3 = macro.content.foo_3
				data_macro.content.foo_4 = macro.content.foo_4
				data_macro.content.foo_5 = macro.content.foo_5

			# zvuk
			elif macro.type == 0x0007:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2
				data_macro.content.foo_3 = macro.content.foo_3
				data_macro.content.foo_4 = macro.content.foo_4
				data_macro.content.foo_5 = macro.content.foo_5

			# button
			elif macro.type == 0x0009:
				data_macro.content.id = macro.content.id
				data_macro.content.image = macro.content.image
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.topleft_x = macro.content.topleft_x
				data_macro.content.topleft_y = macro.content.topleft_y
				data_macro.content.scancode = macro.content.scancode
				data_macro.content.hover_topleft_x = macro.content.hover_topleft_x
				data_macro.content.hover_topleft_y = macro.content.hover_topleft_y
				data_macro.content.hover_bottomright_x = macro.content.hover_bottomright_x
				data_macro.content.hover_bottomright_y = macro.content.hover_bottomright_y
				data_macro.content.foo_2 = macro.content.foo_2
				if self.source.version >= 3:
					data_macro.content.foo_3 = macro.content.foo_3

			# area
			elif macro.type == 0x000a:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2
				data_macro.content.foo_3 = macro.content.foo_3
				data_macro.content.foo_4 = macro.content.foo_4
				data_macro.content.foo_5 = macro.content.foo_5
				data_macro.content.foo_6 = macro.content.foo_6

			# event
			elif macro.type == 0x000b:
				data_macro.content.id = macro.content.id

			# gotopage
			elif macro.type == 0x000c:
				data_macro.content.id = macro.content.id
				if self.source.version >= 3:
					data_macro.content.foo = macro.content.foo

			# svar
			elif macro.type == 0x000d:
				data_macro.content.variable = macro.content.variable
				data_macro.content.value_length = macro.content.value_length
				data_macro.content.value = unicode(macro.content.value.replace('\\U', '\\\\U').replace('\\N', '\\\\N'), 'unicode-escape')

			# ivar / mov
			elif macro.type == 0x000e:
				data_macro.content.variable = macro.content.variable
				data_macro.content.value = macro.content.value

			# screen
			elif macro.type == 0x000f:
				data_macro.content.id = macro.content.id

			# keybutt
			elif macro.type == 0x0011:
				data_macro.content.topleft_x = macro.content.topleft_x
				data_macro.content.topleft_y = macro.content.topleft_y
				data_macro.content.image = macro.content.image
				data_macro.content.foo = macro.content.foo
				data_macro.content.scancode = macro.content.scancode

			# getchar
			elif macro.type == 0x0012:
				data_macro.content.id = macro.content.id

			# pic
			elif macro.type == 0x0013:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2
				if self.source.version <= 2:
					data_macro.content.foo_3 = macro.content.foo_3

			# demo
			elif macro.type == 0x0014:
				data_macro.content.textfile_length = macro.content.textfile_length
				data_macro.content.textfile = macro.content.textfile
				data_macro.content.foo = macro.content.foo

			# reklama
			elif macro.type == 0x0015:
				data_macro.content.topleft_x = macro.content.topleft_x
				data_macro.content.topleft_y = macro.content.topleft_y
				data_macro.content.bottomright_x = macro.content.bottomright_x
				data_macro.content.bottomright_y = macro.content.bottomright_y
				data_macro.content.image = macro.content.image
				data_macro.content.id = macro.content.id

			# keyevent
			elif macro.type == 0x0016:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2
				data_macro.content.foo_3 = macro.content.foo_3

			# snap
			elif macro.type == 0x0017:
				data_macro.content.foo = macro.content.foo

			# playwav
			elif macro.type == 0x0018:
				if self.source.version >= 2:
					data_macro.content.foo_1 = macro.content.foo_1
					data_macro.content.foo_2 = macro.content.foo_2
				else:
					data_macro.content.foo = macro.content.foo

			# image
			elif macro.type == 0x0020:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2
				data_macro.content.foo_3 = macro.content.foo_3
				data_macro.content.foo_4 = macro.content.foo_4
				if self.source.version >= 4:
					data_macro.content.foo_5 = macro.content.foo_5

			# ???
			elif macro.type == 0x0021:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2
				data_macro.content.foo_3 = macro.content.foo_3

			# ???
			elif macro.type == 0x0022:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2
				data_macro.content.foo_3 = macro.content.foo_3
				data_macro.content.foo_4 = macro.content.foo_4
				data_macro.content.foo_5 = macro.content.foo_5

			# curhelp
			elif macro.type == 0x0023:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2
				data_macro.content.foo_3 = macro.content.foo_3
				data_macro.content.foo_4 = macro.content.foo_4
				data_macro.content.text_length = macro.content.text_length
				data_macro.content.text = unicode(macro.content.text.replace('\\U', '\\\\U').replace('\\N', '\\\\N'), 'unicode-escape')
				data_macro.content.foo_5 = macro.content.foo_5

			# ???
			elif macro.type == 0x0024:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2

			# ???
			elif macro.type == 0x0025:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2

			# ???
			elif macro.type == 0x0026:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2

			# ???
			elif macro.type == 0x0027:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2

			# ???
			elif macro.type == 0x0028:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2
				data_macro.content.foo_3 = macro.content.foo_3

			# ???
			elif macro.type == 0x0029:
				data_macro.content.foo = macro.content.foo

			# ???
			elif macro.type == 0x002b:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2
				data_macro.content.foo_3 = macro.content.foo_3
				data_macro.content.foo_4 = macro.content.foo_4
				data_macro.content.foo_5 = macro.content.foo_5
				data_macro.content.foo_6 = macro.content.foo_6
				data_macro.content.foo_7 = macro.content.foo_7

			# ???
			elif macro.type == 0x002c:
				data_macro.content.foo = macro.content.foo
				data_macro.content.textfile_length = macro.content.textfile_length
				data_macro.content.textfile = unicode(macro.content.textfile.replace('\\U', '\\\\U').replace('\\N', '\\\\N'), 'unicode-escape')

			# ???
			elif macro.type == 0x002d:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2

			# link?
			elif macro.type == 0x0033:
				data_macro.content.text_1_length = macro.content.text_1_length
				data_macro.content.text_1 = unicode(macro.content.text_1.replace('\\U', '\\\\U').replace('\\N', '\\\\N'), 'unicode-escape')
				data_macro.content.text_2_length = macro.content.text_2_length
				data_macro.content.text_2 = unicode(macro.content.text_2.replace('\\U', '\\\\U').replace('\\N', '\\\\N'), 'unicode-escape')
				data_macro.content.foo = macro.content.foo

			# ???
			elif macro.type == 0x0035:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2
				data_macro.content.foo_3 = macro.content.foo_3
				data_macro.content.foo_4 = macro.content.foo_4
				data_macro.content.foo_5 = macro.content.foo_5
				data_macro.content.foo_6 = macro.content.foo_6
				data_macro.content.foo_7 = macro.content.foo_7
				data_macro.content.foo_8 = macro.content.foo_8

			# ???
			elif macro.type == 0x0036:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2
				data_macro.content.foo_3 = macro.content.foo_3

			# ???
			elif macro.type == 0x0037:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2
				data_macro.content.foo_3 = macro.content.foo_3
				data_macro.content.foo_4 = macro.content.foo_4

			# ???
			elif macro.type == 0x0038:
				data_macro.content.foo = macro.content.foo

			# if
			elif macro.type == 0x0063:
				data_macro.content.data_length_1 = macro.content.data_length_1
				data_macro.content.data_length_2 = macro.content.data_length_2
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2
				data_macro.content.branches = ObjDict()

				data_macro.content.branches.branch_if = ObjDict()
				data_macro.content.branches.branch_if.value_1 = macro.content.branches.branch_if.value_1
				data_macro.content.branches.branch_if.condition = macro.content.branches.branch_if.condition
				data_macro.content.branches.branch_if.value_2 = macro.content.branches.branch_if.value_2
				if hasattr(macro.content.branches.branch_if, "foo"):
					data_macro.content.branches.branch_if.foo = macro.content.branches.branch_if.foo
				data_macro.content.branches.branch_if.macros = ObjDict()

				for self.macro_inner_index, self.macro_inner in enumerate(macro.content.branches.branch_if.macros):
					data_macro_inner = self._parse_macro(self.macro_inner)
					data_macro.content.branches.branch_if.macros[str(self.macro_inner_index)] = data_macro_inner

				if hasattr(macro.content.branches, "branch_else"):
					data_macro.content.branches.branch_else = ObjDict()
					data_macro.content.branches.branch_else.macros = ObjDict()

					for self.macro_inner_index, self.macro_inner in enumerate(macro.content.branches.branch_else.macros):
						data_macro_inner = self._parse_macro(self.macro_inner)
						data_macro.content.branches.branch_else.macros[str(self.macro_inner_index)] = data_macro_inner
			# nokeys
			elif macro.type == 0x4f4e:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2

			else:
				print "Unknown macro type: %s" % (macro.type)
				sys.exit()

		else:
			if macro.type != 0x0010 and macro.type != 0x002a and macro.type != 0x003a and macro.type != 0xffff:
				print "Macro without content: %s (%s), screen %s, macro %s" % (macro.type, macro_type_hex, self.screen_index, self.macro_index)

		return data_macro



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

		for count_index, count in collections.OrderedDict(sorted(self.counts.iteritems())).iteritems():
			print "Type %s: %s" % (count_index, count)



	def fill_meta_header(self):
		self.meta.header = ObjDict()
		self.meta.header.version = self.library.header.version
		self.meta.header.foo = self.library.header.foo



	def fill_meta_fat(self):
		self.meta.fat = ObjDict()
		self.meta.fat.offsets = ObjDict()

		for offset_index, offset in enumerate(tqdm(self.library.fat.offsets, desc="fat.offsets", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
			self.meta.fat.offsets[str(offset_index + 1)] = offset
