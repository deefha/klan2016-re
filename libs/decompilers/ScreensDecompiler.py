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

		self.counts = ObjDict()



	def _parse_command(self, command):
		data_command = ObjDict()
		data_command.type = command.type

		if hasattr(command, "content"):
			data_command.content = ObjDict()

			command_type_hex = "{0:#0{1}x}".format(command.type, 6)
			if hasattr(self.counts, command_type_hex):
				self.counts[command_type_hex] += 1
			else:
				self.counts[command_type_hex] = 1

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

			# svar
			elif command.type == 0x000d:
				data_command.content.variable = command.content.variable
				data_command.content.value_length = command.content.value_length
				data_command.content.value = command.content.value

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
				if self.source.version > 2:
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
				if self.source.version < 3:
					data_command.content.foo = command.content.foo
				else:
					data_command.content.foo_1 = command.content.foo_1
					data_command.content.foo_2 = command.content.foo_2

			# image
			elif command.type == 0x0020:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2
				data_command.content.foo_3 = command.content.foo_3
				data_command.content.foo_4 = command.content.foo_4

			# curhelp
			elif command.type == 0x0023:
				data_command.content.foo_1 = command.content.foo_1
				data_command.content.foo_2 = command.content.foo_2
				data_command.content.foo_3 = command.content.foo_3
				data_command.content.foo_4 = command.content.foo_4
				data_command.content.text_length = command.content.text_length
				data_command.content.text = command.content.text
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
				data_command.content.branches.branch_if.commands = ObjDict()

				for command_inner_index, command_inner in enumerate(command.content.branches.branch_if.commands):
					data_command_inner = self._parse_command(command_inner)
					data_command.content.branches.branch_if.commands[str(command_inner_index)] = data_command_inner

				if hasattr(command.content.branches, "branch_else"):
					data_command.content.branches.branch_else = ObjDict()
					data_command.content.branches.branch_else.commands = ObjDict()

					for command_inner_index, command_inner in enumerate(command.content.branches.branch_else.commands):
						data_command_inner = self._parse_command(command_inner)
						data_command.content.branches.branch_else.commands[str(command_inner_index)] = data_command_inner

			else:
				print "Unknown command type: %s" % (command.type)
				sys.exit()

		return data_command


	def fill_meta_data(self):
		super(ScreensDecompiler, self).fill_meta_data()

		self.meta.data.screens = ObjDict()

		for screen_index, screen in enumerate(tqdm(self.library.data.screens, desc="data.screens", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
			data_screen = ObjDict()
			data_screen.param_offset = screen.param_offset
			data_screen.content = ObjDict()

			if screen.content:
				data_screen.content.type = screen.content.type
				data_screen.content.foo = screen.content.foo

				data_screen.content.data = ObjDict()
				data_screen.content.data.commands = ObjDict()
				data_screen.content.data.events = ObjDict()

				for command_index, command in enumerate(screen.content.data.commands):
					data_command = self._parse_command(command)
					data_screen.content.data.commands[str(command_index)] = data_command

				for event_index, event in enumerate(screen.content.data.events):
					data_event = ObjDict()
					data_event.binding = event.binding

					if hasattr(event, "content"):
						data_event.content = ObjDict()
						data_event.content.data_length = event.content.data_length
						data_event.content.data = ObjDict()
						data_event.content.data.commands = ObjDict()

						for command_index, command in enumerate(event.content.data.commands):
							data_command = self._parse_command(command)
							data_event.content.data.commands[str(command_index)] = data_command

					data_screen.content.data.events[str(event_index)] = data_event

			self.meta.data.screens[str(screen_index)] = data_screen

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
			self.meta.fat.offsets[str(offset_index)] = offset
