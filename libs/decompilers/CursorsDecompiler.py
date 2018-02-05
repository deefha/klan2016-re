# common imports
import os, sys, datetime
from objdict import ObjDict

# specific imports
from CommonDecompiler import CommonDecompiler



class CursorsDecompiler(CommonDecompiler):

	PATTERN_PATH_FRAMES = "%sframes/%02d/"
	PATTERN_PATH_FOO_1 = "%sfoo_1/"
	PATTERN_PATH_FOO_2 = "%sfoo_2/%02d/"
	PATTERN_PATH_COLORTABLES = "%scolortables/%02d/"

	PATTERN_FILE_FRAME = "%sframes/%02d/content.bin"
	PATTERN_FILE_FOO_1 = "%sfoo_1/content.bin"
	PATTERN_FILE_FOO_2 = "%sfoo_2/%02d/content.bin"
	PATTERN_FILE_COLORTABLE = "%scolortables/%02d/content.bin"

	PATTERN_DECOMPILED_FRAME = "decompiled://%s/%s/%s/frames/%02d/content.bin"
	PATTERN_DECOMPILED_FOO_1 = "decompiled://%s/%s/%s/foo_1/content.bin"
	PATTERN_DECOMPILED_FOO_2 = "decompiled://%s/%s/%s/foo_2/%02d/content.bin"
	PATTERN_DECOMPILED_COLORTABLE = "decompiled://%s/%s/%s/colortables/%02d/content.bin"

	def fill_meta_fat(self):
		self.meta.fat = ObjDict()
		self.meta.fat.frames_offset = self.library.fat.frames_offset
		self.meta.fat.frames_count = self.library.fat.frames_count
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

		self.meta.data.frames = ObjDict()
		self.meta.data.foo_1 = ObjDict()
		self.meta.data.foo_2 = ObjDict()
		self.meta.data.colortables = ObjDict()

		for frame_index, frame in enumerate(self.library.data.frames):
			data_frame = ObjDict()
			data_frame.param_offset = frame.param_offset
			data_frame.param_index = frame.param_index
			data_frame.content = ObjDict()

			print "Frame #%d: param_offset=%d, param_index=%d, x=%d, y=%d, id=%d" % (frame_index, frame.param_offset, frame.param_index, frame.content.x, frame.content.y, frame.content.id)

			file_frame = self.PATTERN_FILE_FRAME % (self.PATH_DATA, frame_index)

			path_frames = self.PATTERN_PATH_FRAMES % (self.PATH_DATA, frame_index)

			if not os.path.exists(path_frames):
				os.makedirs(path_frames)

			data_frame.content.x = frame.content.x
			data_frame.content.y = frame.content.y
			data_frame.content.id = frame.content.id
			data_frame.content.data = self.PATTERN_DECOMPILED_FRAME % (self.issue.number, self.source.library, self.source_index, frame_index)

			print "\tData"
			f = open(file_frame, "wb")
			f.write(frame.content.data)
			f.close

			self.meta.data.frames[str(frame_index)] = data_frame

		self.meta.data.foo_1.param_offset = self.library.data.foo_1.param_offset
		self.meta.data.foo_1.content = ObjDict()

		print "foo_1: param_offset=%d" % self.meta.data.foo_1.param_offset

		file_foo_1 = self.PATTERN_FILE_FOO_1 % self.PATH_DATA

		path_foo_1 = self.PATTERN_PATH_FOO_1 % self.PATH_DATA

		if not os.path.exists(path_foo_1):
			os.makedirs(path_foo_1)

		self.meta.data.foo_1.content.data = self.PATTERN_DECOMPILED_FOO_1 % (self.issue.number, self.source.library, self.source_index)

		print "\tData"
		f = open(file_foo_1, "wb")
		f.write(self.library.data.foo_1.content.data)
		f.close

		for foo_2_index, foo_2 in enumerate(self.library.data.foo_2):
			data_foo_2 = ObjDict()
			data_foo_2.param_offset = foo_2.param_offset
			data_foo_2.content = ObjDict()

			print "foo_2 #%d: param_offset=%d" % (foo_2_index, foo_2.param_offset)

			file_foo_2 = self.PATTERN_FILE_FOO_2 % (self.PATH_DATA, foo_2_index)

			path_foo_2 = self.PATTERN_PATH_FOO_2 % (self.PATH_DATA, foo_2_index)

			if not os.path.exists(path_foo_2):
				os.makedirs(path_foo_2)

			data_foo_2.content.data = self.PATTERN_DECOMPILED_FOO_2 % (self.issue.number, self.source.library, self.source_index, foo_2_index)

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

			file_colortable = self.PATTERN_FILE_COLORTABLE % (self.PATH_DATA, colortable_index)

			path_colortables = self.PATTERN_PATH_COLORTABLES % (self.PATH_DATA, colortable_index)

			if not os.path.exists(path_colortables):
				os.makedirs(path_colortables)

			data_colortable.content.data = self.PATTERN_DECOMPILED_COLORTABLE % (self.issue.number, self.source.library, self.source_index, colortable_index)

			print "\tData"
			f = open(file_colortable, "wb")
			f.write(colortable.content.data)
			f.close

			self.meta.data.colortables[str(colortable_index)] = data_colortable
