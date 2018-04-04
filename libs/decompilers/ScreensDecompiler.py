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



	def _parse_command(self, command):
		data_command = ObjDict()
		data_command.type = command.type

		command_type_hex = "{0:#0{1}x}".format(command.type, 6)
		if hasattr(self.counts, command_type_hex):
			self.counts[command_type_hex] += 1
		else:
			self.counts[command_type_hex] = 1

		if hasattr(command, "content"):
			data_command.content = ObjDict()

			# doit
			if command.type == 0x0001:
				data_command.content.id = command.content.id

			# text
			elif command.type == 0x0004:
				data_command.content.topleft_x = command.content.topleft_x
				data_command.content.topleft_y = command.content.topleft_y
				data_command.content.width = command.content.width
				data_command.content.height = command.content.height
				data_command.content.slider_topleft_x = command.content.slider_topleft_x
				data_command.content.slider_topleft_y = command.content.slider_topleft_y
				data_command.content.textfile_length = command.content.textfile_length
				data_command.content.textfile = command.content.textfile
				if self.source.version >= 3:
					data_command.content.foo = command.content.foo

			# video
			elif command.type == 0x0005:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2
				data_command.content.foo_3 = command.content.foo_3
				data_command.content.foo_4 = command.content.foo_4
				data_command.content.foo_5 = command.content.foo_5
				data_command.content.foo_6 = command.content.foo_6

			# obrazky
			elif command.type == 0x0006:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2
				data_command.content.foo_3 = command.content.foo_3
				data_command.content.foo_4 = command.content.foo_4
				data_command.content.foo_5 = command.content.foo_5

			# zvuk
			elif command.type == 0x0007:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2
				data_command.content.foo_3 = command.content.foo_3
				data_command.content.foo_4 = command.content.foo_4
				data_command.content.foo_5 = command.content.foo_5

			# button
			elif command.type == 0x0009:
				data_command.content.id = command.content.id
				data_command.content.image = command.content.image
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.topleft_x = command.content.topleft_x
				data_command.content.topleft_y = command.content.topleft_y
				data_command.content.scancode = command.content.scancode
				data_command.content.hover_topleft_x = command.content.hover_topleft_x
				data_command.content.hover_topleft_y = command.content.hover_topleft_y
				data_command.content.hover_bottomright_x = command.content.hover_bottomright_x
				data_command.content.hover_bottomright_y = command.content.hover_bottomright_y
				data_command.content.foo_2 = command.content.foo_2
				if self.source.version >= 3:
					data_command.content.foo_3 = command.content.foo_3

			# area
			elif command.type == 0x000a:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2
				data_command.content.foo_3 = command.content.foo_3
				data_command.content.foo_4 = command.content.foo_4
				data_command.content.foo_5 = command.content.foo_5
				data_command.content.foo_6 = command.content.foo_6

			# event
			elif command.type == 0x000b:
				data_command.content.id = command.content.id

			# gotopage
			elif command.type == 0x000c:
				data_command.content.id = command.content.id
				if self.source.version >= 3:
					data_command.content.foo = command.content.foo

			# svar
			elif command.type == 0x000d:
				data_command.content.variable = command.content.variable
				data_command.content.value_length = command.content.value_length
				data_command.content.value = unicode(command.content.value.replace('\\U', '\\\\U').replace('\\N', '\\\\N'), 'unicode-escape')

			# ivar / mov
			elif command.type == 0x000e:
				data_command.content.variable = command.content.variable
				data_command.content.value = command.content.value

			# screen
			elif command.type == 0x000f:
				data_command.content.id = command.content.id

			# keybutt
			elif command.type == 0x0011:
				data_command.content.topleft_x = command.content.topleft_x
				data_command.content.topleft_y = command.content.topleft_y
				data_command.content.image = command.content.image
				data_command.content.foo = command.content.foo
				data_command.content.scancode = command.content.scancode

			# getchar
			elif command.type == 0x0012:
				data_command.content.id = command.content.id

			# pic
			elif command.type == 0x0013:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2
				if self.source.version <= 2:
					data_command.content.foo_3 = command.content.foo_3

			# demo
			elif command.type == 0x0014:
				data_command.content.textfile_length = command.content.textfile_length
				data_command.content.textfile = command.content.textfile
				data_command.content.foo = command.content.foo

			# reklama
			elif command.type == 0x0015:
				data_command.content.topleft_x = command.content.topleft_x
				data_command.content.topleft_y = command.content.topleft_y
				data_command.content.bottomright_x = command.content.bottomright_x
				data_command.content.bottomright_y = command.content.bottomright_y
				data_command.content.image = command.content.image
				data_command.content.id = command.content.id

			# keyevent
			elif command.type == 0x0016:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2
				data_command.content.foo_3 = command.content.foo_3

			# snap
			elif command.type == 0x0017:
				data_command.content.foo = command.content.foo

			# playwav
			elif command.type == 0x0018:
				if self.source.version >= 2:
					data_command.content.foo_1 = command.content.foo_1
					data_command.content.foo_2 = command.content.foo_2
				else:
					data_command.content.foo = command.content.foo

			# image
			elif command.type == 0x0020:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2
				data_command.content.foo_3 = command.content.foo_3
				data_command.content.foo_4 = command.content.foo_4
				if self.source.version >= 4:
					data_command.content.foo_5 = command.content.foo_5

			# ???
			elif command.type == 0x0021:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2
				data_command.content.foo_3 = command.content.foo_3

			# ???
			elif command.type == 0x0022:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2
				data_command.content.foo_3 = command.content.foo_3
				data_command.content.foo_4 = command.content.foo_4
				data_command.content.foo_5 = command.content.foo_5

			# curhelp
			elif command.type == 0x0023:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2
				data_command.content.foo_3 = command.content.foo_3
				data_command.content.foo_4 = command.content.foo_4
				data_command.content.text_length = command.content.text_length
				data_command.content.text = unicode(command.content.text.replace('\\U', '\\\\U').replace('\\N', '\\\\N'), 'unicode-escape')
				data_command.content.foo_5 = command.content.foo_5

			# ???
			elif command.type == 0x0024:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2

			# ???
			elif command.type == 0x0025:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2

			# ???
			elif command.type == 0x0026:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2

			# ???
			elif command.type == 0x0027:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2

			# ???
			elif command.type == 0x0028:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2
				data_command.content.foo_3 = command.content.foo_3

			# ???
			elif command.type == 0x0029:
				data_command.content.foo = command.content.foo

			# ???
			elif command.type == 0x002b:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2
				data_command.content.foo_3 = command.content.foo_3
				data_command.content.foo_4 = command.content.foo_4
				data_command.content.foo_5 = command.content.foo_5
				data_command.content.foo_6 = command.content.foo_6
				data_command.content.foo_7 = command.content.foo_7

			# ???
			elif command.type == 0x002c:
				data_command.content.foo = command.content.foo
				data_command.content.textfile_length = command.content.textfile_length
				data_command.content.textfile = unicode(command.content.textfile.replace('\\U', '\\\\U').replace('\\N', '\\\\N'), 'unicode-escape')

			# ???
			elif command.type == 0x002d:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2

			# link?
			elif command.type == 0x0033:
				data_command.content.text_1_length = command.content.text_1_length
				data_command.content.text_1 = unicode(command.content.text_1.replace('\\U', '\\\\U').replace('\\N', '\\\\N'), 'unicode-escape')
				data_command.content.text_2_length = command.content.text_2_length
				data_command.content.text_2 = unicode(command.content.text_2.replace('\\U', '\\\\U').replace('\\N', '\\\\N'), 'unicode-escape')
				data_command.content.foo = command.content.foo

			# ???
			elif command.type == 0x0035:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2
				data_command.content.foo_3 = command.content.foo_3
				data_command.content.foo_4 = command.content.foo_4
				data_command.content.foo_5 = command.content.foo_5
				data_command.content.foo_6 = command.content.foo_6
				data_command.content.foo_7 = command.content.foo_7
				data_command.content.foo_8 = command.content.foo_8

			# ???
			elif command.type == 0x0036:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2
				data_command.content.foo_3 = command.content.foo_3

			# ???
			elif command.type == 0x0037:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2
				data_command.content.foo_3 = command.content.foo_3
				data_command.content.foo_4 = command.content.foo_4

			# ???
			elif command.type == 0x0038:
				data_command.content.foo = command.content.foo

			# if
			elif command.type == 0x0063:
				data_command.content.data_length_1 = command.content.data_length_1
				data_command.content.data_length_2 = command.content.data_length_2
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2
				data_command.content.branches = ObjDict()

				data_command.content.branches.branch_if = ObjDict()
				data_command.content.branches.branch_if.value_1 = command.content.branches.branch_if.value_1
				data_command.content.branches.branch_if.condition = command.content.branches.branch_if.condition
				data_command.content.branches.branch_if.value_2 = command.content.branches.branch_if.value_2
				if hasattr(command.content.branches.branch_if, "foo"):
					data_command.content.branches.branch_if.foo = command.content.branches.branch_if.foo
				data_command.content.branches.branch_if.commands = ObjDict()

				for self.command_inner_index, self.command_inner in enumerate(command.content.branches.branch_if.commands):
					data_command_inner = self._parse_command(self.command_inner)
					data_command.content.branches.branch_if.commands[str(self.command_inner_index)] = data_command_inner

				if hasattr(command.content.branches, "branch_else"):
					data_command.content.branches.branch_else = ObjDict()
					data_command.content.branches.branch_else.commands = ObjDict()

					for self.command_inner_index, self.command_inner in enumerate(command.content.branches.branch_else.commands):
						data_command_inner = self._parse_command(self.command_inner)
						data_command.content.branches.branch_else.commands[str(self.command_inner_index)] = data_command_inner
			# nokeys
			elif command.type == 0x4f4e:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2

			else:
				print "Unknown command type: %s" % (command.type)
				sys.exit()

		else:
			if command.type != 0x0010 and command.type != 0x002a and command.type != 0x003a and command.type != 0xffff:
				print "Command without content: %s (%s), screen %s, command %s" % (command.type, command_type_hex, self.screen_index, self.command_index)

		return data_command



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
				data_screen.content.data.commands = ObjDict()
				data_screen.content.data.events = ObjDict()

				for self.command_index, self.command in enumerate(self.screen.content.data.commands):
					data_command = self._parse_command(self.command)
					data_screen.content.data.commands[str(self.command_index)] = data_command

				for self.event_index, self.event in enumerate(self.screen.content.data.events):
					data_event = ObjDict()
					data_event.binding = self.event.binding

					if hasattr(self.event, "content"):
						data_event.content = ObjDict()
						data_event.content.data_length = self.event.content.data_length
						data_event.content.data = ObjDict()
						data_event.content.data.commands = ObjDict()

						for self.command_index, self.command in enumerate(self.event.content.data.commands):
							data_command = self._parse_command(self.command)
							data_event.content.data.commands[str(self.command_index)] = data_command

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
