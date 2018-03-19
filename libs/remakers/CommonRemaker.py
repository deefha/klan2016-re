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



	def fill_meta(self):
		self.meta_remaked.header = ObjDict()
		self.meta_remaked.header.issue = self.issue.number
		self.meta_remaked.header.library = self.source.library

		if hasattr(self.meta_decompiled.header, "filedate") and hasattr(self.meta_decompiled.header, "filetime"):
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



	def print_stats(self):
		print "Total: %s" % self.items_total
		print "Hit: %s" % self.items_hit
		print "Miss: %s" % self.items_miss
