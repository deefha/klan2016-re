# common imports
import os, sys, datetime
from io import BytesIO
from objdict import ObjDict
from pycdlib import PyCdlib
from pprint import pprint
from tqdm import tqdm

# specific imports
from structs.klan_audio_v1 import KlanAudioV1
from structs.klan_audio_v2 import KlanAudioV2
from structs.klan_audio_v3 import KlanAudioV3
from structs.klan_cursors import KlanCursors
from structs.klan_fonts import KlanFonts
from structs.klan_images import KlanImages
from structs.klan_music_v1 import KlanMusicV1
from structs.klan_music_v2 import KlanMusicV2

ROOT_DATA = os.path.dirname(os.path.realpath(__file__)) + "/../../data/"

PATH_PHASE = "%s/decompiled/" % ROOT_DATA
PATH_ORIGINS = "%s/initialized/" % ROOT_DATA

PATTERN_FILE_ORIGIN = "%s%%s.iso" % PATH_ORIGINS



class CommonDecompiler(object):

	def __init__(self, issue, source, source_index):
		self.issue = issue
		self.source = source
		self.source_index = source_index

		self.PATH_DATA = "%s/%s/%s/%s/" % (PATH_PHASE, self.issue.number, self.source.library, self.source_index)

		self.FILE_META = "%s/%s/%s/%s.json" % (PATH_PHASE, self.issue.number, self.source.library, self.source_index)

		self.meta = ObjDict()

		if not os.path.exists(self.PATH_DATA):
			os.makedirs(self.PATH_DATA)

		iso = PyCdlib()
		self.iso_content = BytesIO()

		iso.open(PATTERN_FILE_ORIGIN % self.issue.number)

		iso.get_file_from_iso_fp(self.iso_content, iso_path="/%s;1" % self.source.path)
		iso.close()

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

		#print "Count: %d" % self.library.fat.count

		for offset_index, offset in enumerate(tqdm(self.library.fat.offsets, desc="fat.offsets", ascii=True, leave=True)):
			#print "Offset #%d: %d" % (offset_index, offset)

			self.meta.fat.offsets[str(offset_index)] = offset



	def fill_meta_data(self):
		self.meta.data = ObjDict()



	def export_meta(self):
		with open(self.FILE_META, "w") as f:
			f.write(self.meta.dumps())
