import os, sys, pprint, datetime

from objdict import ObjDict

PATH_DATA = os.path.dirname(os.path.realpath(__file__)) + "/../../data/"



class CommonRemaker(object):

	def __init__(self, issue, source):
		self.issue = issue
		self.source = source

		self.ROOT_BLOBS = "%sblobs/" % PATH_DATA

		self.PATH_BLOBS = "%sblobs/%s/%s/" % (PATH_DATA, self.issue, self.source)
		self.PATH_META = "%smeta/%s/%s/" % (PATH_DATA, self.issue, self.source)
		self.PATH_ASSETS = "%sassets/%s/%s/" % (PATH_DATA, self.issue, self.source)
		self.PATH_SCHEMES = "%sschemes/%s/%s/" % (PATH_DATA, self.issue, self.source)

		self.FILE_META = "%smeta/%s/%s.json" % (PATH_DATA, self.issue, self.source)
		self.FILE_SCHEME = "%sschemes/%s/%s.json" % (PATH_DATA, self.issue, self.source)

		if not os.path.exists(self.PATH_ASSETS):
			os.makedirs(self.PATH_ASSETS)

		if not os.path.exists(self.PATH_SCHEMES):
			os.makedirs(self.PATH_SCHEMES)

		with open(self.FILE_META, "r") as f:
			#content = f.read()
			lines = f.readlines() # TODO
			content = ''.join(lines) # TODO

		self.meta = ObjDict(content)
		self.scheme = ObjDict()



	def fill_scheme(self):
		self.scheme.header = ObjDict()
		self.scheme.header.issue = self.issue
		self.scheme.header.source = self.source

		year = ((self.meta.header.filedate & 0b1111111000000000) >> 9) + 1980
		month = (self.meta.header.filedate & 0b0000000111100000) >> 5
		day = self.meta.header.filedate & 0b0000000000011111
		hour = (self.meta.header.filetime & 0b1111100000000000) >> 11
		minute = (self.meta.header.filetime & 0b0000011111100000) >> 5
		sec = (self.meta.header.filetime & 0b0000000000011111) * 2

		self.scheme.header.created = datetime.datetime(year, month, day, hour, minute, sec).isoformat()
		self.scheme.header.remaked = datetime.datetime.now().isoformat()



	def export_scheme(self):
		f = open(self.FILE_SCHEME, "w")
		f.write(self.scheme.dumps())
		f.close
