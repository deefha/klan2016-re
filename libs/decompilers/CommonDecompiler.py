# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
import json, re, string
from io import BytesIO
from pycdlib import PyCdlib

PATH_SELF = os.path.dirname(os.path.realpath(__file__))

# structs imports
sys.path.insert(0, "%s/%s" % (PATH_SELF, "../structs/")) # TODO not very nice...
from structs.klan_audio_v1 import KlanAudioV1
from structs.klan_audio_v2 import KlanAudioV2
from structs.klan_audio_v3 import KlanAudioV3
from structs.klan_cursors import KlanCursors
from structs.klan_descriptions import KlanDescriptions
from structs.klan_fonts import KlanFonts
from structs.klan_images import KlanImages
from structs.klan_music_v1 import KlanMusicV1
from structs.klan_music_v2 import KlanMusicV2
from structs.klan_screens_v1 import KlanScreensV1
from structs.klan_screens_v2 import KlanScreensV2
from structs.klan_screens_v3 import KlanScreensV3
from structs.klan_screens_v4 import KlanScreensV4
from structs.klan_texts_v1 import KlanTextsV1
from structs.klan_texts_v2 import KlanTextsV2
from structs.klan_texts_v3 import KlanTextsV3
from structs.klan_texts_v4 import KlanTextsV4
from structs.klan_texts_v5 import KlanTextsV5
from structs.klan_texts_v6 import KlanTextsV6
from structs.klan_texts_v7 import KlanTextsV7
from structs.klan_video import KlanVideo

PATH_DATA = "%s/%s" % (PATH_SELF, "../../data/")
PATH_ORIGINS = "%sinitialized/" % PATH_DATA
PATH_PHASE = "%sdecompiled/" % PATH_DATA

PATTERN_FILE_ORIGIN = "%s%%s.iso" % PATH_ORIGINS


