# common imports
import os, sys, datetime
from objdict import ObjDict
from tqdm import tqdm

# specific imports
from CommonDecompiler import CommonDecompiler



class MusicDecompiler(CommonDecompiler):

	PATTERN_PATH_MOD = "%s/mods/%04d/"
	PATTERN_PATH_MOD_PATTERNS = "%s/mods/%04d/patterns/"
	PATTERN_PATH_SAMPLE = "%s/samples/"

	PATTERN_FILE_MOD_PATTERN = "%s/mods/%04d/patterns/%04d.bin"
	PATTERN_FILE_MOD_PATTERNS = "%s/mods/%04d/patterns/content.bin"
	PATTERN_FILE_SAMPLE = "%s/samples/%04d.bin"

	PATTERN_DECOMPILED_MOD_PATTERN = "blobs://%s/%s/%s/mods/%04d/patterns/%04d.bin"
	PATTERN_DECOMPILED_MOD_PATTERNS = "blobs://%s/%s/%s/mods/%04d/patterns/content.bin"
	PATTERN_DECOMPILED_SAMPLE = "blobs://%s/%s/%s/samples/%04d.bin"

	def fill_meta_data(self):
		super(MusicDecompiler, self).fill_meta_data()

		self.meta.data.names = ObjDict()

		for names_index, name in enumerate(tqdm(self.library.data.names, desc="data.names", ascii=True, leave=True)):
			#self.meta.data.names[str(names_index)] = name
			self.meta.data.names[str(names_index)] = ""

		self.meta.data.mods = ObjDict()

		for mod_index, mod in enumerate(tqdm(self.library.data.mods, desc="data.mods", ascii=True, leave=True)):
			data_mod = ObjDict()
			data_mod.param_offset = mod.param_offset
			data_mod.content = ObjDict()

			if mod.content:
				if self.source.version == 1:
					#print "Mod #%d: param_offset=%d, name='%s', count_sequences=%d, count_patterns=%d, count_samples=%d, size_patterns=%d" % (mod_index, mod.param_offset, mod.content.name, mod.content.count_sequences, mod.content.count_patterns, mod.content.count_samples, mod.content.size_patterns)

					path_mod = self.PATTERN_PATH_MOD % (self.PATH_DATA, mod_index)
					path_mod_patterns = self.PATTERN_PATH_MOD_PATTERNS % (self.PATH_DATA, mod_index)

					if not os.path.exists(path_mod):
						os.makedirs(path_mod)

					if not os.path.exists(path_mod_patterns):
						os.makedirs(path_mod_patterns)

					#data_mod.content.name = mod.content.name
					data_mod.content.name = ""
					data_mod.content.count_sequences = mod.content.count_sequences
					data_mod.content.count_patterns = mod.content.count_patterns
					data_mod.content.count_samples = mod.content.count_samples
					data_mod.content.foo_1 = mod.content.foo_1
					data_mod.content.size_patterns = mod.content.size_patterns
					data_mod.content.foo_2 = mod.content.foo_2

					data_mod.content.data = ObjDict()
					data_mod.content.data.param_count_patterns = mod.content.data.param_count_patterns
					data_mod.content.data.samples = mod.content.data.samples
					data_mod.content.data.sequences = mod.content.data.sequences
					data_mod.content.data.patterns = ObjDict()

					for pattern_index, pattern in enumerate(tqdm(mod.content.data.patterns, desc="mod.content.data.patterns", ascii=True, leave=True)):
						file_pattern = self.PATTERN_FILE_MOD_PATTERN % (self.PATH_DATA, mod_index, pattern_index)

						data_mod.content.data.patterns[str(pattern_index)] = self.PATTERN_DECOMPILED_MOD_PATTERN % (self.issue.number, self.source.library, self.source_index, mod_index, pattern_index)

						#print "\tPattern #%d" % pattern_index
						f = open(file_pattern, "wb")
						f.write(pattern)
						f.close

				elif self.source.version == 2:
					#print "Mod #%d: param_offset=%d, name='%s', count_samples=%d, size_patterns=%d" % (mod_index, mod.param_offset, mod.content.name, mod.content.count_samples, mod.content.size_patterns)

					path_mod = self.PATTERN_PATH_MOD % (self.PATH_DATA, mod_index)
					path_mod_patterns = self.PATTERN_PATH_MOD_PATTERNS % (self.PATH_DATA, mod_index)

					if not os.path.exists(path_mod):
						os.makedirs(path_mod)

					if not os.path.exists(path_mod_patterns):
						os.makedirs(path_mod_patterns)

					#data_mod.content.name = mod.content.name
					data_mod.content.name = ""
					data_mod.content.count_samples = mod.content.count_samples
					data_mod.content.size_patterns = mod.content.size_patterns
					data_mod.content.foo_1 = mod.content.foo_1
					data_mod.content.foo_2 = mod.content.foo_2

					data_mod.content.data = ObjDict()
					data_mod.content.data.param_size_patterns = mod.content.data.param_size_patterns
					data_mod.content.data.samples = mod.content.data.samples

					file_patterns = self.PATTERN_FILE_MOD_PATTERNS % (self.PATH_DATA, mod_index)

					data_mod.content.data.patterns = self.PATTERN_DECOMPILED_MOD_PATTERNS % (self.issue.number, self.source.library, self.source_index, mod_index)

					#print "\tPatterns"
					f = open(file_patterns, "wb")
					f.write(mod.content.data.patterns)
					f.close

			#else:
				#print "Mod #%d: param_offset=%d, no content" % (mod_index, mod.param_offset)

			self.meta.data.mods[str(mod_index)] = data_mod

		self.meta.data.samples = ObjDict()

		for sample_index, sample in enumerate(tqdm(self.library.data.samples, desc="data.samples", ascii=True, leave=True)):
			data_sample = ObjDict()
			data_sample.param_offset = sample.param_offset
			data_sample.content = ObjDict()

			if sample.content:
				if self.source.version == 1:
					#print "Sample #%d: param_offset=%d" % (sample_index, sample.param_offset)

					path_sample = self.PATTERN_PATH_SAMPLE % (self.PATH_DATA)

					if not os.path.exists(path_sample):
						os.makedirs(path_sample)

					data_sample.content.data_size = sample.content.data_size
					data_sample.content.loop_start = sample.content.loop_start
					data_sample.content.loop_end = sample.content.loop_end
					#data_sample.content.foo = sample.content.foo
					data_sample.content.foo = ""

					data_sample.content.data = ObjDict()
					data_sample.content.data.param_data_size = sample.content.data.param_data_size

					file_sample = self.PATTERN_FILE_SAMPLE % (self.PATH_DATA, sample_index)

					data_sample.content.data.content = self.PATTERN_DECOMPILED_SAMPLE % (self.issue.number, self.source.library, self.source_index, sample_index)

					#print "\tContent"
					f = open(file_sample, "wb")
					f.write(sample.content.data.content)
					f.close

				elif self.source.version == 2:
					#print "Sample #%d: param_offset=%d" % (sample_index, sample.param_offset)

					path_sample = self.PATTERN_PATH_SAMPLE % (self.PATH_DATA)

					if not os.path.exists(path_sample):
						os.makedirs(path_sample)

					data_sample.content.data_size = sample.content.data_size
					#data_sample.content.foo = sample.content.foo
					data_sample.content.foo = ""

					data_sample.content.data = ObjDict()
					data_sample.content.data.param_data_size = sample.content.data.param_data_size

					file_sample = self.PATTERN_FILE_SAMPLE % (self.PATH_DATA, sample_index)

					data_sample.content.data.content = self.PATTERN_DECOMPILED_SAMPLE % (self.issue.number, self.source.library, self.source_index, sample_index)

					#print "\tContent"
					f = open(file_sample, "wb")
					f.write(sample.content.data.content)
					f.close

			#else:
				#print "Sample #%d: param_offset=%d, no content" % (sample_index, sample.param_offset)

			self.meta.data.samples[str(sample_index)] = data_sample



	def fill_meta_header(self):
		super(MusicDecompiler, self).fill_meta_header()

		self.meta.header2 = ObjDict()
		self.meta.header2.count_mods = self.library.header2.count_mods
		self.meta.header2.count_samples = self.library.header2.count_samples
		self.meta.header2.foo = self.library.header2.foo



	def fill_meta_fat(self):
		self.meta.fat_mods = ObjDict()
		self.meta.fat_mods.offsets = ObjDict()

		#print "Mods count: %d" % self.library.header2.count_mods

		for offset_index, offset in enumerate(tqdm(self.library.fat_mods.offsets, desc="fat_mods.offsets", ascii=True, leave=True)):
			#print "Offset #%d: %d" % (offset_index, offset)

			self.meta.fat_mods.offsets[str(offset_index)] = offset

		self.meta.fat_samples = ObjDict()
		self.meta.fat_samples.offsets = ObjDict()

		#print "Samples count: %d" % self.library.header2.count_samples

		for offset_index, offset in enumerate(tqdm(self.library.fat_samples.offsets, desc="fat_samples.offsets", ascii=True, leave=True)):
			#print "Offset #%d: %d" % (offset_index, offset)

			self.meta.fat_samples.offsets[str(offset_index)] = offset
