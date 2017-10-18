import os, sys

from objdict import ObjDict
from structs.klan_font import KlanFont

PATH_DATA = os.path.dirname(os.path.realpath(__file__)) + "/../../data/"



class CommonDecompilator(object):

	def __init__(self, issue, source):
		self.issue = issue
		self.source = source

		self.PATH_BLOBS = "%sblobs/%s/%s/" % (PATH_DATA, self.issue, self.source)
		self.PATH_META = "%smeta/%s/%s/" % (PATH_DATA, self.issue, self.source)

		self.FILE_SOURCE = "%ssources/%s/%s.lib" % (PATH_DATA, self.issue, self.source) # TODO test if exists
		self.FILE_META = "%smeta/%s/%s.json" % (PATH_DATA, self.issue, self.source)

		self.meta = ObjDict()

		if not os.path.exists(self.PATH_BLOBS):
			os.makedirs(self.PATH_BLOBS)

		if not os.path.exists(self.PATH_META):
			os.makedirs(self.PATH_META)

		if self.source == "font":
			self.library = KlanFont.from_file(self.FILE_SOURCE)



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
