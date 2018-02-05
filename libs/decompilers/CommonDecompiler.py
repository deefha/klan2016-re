# common imports
import os, sys, datetime
from io import BytesIO
from objdict import ObjDict
from pycdlib import PyCdlib
from pprint import pprint

# specific imports
from structs.klan_cursors import KlanCursors
from structs.klan_fonts import KlanFonts
from structs.klan_images import KlanImages
from structs.klan_wave_v1 import KlanWaveV1
from structs.klan_wave_v2 import KlanWaveV2
from structs.klan_wave_v3 import KlanWaveV3
from structs.klan_music_v1 import KlanMusicV1
from structs.klan_music_v2 import KlanMusicV2

PATH_DATA = os.path.dirname(os.path.realpath(__file__)) + "/../../data/"



class CommonDecompiler(object):

	def __init__(self, issue, source, source_index):
		self.issue = issue
		self.source = source
		self.source_index = source_index

		self.PATH_BLOBS = "%sblobs/%s/%s/%s/" % (PATH_DATA, self.issue.number, self.source.library, self.source_index)
		self.PATH_META = "%smeta/%s/%s/%s/" % (PATH_DATA, self.issue.number, self.source.library, self.source_index)

		self.FILE_META = "%smeta/%s/%s/%s.json" % (PATH_DATA, self.issue.number, self.source.library, self.source_index)

		self.meta = ObjDict()

		if not os.path.exists(self.PATH_BLOBS):
			os.makedirs(self.PATH_BLOBS)

		if not os.path.exists(self.PATH_META):
			os.makedirs(self.PATH_META)

		iso = PyCdlib()
		self.iso_content = BytesIO()

		iso.open("%sorigins/%s.iso" % (PATH_DATA, self.issue.number))

		#for child in iso.list_dir(iso_path='/'):
			#print(child.file_identifier())

		iso.get_file_from_iso_fp(self.iso_content, iso_path="/%s;1" % self.source.path)
		iso.close()

		self.iso_content.seek(0)

		if self.source.library == "cursors":
			self.library = KlanCursors.from_io(self.iso_content)

		elif self.source.library == "fonts":
			self.library = KlanFonts.from_io(self.iso_content)

		elif self.source.library == "images":
			self.library = KlanImages.from_io(self.iso_content)

		elif self.source.library == "audios":
			if self.source.version == 1:
				self.library = KlanWaveV1.from_io(self.iso_content)
			elif self.source.version == 2:
				self.library = KlanWaveV2.from_io(self.iso_content)
			elif self.source.version == 3:
				self.library = KlanWaveV3.from_io(self.iso_content)

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

		print "Count: %d" % self.library.fat.count

		for offset_index, offset in enumerate(self.library.fat.offsets):
			print "Offset #%d: %d" % (offset_index, offset)

			self.meta.fat.offsets[str(offset_index)] = offset



	def fill_meta_data(self):
		self.meta.data = ObjDict()



	def export_meta(self):
		f = open(self.FILE_META, "w")
		f.write(self.meta.dumps())
		f.close
