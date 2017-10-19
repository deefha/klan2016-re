import os, sys

from objdict import ObjDict

PATH_DATA = os.path.dirname(os.path.realpath(__file__)) + "/../../data/"



class CommonRemaker(object):

	def __init__(self, issue, source):
		self.issue = issue
		self.source = source

		self.PATH_BLOBS = "%sblobs/%s/%s/" % (PATH_DATA, self.issue, self.source)
		self.PATH_META = "%smeta/%s/%s/" % (PATH_DATA, self.issue, self.source)
		self.PATH_OBJECTS = "%sobjects/%s/%s/" % (PATH_DATA, self.issue, self.source)

		self.FILE_META = "%smeta/%s/%s.json" % (PATH_DATA, self.issue, self.source)
		self.FILE_OBJECT = "%sobjects/%s/%s.json" % (PATH_DATA, self.issue, self.source)

		if not os.path.exists(self.PATH_OBJECTS):
			os.makedirs(self.PATH_OBJECTS)

		with open(self.FILE_META, "r") as f:
			content = f.read()
			self.meta = ObjDict(content)
