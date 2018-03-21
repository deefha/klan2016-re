# -*- coding: utf-8 -*-

# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
import json, re, string
from io import BytesIO
from pycdlib import PyCdlib
from structs.klan_audio_v1 import KlanAudioV1
from structs.klan_audio_v2 import KlanAudioV2
from structs.klan_audio_v3 import KlanAudioV3
from structs.klan_cursors import KlanCursors
from structs.klan_fonts import KlanFonts
from structs.klan_images import KlanImages
from structs.klan_music_v1 import KlanMusicV1
from structs.klan_music_v2 import KlanMusicV2
from structs.klan_texts_v1 import KlanTextsV1
from structs.klan_texts_v2 import KlanTextsV2
from structs.klan_texts_v3 import KlanTextsV3
from structs.klan_texts_v4 import KlanTextsV4

ROOT_DATA = os.path.dirname(os.path.realpath(__file__)) + "/../../data/"

PATH_PHASE = "%s/decompiled/" % ROOT_DATA
PATH_ORIGINS = "%s/initialized/" % ROOT_DATA

PATTERN_FILE_ORIGIN = "%s%%s.iso" % PATH_ORIGINS



class CommonDecompiler(object):

	def __init__(self, issue, source, source_index):
		self.issue = issue
		self.source = source
		self.source_index = source_index

		print "\tPath: %s" % self.source.path
		print "\tLibrary: %s" % self.source.library
		print "\tVersion: %s" % self.source.version
		print "\tIndex: %s" % self.source_index

		if not os.path.isfile(PATTERN_FILE_ORIGIN % self.issue.number):
			print "\tOrigin not exists, initialize first"
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
			mask = string.replace(os.path.basename(self.source.path), '.', '\.')
			mask = string.replace(mask, '*', '.*')
			regex = re.compile(mask)

			for child in self.iso.list_children(iso_path="/%s" % path):
				if re.match(regex, child.file_identifier()):
					self.iso_paths.append("/%s/%s" % (path, child.file_identifier()))



	def decompile(self):
		for self.iso_path_index, self.iso_path in enumerate(self.iso_paths):
			print "\t\tISO path #%s/%s: %s" % (self.iso_path_index, len(self.iso_paths), self.iso_path)

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

			elif self.source.library == "fonts":
				self.library = KlanFonts.from_io(self.iso_content)

			elif self.source.library == "images":
				self.library = KlanImages.from_io(self.iso_content)

			elif self.source.library == "music":
				if self.source.version == 1:
					self.library = KlanMusicV1.from_io(self.iso_content)
				elif self.source.version == 2:
					self.library = KlanMusicV2.from_io(self.iso_content)

			elif self.source.library == "texts":
				if self.source.version == 1:
					self.library = KlanTextsV1.from_io(self.iso_content)
				elif self.source.version == 2:
					self.library = KlanTextsV2.from_io(self.iso_content)
				elif self.source.version == 3:
					self.library = KlanTextsV3.from_io(self.iso_content)
				elif self.source.version == 4:
					self.library = KlanTextsV4.from_io(self.iso_content)

			self.fill_meta_header()
			self.fill_meta_fat()
			self.fill_meta_data()

			self.iso_content.close()

		self.export_meta()



	def fill_meta_header(self):
		self.meta.header = ObjDict()
		self.meta.header.magic = self.library.header.magic
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
