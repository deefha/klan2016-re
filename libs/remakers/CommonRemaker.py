# -*- coding: utf-8 -*-

# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
# NONE

ROOT_DATA = os.path.dirname(os.path.realpath(__file__)) + "/../../data/"



class CommonRemaker(object):

	def __init__(self, issue, source, source_index):
		self.initialized = False
		self.issue = issue
		self.source = source
		self.source_index = source_index

		self.items_total = 0
		self.items_hit = 0
		self.items_miss = 0

		self.PATH_PHASE_DECOMPILED = "%sdecompiled/" % ROOT_DATA
		self.PATH_PHASE_REMAKED = "%sremaked/" % ROOT_DATA

		self.PATH_DATA_DECOMPILED = "%s%s/%s/%s/" % (self.PATH_PHASE_DECOMPILED, self.issue.number, self.source.library, self.source_index)
		self.PATH_DATA_REMAKED = "%s%s/%s/%s/" % (self.PATH_PHASE_REMAKED, self.issue.number, self.source.library, self.source_index)

		self.FILE_META_DECOMPILED = "%s%s/%s/%s.json" % (self.PATH_PHASE_DECOMPILED, self.issue.number, self.source.library, self.source_index)
		self.FILE_META_REMAKED = "%s%s/%s/%s.json" % (self.PATH_PHASE_REMAKED, self.issue.number, self.source.library, self.source_index)

		if not os.path.exists(self.PATH_DATA_REMAKED):
			os.makedirs(self.PATH_DATA_REMAKED)

		print "Loading decompiled data..."

		try:
			with open(self.FILE_META_DECOMPILED, "r") as f:
				#content = f.read()
				lines = f.readlines() # TODO
				content = ''.join(lines) # TODO

				self.meta_decompiled = ObjDict(content)
				self.meta_remaked = ObjDict()
				
				self.initialized = True
		except IOError:
			print "Not decompiled"



	def _parse_macro(self, macro):
		data_macro = ObjDict()
		data_macro.type = ""
		data_macro.params = ObjDict()

		macro_type_hex = "{0:#0{1}x}".format(macro.type, 6)

		# doit
		if macro.type == 0x0001:
			data_macro.type = "doit"
			data_macro.params.id = macro.content.id

		# text
		elif macro.type == 0x0004:
			data_macro.type = "text"
			data_macro.params.content = macro.content.textfile
			data_macro.params.area = ObjDict()
			data_macro.params.area.topleft_x = macro.content.topleft_x
			data_macro.params.area.topleft_y = macro.content.topleft_y
			data_macro.params.area.width = macro.content.width
			data_macro.params.area.height = macro.content.height
			data_macro.params.slider = ObjDict()
			data_macro.params.slider.topleft_x = macro.content.slider_topleft_x
			data_macro.params.slider.topleft_y = macro.content.slider_topleft_y
			# macros >= 3
			if self.source.library == 'screens' and self.source.version >= 6:
				data_macro.params.foo = macro.content.foo

		# video
		elif macro.type == 0x0005:
			data_macro.type = "video"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2
			data_macro.params.foo_3 = macro.content.foo_3
			data_macro.params.foo_4 = macro.content.foo_4
			data_macro.params.foo_5 = macro.content.foo_5
			data_macro.params.foo_6 = macro.content.foo_6

		# obrazky
		elif macro.type == 0x0006:
			data_macro.type = "obrazky"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2
			data_macro.params.foo_3 = macro.content.foo_3
			data_macro.params.foo_4 = macro.content.foo_4
			data_macro.params.foo_5 = macro.content.foo_5

		# zvuk
		elif macro.type == 0x0007:
			data_macro.type = "zvuk"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2
			data_macro.params.foo_3 = macro.content.foo_3
			data_macro.params.foo_4 = macro.content.foo_4
			data_macro.params.foo_5 = macro.content.foo_5

		# button
		elif macro.type == 0x0009:
			data_macro.type = "button"
			data_macro.params.id = macro.content.id
			data_macro.params.image = macro.content.image
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.topleft_x = macro.content.topleft_x
			data_macro.params.topleft_y = macro.content.topleft_y
			data_macro.params.scancode = macro.content.scancode
			data_macro.params.hover_topleft_x = macro.content.hover_topleft_x
			data_macro.params.hover_topleft_y = macro.content.hover_topleft_y
			data_macro.params.hover_bottomright_x = macro.content.hover_bottomright_x
			data_macro.params.hover_bottomright_y = macro.content.hover_bottomright_y
			data_macro.params.foo_2 = macro.content.foo_2
			# macros >= 3
			if self.source.library == 'screens' and self.source.version >= 6:
				data_macro.params.foo_3 = macro.content.foo_3

		# area
		elif macro.type == 0x000a:
			data_macro.type = "area"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2
			data_macro.params.foo_3 = macro.content.foo_3
			data_macro.params.foo_4 = macro.content.foo_4
			data_macro.params.foo_5 = macro.content.foo_5
			data_macro.params.foo_6 = macro.content.foo_6

		# event
		elif macro.type == 0x000b:
			data_macro.type = "event"
			data_macro.params.id = macro.content.id

		# gotopage
		elif macro.type == 0x000c:
			data_macro.type = "gotopage"
			data_macro.params.id = macro.content.id
			# macros >= 3
			if self.source.library == 'screens' and self.source.version >= 6:
				data_macro.params.foo = macro.content.foo

		# svar
		elif macro.type == 0x000d:
			data_macro.type = "svar"
			data_macro.params.variable = macro.content.variable
			data_macro.params.value_length = macro.content.value_length
			data_macro.params.value = macro.content.value

		# ivar / mov
		elif macro.type == 0x000e:
			data_macro.type = "ivar/mov"
			data_macro.params.variable = macro.content.variable
			data_macro.params.value = macro.content.value

		# screen
		elif macro.type == 0x000f:
			data_macro.type = "screen"
			data_macro.params.id = macro.content.id

		# woknoshit
		elif macro.type == 0x0010:
			data_macro.type = "woknoshit"

		# keybutt
		elif macro.type == 0x0011:
			data_macro.type = "keybutt"
			data_macro.params.topleft_x = macro.content.topleft_x
			data_macro.params.topleft_y = macro.content.topleft_y
			data_macro.params.image = macro.content.image
			data_macro.params.foo = macro.content.foo
			data_macro.params.scancode = macro.content.scancode

		# getchar
		elif macro.type == 0x0012:
			data_macro.type = "getchar"
			data_macro.params.id = macro.content.id

		# pic
		elif macro.type == 0x0013:
			data_macro.type = "pic"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2
			# macros <= 2
			if self.source.library == 'screens' and self.source.version <= 4:
				data_macro.params.foo_3 = macro.content.foo_3

		# demo
		elif macro.type == 0x0014:
			data_macro.type = "demo"
			data_macro.params.textfile_length = macro.content.textfile_length
			data_macro.params.textfile = macro.content.textfile
			data_macro.params.foo = macro.content.foo

		# reklama
		elif macro.type == 0x0015:
			data_macro.type = "reklama"
			data_macro.params.topleft_x = macro.content.topleft_x
			data_macro.params.topleft_y = macro.content.topleft_y
			data_macro.params.bottomright_x = macro.content.bottomright_x
			data_macro.params.bottomright_y = macro.content.bottomright_y
			data_macro.params.image = macro.content.image
			data_macro.params.id = macro.content.id

		# keyevent
		elif macro.type == 0x0016:
			data_macro.type = "keyevent"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2
			data_macro.params.foo_3 = macro.content.foo_3

		# snap
		elif macro.type == 0x0017:
			data_macro.type = "snap"
			data_macro.params.foo = macro.content.foo

		# playwav
		elif macro.type == 0x0018:
			data_macro.type = "playwav"
			# macros >= 2
			if self.source.library == 'screens' and self.source.version >= 5:
				data_macro.params.foo_1 = macro.content.foo_1
				data_macro.params.foo_2 = macro.content.foo_2
			else:
				data_macro.params.foo = macro.content.foo

		# image
		elif macro.type == 0x0020:
			data_macro.type = "image"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2
			data_macro.params.foo_3 = macro.content.foo_3
			data_macro.params.foo_4 = macro.content.foo_4
			# macros >= 4
			if self.source.library == 'screens' and self.source.version >= 7:
				data_macro.params.foo_5 = macro.content.foo_5

		# ???
		elif macro.type == 0x0021:
			data_macro.type = "0x0021"
			data_macro.params.foo_1 = macro.content.foo_1

		# ???
		elif macro.type == 0x0022:
			data_macro.type = "0x0022"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2
			data_macro.params.foo_3 = macro.content.foo_3
			data_macro.params.foo_4 = macro.content.foo_4
			data_macro.params.foo_5 = macro.content.foo_5

		# curhelp
		elif macro.type == 0x0023:
			data_macro.type = "curhelp"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2
			data_macro.params.foo_3 = macro.content.foo_3
			data_macro.params.foo_4 = macro.content.foo_4
			data_macro.params.text_length = macro.content.text_length
			data_macro.params.text = macro.content.text
			data_macro.params.foo_5 = macro.content.foo_5

		# ???
		elif macro.type == 0x0024:
			data_macro.type = "0x0024"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2

		# ???
		elif macro.type == 0x0025:
			data_macro.type = "0x0025"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2

		# ???
		elif macro.type == 0x0026:
			data_macro.type = "0x0026"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2

		# ???
		elif macro.type == 0x0027:
			data_macro.type = "0x0027"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2

		# ???
		elif macro.type == 0x0028:
			data_macro.type = "0x0028"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2
			data_macro.params.foo_3 = macro.content.foo_3

		# ???
		elif macro.type == 0x0029:
			data_macro.type = "0x0029"
			data_macro.params.foo = macro.content.foo

		# ???
		elif macro.type == 0x002a:
			data_macro.type = "0x002a"

		# ???
		elif macro.type == 0x002b:
			data_macro.type = "0x002b"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2
			data_macro.params.foo_3 = macro.content.foo_3
			data_macro.params.foo_4 = macro.content.foo_4
			data_macro.params.foo_5 = macro.content.foo_5
			data_macro.params.foo_6 = macro.content.foo_6
			data_macro.params.foo_7 = macro.content.foo_7

		# ???
		elif macro.type == 0x002c:
			data_macro.type = "0x002c"
			data_macro.params.foo = macro.content.foo
			data_macro.params.textfile_length = macro.content.textfile_length
			data_macro.params.textfile = macro.content.textfile

		# ???
		elif macro.type == 0x002d:
			data_macro.type = "0x002d"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2

		# link?
		elif macro.type == 0x0033:
			data_macro.type = "link?"
			data_macro.params.text_1_length = macro.content.text_1_length
			data_macro.params.text_1 = macro.content.text_1
			data_macro.params.text_2_length = macro.content.text_2_length
			data_macro.params.text_2 = macro.content.text_2
			data_macro.params.foo = macro.content.foo

		# ???
		elif macro.type == 0x0035:
			data_macro.type = "0x0035"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2
			data_macro.params.foo_3 = macro.content.foo_3
			data_macro.params.foo_4 = macro.content.foo_4
			data_macro.params.foo_5 = macro.content.foo_5
			data_macro.params.foo_6 = macro.content.foo_6
			data_macro.params.foo_7 = macro.content.foo_7
			data_macro.params.foo_8 = macro.content.foo_8

		# ???
		elif macro.type == 0x0036:
			data_macro.type = "0x0036"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2
			data_macro.params.foo_3 = macro.content.foo_3

		# ???
		elif macro.type == 0x0037:
			data_macro.type = "0x0037"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2
			data_macro.params.foo_3 = macro.content.foo_3
			data_macro.params.foo_4 = macro.content.foo_4

		# ???
		elif macro.type == 0x0038:
			data_macro.type = "0x0038"
			data_macro.params.foo = macro.content.foo

		# ???
		elif macro.type == 0x003a:
			data_macro.type = "0x003a"

		# if
		elif macro.type == 0x0063:
			data_macro.type = "if"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2
			data_macro.params.branches = ObjDict()

			data_macro.params.branches.branch_if = ObjDict()
			data_macro.params.branches.branch_if.value_1 = macro.content.branches.branch_if.value_1
			data_macro.params.branches.branch_if.condition = macro.content.branches.branch_if.condition
			data_macro.params.branches.branch_if.value_2 = macro.content.branches.branch_if.value_2
			if hasattr(macro.content.branches.branch_if, "foo"):
				data_macro.params.branches.branch_if.foo = macro.content.branches.branch_if.foo
			data_macro.params.branches.branch_if.macros = ObjDict()

			for macro_inner_index, macro_inner in macro.content.branches.branch_if.macros.iteritems():
				data_macro_inner = self._parse_macro(macro_inner)
				data_macro.params.branches.branch_if.macros[str(macro_inner_index)] = data_macro_inner

			if hasattr(macro.content.branches, "branch_else"):
				data_macro.params.branches.branch_else = ObjDict()
				data_macro.params.branches.branch_else.macros = ObjDict()

				for macro_inner_index, macro_inner in macro.content.branches.branch_else.macros.iteritems():
					data_macro_inner = self._parse_macro(macro_inner)
					data_macro.params.branches.branch_else.macros[str(macro_inner_index)] = data_macro_inner

		# #07/texts/184/linktable error
		elif macro.type == 0x00f0:
			data_macro.type = "0x00f0"
			#data_macro.params.foo = macro.content.foo # TODO
			data_macro.params.foo = ""

		# #10/texts/202/linktable error
		elif macro.type == 0x414d:
			data_macro.type = "0x414d"
			#data_macro.params.foo = macro.content.foo # TODO
			data_macro.params.foo = ""

		# nokeys
		elif macro.type == 0x4f4e:
			data_macro.type = "nokeys"
			data_macro.params.foo_1 = macro.content.foo_1
			data_macro.params.foo_2 = macro.content.foo_2

		# #30/texts/94/linktable error
		elif macro.type == 0x614d:
			data_macro.type = "0x614d"
			#data_macro.params.foo = macro.content.foo # TODO
			data_macro.params.foo = ""

		# #08/texts/211/linktable error
		elif macro.type == 0xc0ff:
			data_macro.type = "0xc0ff"
			#data_macro.params.foo = macro.content.foo # TODO
			data_macro.params.foo = ""

		# #21/texts/145/0/linktable error
		elif macro.type == 0xc20c:
			data_macro.type = "0xc20c"
			#data_macro.params.foo = macro.content.foo # TODO
			data_macro.params.foo = ""

		# #21/texts/145/1/linktable error
		elif macro.type == 0xff02:
			data_macro.type = "0xff02"
			#data_macro.params.foo = macro.content.foo # TODO
			data_macro.params.foo = ""

		# separator
		elif macro.type == 0xffff:
			data_macro.type = "separator"

		else:
			if self.source.library == 'screens':
				print "Unknown macro: %s (%s), screen %s, macro %s" % (macro.type, macro_type_hex, self.screen_index, self.macro_index)
			if self.source.library == 'texts':
				print "Unknown macro: %s (%s), text %s, macro %s" % (macro.type, macro_type_hex, self.text_index, self.macro_index)
			sys.exit()

		return data_macro



	def fill_meta(self):
		self.meta_remaked.header = ObjDict()
		self.meta_remaked.header.issue = self.issue.number
		self.meta_remaked.header.path = self.source.path
		self.meta_remaked.header.library = self.source.library
		self.meta_remaked.header.version = self.source.version
		self.meta_remaked.header.index = self.source_index

		if hasattr(self.meta_decompiled.header, "filedate") and hasattr(self.meta_decompiled.header, "filetime"):
			year = ((self.meta_decompiled.header.filedate & 0b1111111000000000) >> 9) + 1980
			month = (self.meta_decompiled.header.filedate & 0b0000000111100000) >> 5
			day = self.meta_decompiled.header.filedate & 0b0000000000011111
			hour = (self.meta_decompiled.header.filetime & 0b1111100000000000) >> 11
			minute = (self.meta_decompiled.header.filetime & 0b0000011111100000) >> 5
			sec = (self.meta_decompiled.header.filetime & 0b0000000000011111) * 2

			try:
				self.meta_remaked.header.created = datetime.datetime(year, month, day, hour, minute, sec).isoformat()
			except ValueError:
				self.meta_remaked.header.created = ""
		else:
			self.meta_remaked.header.created = ""

		self.meta_remaked.header.remaked = datetime.datetime.now().isoformat()



	def export_meta(self):
		with open(self.FILE_META_REMAKED, "w") as f:
			f.write(self.meta_remaked.dumps())



	def print_stats(self):
		print "Total: %s" % self.items_total
		print "Hit: %s" % self.items_hit
		print "Miss: %s" % self.items_miss
