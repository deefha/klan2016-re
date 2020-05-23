# -*- coding: utf-8 -*-

# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
import array
import binascii
import struct
from .CommonRemaker import CommonRemaker



class MusicRemaker(CommonRemaker):

	PATTERN_FILE_CONTENT = "%s%04d/content.bin"

	PERIODS = [ 1712, 1616, 1525, 1440, 1357, 1281, 1209, 1141, 1077, 1017, 961, 907, 856, 808, 762, 720, 678, 640, 604, 570, 538, 508, 480, 453, 428, 404, 381, 360, 339, 320, 302, 285, 269, 254, 240, 226, 214, 202, 190, 180, 170, 160, 151, 143, 135, 127, 120, 113, 107, 101, 95, 90, 85, 80, 76, 71, 67, 64, 60, 57 ]



	def export_assets(self):
		for mod_index, mod in self.meta_decompiled.data.mods.items():
			#if mod.content:
			if mod_index == "0" or mod_index == "1" or mod_index == "2":
				struct_sources = []

				# song title - 20 B
				struct_sources.append(("20s", "ModuleTitleModuleTit"))

				# sample headers 1-31
				for sample_index, sample_id in enumerate(mod.content.data.samples):
					if sample_index > 0:
						if sample_id == 65535:
							# sample name - 22 B
							#struct_sources.append(("22s", binascii.hexlify(array.array("c", "\0" * 22))))
							struct_sources.append(("22s", 'SampleNameSampleNameSa'))
							# sample length in words - 2 B
							struct_sources.append((">H", 0))
							# sample finetune - 1 B
							struct_sources.append(("B", 0))
							# sample volume - 1 B
							struct_sources.append(("B", 0))
							# sample repeatstart in words - 2 B
							struct_sources.append((">H", 0))
							# sample repeatlength in words - 2 B
							struct_sources.append((">H", 0))
						else:
							sample = self.meta_decompiled.data.samples[str(sample_id)]

							# sample name - 22 B
							struct_sources.append(("22s", "SampleNameSampleNameSa"))
							# sample length in words - 2 B
							struct_sources.append((">H", sample.content.data_size / 2))
							# sample finetune - 1 B
							struct_sources.append(("B", 0))
							# sample volume - 1 B
							struct_sources.append(("B", 64)) # TODO
							# sample repeatstart in words - 2 B
							struct_sources.append((">H", sample.content.loop_start / 2))
							# sample repeatlength in words - 2 B
							struct_sources.append((">H", (sample.content.loop_end - sample.content.loop_start) / 2))

				# number of song positions !played! - 1 B
				struct_sources.append(("B", mod.content.count_sequences))

				# foo - 1 B
				struct_sources.append(("B", 0))

				# pattern table - 128x 1 B
				for pattern_id in mod.content.data.sequences:
					struct_sources.append(("B", pattern_id))

				# vendor - 4 B
				struct_sources.append(("4s", "M.K."))

				# patterns - 64x 16 B
				for pattern_index, pattern in mod.content.data.patterns.items():
					with open(pattern.replace("blobs://", self.ROOT_BLOBS), "rb") as f:
						for row_index in range(64):
							# first 4 channels
							for channel_index in range(4):
								channel_data_instrument, channel_data_period, channel_data_effect_1, channel_data_effect_2 = struct.unpack("4B", f.read(4))

								channel_data_instrument_ub = channel_data_instrument >> 4
								channel_data_instrument_lb = channel_data_instrument << 4
								if channel_data_period == 255:
									channel_data_period_tr = 0
								else:
									channel_data_period_tr = self.PERIODS[channel_data_period]

								struct_sources.append((">H", channel_data_instrument_ub | channel_data_period_tr))
								struct_sources.append(("B", channel_data_instrument_lb | channel_data_effect_1))
								struct_sources.append(("B", channel_data_effect_2))

							# skip next 4 channels
							f.read(16)

				# final write
				with open("%s%04d.mod" % (self.PATH_ASSETS, int(mod_index)), "wb") as f:
					# structure
					for struct_source in struct_sources:
						struct_source_format = struct_source[0]
						struct_source_value = struct_source[1]

						f.write(struct.pack(struct_source_format, struct_source_value))

					# samples data
					for sample_index, sample_id in enumerate(mod.content.data.samples):
						if sample_index > 0:
							if sample_id == 65535:
								continue
							else:
								with open(self.meta.data.samples[str(sample_id)].content.data.content.replace("blobs://", self.ROOT_BLOBS), "rb") as f_sample:
									sample_data = f_sample.read()
									f.write(sample_data)



	def fill_scheme(self):
		super(MusicRemaker, self).fill_scheme()

		self.scheme.mods = ObjDict()

		for mod_index, mod in self.meta.data.mods.items():
			if mod.content:
				data_mod = ObjDict()
				#data_mod.width = mod.content.width
				#data_mod.height = mod.content.height
				data_mod.asset = "assets://%s/%s/%s/%04d.mod" % (self.issue.number, self.source.library, self.source_index, int(mod_index))

				self.scheme.mods[mod_index] = data_mod
