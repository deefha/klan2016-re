# common imports
import os, sys, datetime
from objdict import ObjDict
from pprint import pprint

# specific imports

ROOT_DATA = os.path.dirname(os.path.realpath(__file__)) + "/../../data/"



class CommonRemaker(object):

	def __init__(self, issue, source, source_index):
		self.issue = issue
		self.source = source
		self.source_index = source_index

		self.PATH_PHASE_DECOMPILED = "%s/decompiled/" % ROOT_DATA
		self.PATH_PHASE_REMAKED = "%s/remaked/" % ROOT_DATA

		self.PATH_DATA_DECOMPILED = "%s/%s/%s/%s/" % (self.PATH_PHASE_DECOMPILED, self.issue.number, self.source.library, self.source_index)
		self.PATH_DATA_REMAKED = "%s/%s/%s/%s/" % (self.PATH_PHASE_REMAKED, self.issue.number, self.source.library, self.source_index)

		self.FILE_META_DECOMPILED = "%s/%s/%s/%s.json" % (self.PATH_PHASE_DECOMPILED, self.issue.number, self.source.library, self.source_index)
		self.FILE_META_REMAKED = "%s/%s/%s/%s.json" % (self.PATH_PHASE_REMAKED, self.issue.number, self.source.library, self.source_index)

		if not os.path.exists(self.PATH_DATA_REMAKED):
			os.makedirs(self.PATH_DATA_REMAKED)

		with open(self.FILE_META_DECOMPILED, "r") as f:
			#content = f.read()
			lines = f.readlines() # TODO
			content = ''.join(lines) # TODO

		self.meta_decompiled = ObjDict(content)
		self.meta_remaked = ObjDict()



	def fill_meta(self):
		self.meta_remaked.header = ObjDict()
		self.meta_remaked.header.issue = self.issue.number
		self.meta_remaked.header.library = self.source.library

		if self.meta_decompiled.header.filedate and self.meta_decompiled.header.filetime:
			year = ((self.meta_decompiled.header.filedate & 0b1111111000000000) >> 9) + 1980
			month = (self.meta_decompiled.header.filedate & 0b0000000111100000) >> 5
			day = self.meta_decompiled.header.filedate & 0b0000000000011111
			hour = (self.meta_decompiled.header.filetime & 0b1111100000000000) >> 11
			minute = (self.meta_decompiled.header.filetime & 0b0000011111100000) >> 5
			sec = (self.meta_decompiled.header.filetime & 0b0000000000011111) * 2

			self.meta_remaked.header.created = datetime.datetime(year, month, day, hour, minute, sec).isoformat()
			self.meta_remaked.header.remaked = datetime.datetime.now().isoformat()
		else:
			self.meta_remaked.header.created = ""
			self.meta_remaked.header.remaked = ""



	def export_meta(self):
		with open(self.FILE_META_REMAKED, "w") as f:
			f.write(self.meta_remaked.dumps())