class CommonDecompiler(object):

	def __init__(self, issue, source, source_index):
		self.issue = issue
		self.source = source
		self.source_index = source_index

		print("\tPath: %s" % self.source.path)
		print("\tLibrary: %s" % self.source.library)
		print("\tVersion: %s" % self.source.version)
		print("\tIndex: %s" % self.source_index)

		if not os.path.isfile(PATTERN_FILE_ORIGIN % self.issue.number):
			print("\tOrigin not exists, initialize first")
			sys.exit()

		self.PATH_DATA = "%s/%s/%s/%s/" % (PATH_PHASE, self.issue.number, self.source.library, self.source_index)

		self.FILE_META = "%s/%s/%s/%s.json" % (PATH_PHASE, self.issue.number, self.source.library, self.source_index)

		self.meta = ObjDict()

		if not os.path.exists(self.PATH_DATA):
			os.makedirs(self.PATH_DATA)

		self.iso = PyCdlib()
		self.iso_paths = []
		self.iso_content = BytesIO()

		self.iso.open(PATTERN_FILE_ORIGIN % self.issue.number)

		if '*' not in self.source.path:
			self.iso_paths.append("/%s;1" % self.source.path)
		else:
			path = os.path.dirname(self.source.path)
			mask = os.path.basename(self.source.path).replace('.', '\.')
			mask = mask.replace('*', '.*')
			regex = re.compile(mask)

			for child in self.iso.list_children(iso_path="/%s" % path):
				if regex.match(child.file_identifier().decode()):
					self.iso_paths.append("/%s/%s" % (path, child.file_identifier().decode()))


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
				data_macro.content.textfile = macro.content.textfile.decode('ascii')
				# macros >= 3
				if self.source.library == "screens" and self.source.version >= 3:
					data_macro.content.foo = macro.content.foo
				# macros >= 3
				if self.source.library == "texts" and self.source.version >= 6:
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
				# macros >= 3
				if self.source.library == "screens" and self.source.version >= 3:
					data_macro.content.foo_3 = macro.content.foo_3
				# macros >= 3
				if self.source.library == "texts" and self.source.version >= 6:
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
				# macros >= 3
				if self.source.library == "screens" and self.source.version >= 3:
					data_macro.content.foo = macro.content.foo
				# macros >= 3
				if self.source.library == "texts" and self.source.version >= 6:
					data_macro.content.foo = macro.content.foo

			# svar
			elif macro.type == 0x000d:
				data_macro.content.variable = macro.content.variable
				data_macro.content.value_length = macro.content.value_length
				if self.source.library == "screens" and self.source.version < 3:
					data_macro.content.value = macro.content.value.decode('ascii')
				else:
					data_macro.content.value = macro.content.value.decode('unicode-escape')

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
				# macros <= 2
				if self.source.library == "screens" and self.source.version <= 2:
					data_macro.content.foo_3 = macro.content.foo_3
				# macros <= 2
				if self.source.library == "texts" and self.source.version <= 4:
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
				# macros >= 2
				if self.source.library == "screens" and self.source.version >= 2:
					data_macro.content.foo_1 = macro.content.foo_1
					data_macro.content.foo_2 = macro.content.foo_2
				# macros >= 2
				elif self.source.library == "texts" and self.source.version >= 5:
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
				# macros >= 4
				if self.source.library == "screens" and self.source.version >= 4:
					data_macro.content.foo_5 = macro.content.foo_5
				# macros >= 4
				if self.source.library == "texts" and self.source.version >= 7:
					data_macro.content.foo_5 = macro.content.foo_5

			# ???
			elif macro.type == 0x0021:
				data_macro.content.foo_1 = macro.content.foo_1

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
				data_macro.content.text = macro.content.text.decode('unicode-escape')
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
				data_macro.content.textfile = macro.content.textfile.decode('ascii')

			# ???
			elif macro.type == 0x002d:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2

			# link?
			elif macro.type == 0x0033:
				data_macro.content.text_1_length = macro.content.text_1_length
				data_macro.content.text_1 = macro.content.text_1.decode('ascii')
				data_macro.content.text_2_length = macro.content.text_2_length
				data_macro.content.text_2 = macro.content.text_2.decode('ascii')
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

			# #07/texts/184/linktable error
			elif macro.type == 0x00f0:
				#data_macro.content.foo = macro.content.foo # TODO
				data_macro.content.foo = ""

			# #10/texts/202/linktable error
			elif macro.type == 0x414d:
				#data_macro.content.foo = macro.content.foo # TODO
				data_macro.content.foo = ""

			# nokeys
			elif macro.type == 0x4f4e:
				data_macro.content.foo_1 = macro.content.foo_1
				data_macro.content.foo_2 = macro.content.foo_2

			# #30/texts/94/linktable error
			elif macro.type == 0x614d:
				#data_macro.content.foo = macro.content.foo # TODO
				data_macro.content.foo = ""

			# #08/texts/211/linktable error
			elif macro.type == 0xc0ff:
				#data_macro.content.foo = macro.content.foo # TODO
				data_macro.content.foo = ""

			# #21/texts/145/0/linktable error
			elif macro.type == 0xc20c:
				#data_macro.content.foo = macro.content.foo # TODO
				data_macro.content.foo = ""

			# #21/texts/145/1/linktable error
			elif macro.type == 0xff02:
				#data_macro.content.foo = macro.content.foo # TODO
				data_macro.content.foo = ""

			else:
				if self.source.library == "screens":
					print("Unknown macro: %s (%s), screen %s, macro %s" % (macro.type, macro_type_hex, self.screen_index, self.macro_index))
				if self.source.library == "texts":
					print("Unknown macro: %s (%s), text %s, macro %s" % (macro.type, macro_type_hex, self.text_index, self.macro_index))
				sys.exit()

		else:
			if macro.type != 0x0010 and macro.type != 0x002a and macro.type != 0x003a and macro.type != 0xffff:
				if self.source.library == "screens":
					print("Macro without content: %s (%s), screen %s, macro %s" % (macro.type, macro_type_hex, self.screen_index, self.macro_index))
				if self.source.library == "texts":
					print("Macro without content: %s (%s), text %s, macro %s" % (macro.type, macro_type_hex, self.text_index, self.macro_index))
				sys.exit()

		return data_macro


	def decompile(self):
		for self.iso_path_index, self.iso_path in enumerate(self.iso_paths):
			print("\t\tISO path #%s/%s: %s" % (self.iso_path_index, len(self.iso_paths), self.iso_path))

			self.iso_content = BytesIO()
			self.iso.get_file_from_iso_fp(self.iso_content, iso_path=self.iso_path)
			self.iso_content.seek(0)

			if self.source.library == "audio":
				if self.source.version == 1:
					self.library = KlanAudioV1.from_io(self.iso_content)
				elif self.source.version == 2:
					self.library = KlanAudioV2.from_io(self.iso_content)
				elif self.source.version == 3:
					self.library = KlanAudioV3.from_io(self.iso_content)

			elif self.source.library == "cursors":
				self.library = KlanCursors.from_io(self.iso_content)

			elif self.source.library == "descriptions":
				self.library = KlanDescriptions.from_io(self.iso_content)

			elif self.source.library == "fonts":
				self.library = KlanFonts.from_io(self.iso_content)

			elif self.source.library == "images":
				self.library = KlanImages.from_io(self.iso_content)

			elif self.source.library == "music":
				if self.source.version == 1:
					self.library = KlanMusicV1.from_io(self.iso_content)
				elif self.source.version == 2:
					self.library = KlanMusicV2.from_io(self.iso_content)

			elif self.source.library == "screens":
				if self.source.version == 1:
					self.library = KlanScreensV1.from_io(self.iso_content)
				elif self.source.version == 2:
					self.library = KlanScreensV2.from_io(self.iso_content)
				elif self.source.version == 3:
					self.library = KlanScreensV3.from_io(self.iso_content)
				elif self.source.version == 4:
					self.library = KlanScreensV4.from_io(self.iso_content)

			elif self.source.library == "texts":
				if self.source.version == 1:
					self.library = KlanTextsV1.from_io(self.iso_content)
				elif self.source.version == 2:
					self.library = KlanTextsV2.from_io(self.iso_content)
				elif self.source.version == 3:
					self.library = KlanTextsV3.from_io(self.iso_content)
				elif self.source.version == 4:
					self.library = KlanTextsV4.from_io(self.iso_content)
				elif self.source.version == 5:
					self.library = KlanTextsV5.from_io(self.iso_content)
				elif self.source.version == 6:
					self.library = KlanTextsV6.from_io(self.iso_content)
				elif self.source.version == 7:
					self.library = KlanTextsV7.from_io(self.iso_content)

			elif self.source.library == "video":
				self.library = KlanVideo.from_io(self.iso_content)

			self.fill_meta_header()
			self.fill_meta_fat()
			self.fill_meta_data()

			self.iso_content.close()

		self.export_meta()


	def fill_meta_header(self):
		self.meta.header = ObjDict()
		self.meta.header.magic = self.library.header.magic.decode('ascii')
		self.meta.header.version = self.library.header.version # TODO hexa?
		self.meta.header.type = self.library.header.type
		self.meta.header.filesize = self.library.header.filesize
		self.meta.header.filetime = self.library.header.filetime # TODO ISO date
		self.meta.header.filedate = self.library.header.filedate # TODO ISO date
		self.meta.header.foo_1 = self.library.header.foo_1
		self.meta.header.foo_2 = self.library.header.foo_2
		self.meta.header.crc = self.library.header.crc # TODO check?!


	def fill_meta_fat(self):
		self.meta.fat = ObjDict()
		self.meta.fat.count = self.library.fat.count
		self.meta.fat.foo_1 = self.library.fat.foo_1
		self.meta.fat.foo_2 = self.library.fat.foo_2
		self.meta.fat.foo_3 = self.library.fat.foo_3
		self.meta.fat.offsets = ObjDict()

		for offset_index, offset in enumerate(tqdm(self.library.fat.offsets, desc="fat.offsets", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
			self.meta.fat.offsets[str(offset_index)] = offset


	def fill_meta_data(self):
		self.meta.data = ObjDict()


	def export_meta(self):
		with open(self.FILE_META, "w") as f:
			f.write(self.meta.dumps())
			#f.write(json.dumps(json.loads(self.meta.dumps()), indent=4))


	def __del__(self):
		self.iso.close()
