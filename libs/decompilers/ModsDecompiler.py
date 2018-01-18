import os, sys

from objdict import ObjDict
from CommonDecompiler import CommonDecompiler



class ModsDecompiler(CommonDecompiler):

	PATTERN_PATH_WAVE = "%s%04d/"
	PATTERN_FILE_CONTENT = "%s%04d/content.bin"

	def fill_meta_data(self):
		super(ModsDecompiler, self).fill_meta_data()

		self.meta.data.names = ObjDict()

		for names_index, name in enumerate(self.library.data.names):
			#self.meta.data.names[str(names_index)] = name
			self.meta.data.names[str(names_index)] = ""

		self.meta.data.mods = ObjDict()

		#for mods_index, mod in enumerate(self.library.data.mods):
			#data_mod = ObjDict()
			#data_mod.param_offset = mod.param_offset
			#data_mod.content = ObjDict()

			#if mod.content:
				#print "Wave #%d: param_offset=%d, data_size=%d, mod_size=%d, mode=%d" % (mods_index, mod.param_offset, mod.content.data_size, mod.content.mod_size, mod.content.mode)

				#file_content = self.PATTERN_FILE_CONTENT % (self.PATH_BLOBS, mods_index)

				#path_mod = self.PATTERN_PATH_WAVE % (self.PATH_BLOBS, mods_index)

				#if not os.path.exists(path_mod):
					#os.makedirs(path_mod)

				#data_mod.content.data_size = mod.content.data_size
				#data_mod.content.mod_size = mod.content.mod_size
				#data_mod.content.mode = mod.content.mode
				#data_mod.content.foo_1 = mod.content.foo_1
				#data_mod.content.foo_2 = mod.content.foo_2
				#data_mod.content.data = ObjDict()
				#data_mod.content.data.param_data_size = mod.content.data.param_data_size

				#if self.issue > "00":
					#data_mod.content.data.title = ""
					##data_mod.content.data.title = mod.content.data.title
				#else:
					#data_mod.content.data.title = ""

				#data_mod.content.data.content = "blobs://%s/%s/%04d/content.bin" % (self.issue, self.source, mods_index)

				#print "\tContent"
				#f = open(file_content, "wb")
				#f.write(mod.content.data.content)
				#f.close

			#else:
				#print "Wave #%d: param_offset=%d, no content" % (mods_index, mod.param_offset)

			#self.meta.data.mods[str(mods_index)] = data_mod

		self.meta.data.samples = ObjDict()



	def fill_meta_header(self):
		super(ModsDecompiler, self).fill_meta_header()

		self.meta.header2 = ObjDict()
		self.meta.header2.count_mods = self.library.header2.count_mods
		self.meta.header2.count_samples = self.library.header2.count_samples
		self.meta.header2.foo = self.library.header2.foo



	def fill_meta_fat(self):
		self.meta.fat_mods = ObjDict()
		self.meta.fat_mods.offsets = ObjDict()

		print "Mods count: %d" % self.library.header2.count_mods

		for offset_index, offset in enumerate(self.library.fat_mods.offsets):
			print "Offset #%d: %d" % (offset_index, offset)

			self.meta.fat_mods.offsets[str(offset_index)] = offset

		self.meta.fat_samples = ObjDict()
		self.meta.fat_samples.offsets = ObjDict()

		print "Samples count: %d" % self.library.header2.count_samples

		for offset_index, offset in enumerate(self.library.fat_samples.offsets):
			print "Offset #%d: %d" % (offset_index, offset)

			self.meta.fat_samples.offsets[str(offset_index)] = offset
