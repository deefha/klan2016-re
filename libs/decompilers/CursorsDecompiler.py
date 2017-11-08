import os, sys

from objdict import ObjDict
from CommonDecompiler import CommonDecompiler



class CursorsDecompiler(CommonDecompiler):

	PATTERN_PATH_CURSORS = "%scursors/%02d/"
	PATTERN_PATH_FOO_2 = "%sfoo_2/%02d/"
	PATTERN_PATH_COLORTABLES = "%scolortables/%02d/"
	PATTERN_FILE_CURSOR = "%scursors/%02d/data.bin"
	PATTERN_FILE_FOO_2 = "%sfoo_2/%02d/data.bin"
	PATTERN_FILE_COLORTABLE = "%scolortables/%02d/data.bin"

	def fill_meta_fat(self):
		self.meta.fat = ObjDict()
		self.meta.fat.cursors_offset = self.library.fat.cursors_offset
		self.meta.fat.cursors_count = self.library.fat.cursors_count
		self.meta.fat.foo_1_offset = self.library.fat.foo_1_offset
		self.meta.fat.foo_2_count = self.library.fat.foo_2_count
		self.meta.fat.colortables_ofset = self.library.fat.colortables_ofset
		self.meta.fat.foo = self.library.fat.foo
		self.meta.fat.foo_2 = ObjDict()

		for foo_2_index, foo_2 in enumerate(self.library.fat.foo_2):
			print "foo_2 #%d: offset=%d, foo=%d" % (foo_2_index, foo_2.offset, foo_2.foo)

			data_foo_2 = ObjDict()
			data_foo_2.offset = foo_2.offset
			data_foo_2.foo = foo_2.foo

			self.meta.fat.foo_2[str(foo_2_index)] = data_foo_2



	def fill_meta_data(self):
		super(CursorsDecompiler, self).fill_meta_data()

		self.meta.data.cursors = ObjDict()
		self.meta.data.foo_1 = ObjDict()
		self.meta.data.foo_2 = ObjDict()
		self.meta.data.colortables = ObjDict()

		for cursor_index, cursor in enumerate(self.library.data.cursors):
			data_cursor = ObjDict()
			data_cursor.param_offset = cursor.param_offset
			data_cursor.param_index = cursor.param_index
			data_cursor.content = ObjDict()

			print "Cursor #%d: param_offset=%d, param_index=%d, x=%d, y=%d, id=%d" % (cursor_index, cursor.param_offset, cursor.param_index, cursor.content.x, cursor.content.y, cursor.content.id)

			file_cursor = self.PATTERN_FILE_CURSOR % (self.PATH_BLOBS, cursor_index)

			path_cursors = self.PATTERN_PATH_CURSORS % (self.PATH_BLOBS, cursor_index)

			if not os.path.exists(path_cursors):
				os.makedirs(path_cursors)

			data_cursor.content.x = cursor.content.x
			data_cursor.content.y = cursor.content.y
			data_cursor.content.id = cursor.content.id
			data_cursor.content.data = "blobs://%s/%s/cursors/%02d/data.bin" % (self.issue, self.source, cursor_index)

			print "\tData"
			f = open(file_cursor, "wb")
			f.write(cursor.content.data)
			f.close

			self.meta.data.cursors[str(cursor_index)] = data_cursor

		self.meta.data.foo_1.param_offset = self.library.data.foo_1.param_offset
		self.meta.data.foo_1.content = ObjDict()
		self.meta.data.foo_1.content.data =  "blobs://%s/%s/foo_1/data.bin" % (self.issue, self.source)

		for foo_2_index, foo_2 in enumerate(self.library.data.foo_2):
			data_foo_2 = ObjDict()
			data_foo_2.param_offset = foo_2.param_offset
			data_foo_2.content = ObjDict()

			print "foo_2 #%d: param_offset=%d" % (foo_2_index, foo_2.param_offset)

			file_foo_2 = self.PATTERN_FILE_FOO_2 % (self.PATH_BLOBS, foo_2_index)

			path_foo_2 = self.PATTERN_PATH_FOO_2 % (self.PATH_BLOBS, foo_2_index)

			if not os.path.exists(path_foo_2):
				os.makedirs(path_foo_2)

			data_foo_2.content.data = "blobs://%s/%s/foo_2/%02d/data.bin" % (self.issue, self.source, foo_2_index)

			print "\tData"
			f = open(file_foo_2, "wb")
			f.write(foo_2.content.data)
			f.close

			self.meta.data.foo_2[str(foo_2_index)] = data_foo_2

		for colortable_index, colortable in enumerate(self.library.data.colortables):
			data_colortable = ObjDict()
			data_colortable.param_offset = colortable.param_offset
			data_colortable.param_index = colortable.param_index
			data_colortable.content = ObjDict()

			print "Colortable #%d: param_offset=%d, param_index=%d" % (colortable_index, colortable.param_offset, colortable.param_index)

			file_colortable = self.PATTERN_FILE_COLORTABLE % (self.PATH_BLOBS, colortable_index)

			path_colortables = self.PATTERN_PATH_COLORTABLES % (self.PATH_BLOBS, colortable_index)

			if not os.path.exists(path_colortables):
				os.makedirs(path_colortables)

			data_colortable.content.data = "blobs://%s/%s/colortables/%02d/data.bin" % (self.issue, self.source, colortable_index)

			print "\tData"
			f = open(file_colortable, "wb")
			f.write(colortable.content.data)
			f.close

			self.meta.data.colortables[str(colortable_index)] = data_colortable
