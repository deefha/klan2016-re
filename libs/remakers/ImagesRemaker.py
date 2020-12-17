# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
from PIL import Image
from .CommonRemaker import CommonRemaker


class ImagesRemaker(CommonRemaker):

	def __init__(self, issue, source, source_index):
		super(ImagesRemaker, self).__init__(issue, source, source_index)

		self.descriptions = ObjDict()

		print("Loading descriptions...")

		if self.issue.number >= "06":
			with open("%s%s/%s/0.json" % (self.PATH_PHASE_REMAKED, self.issue.number, "descriptions"), "r") as f:
				lines = f.readlines() # TODO
				content = ''.join(lines) # TODO
				self.descriptions = ObjDict(content)


	def export_assets(self):
		for image_index, image in tqdm(self.meta_decompiled.data.images.items(), total=len(self.meta_decompiled.data.images), desc="data.images", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"):
			if image.content:
				self.items_total += 1
				status = True

				# 256 colors, indexed, no compression
				# 0x0100 - M256 (#00+)
				if image.content.mode == 0x0100:
					with open(image.content.data.colormap.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
						image_colormap = f.read()

					with open(image.content.data.content.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
						image_content = f.read()

						i = Image.frombytes("P", (image.content.width, image.content.height), image_content)
						i.putpalette(image_colormap)
						i.save("%s%04d.png" % (self.PATH_DATA_REMAKED, int(image_index)))

				# 256 colors, indexed, custom RLE compression
				# 0x0001 - M1 (#00+)
				# 0x0101 - M257 (#09+)
				elif image.content.mode == 0x0001 or image.content.mode == 0x0101:
					with open(image.content.data.colormap.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
						image_colormap = f.read()

					with open(image.content.data.content.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
						image_content = f.read()

					image_content_unpacked = []
					content_byte_break = True
					content_byte_break_length = None
					content_byte_break_count = None

					for content_byte in image_content:
						if content_byte_break:
							if content_byte > 127:
								content_byte_break_length = content_byte - 127
								content_byte_break_count = None
							else:
								content_byte_break_length = None
								content_byte_break_count = content_byte + 1

							content_byte_break = False
						else:
							if content_byte_break_count:
								image_content_unpacked.extend([content_byte] * content_byte_break_count)
								content_byte_break = True
							else:
								image_content_unpacked.append(content_byte)
								content_byte_break_length -= 1

								if not content_byte_break_length:
									content_byte_break = True

					#image_content_unpacked = "".join(image_content_unpacked)

					i = Image.frombytes("P", (image.content.width, image.content.height), bytes(image_content_unpacked))
					i.putpalette(image_colormap)
					i.save("%s%04d.png" % (self.PATH_DATA_REMAKED, int(image_index)))

				# 256 colors, indexed, custom LZSS compression
				# 0x0102 - M258 (#11+)
				elif image.content.mode == 0x0102:
					with open(image.content.data.colormap.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
						image_colormap = f.read()

					with open(image.content.data.content.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
						image_content = f.read()

					image_content_unpacked = []

					image_buffer = []
					image_buffer_index = 4096 - 18
					for i in range(4096):
						image_buffer.append(0)

					content_byte_flags = True
					content_byte_flags_value = None
					content_byte_flags_index = None
					content_byte_reference = False
					content_byte_reference_value_first = None
					content_byte_reference_value_second = None

					for content_byte in image_content:
						if content_byte_flags:
							content_byte_flags_value = content_byte
							content_byte_flags_index = 0

							content_byte_flags = False
						else:
							#print("Flags: %s, flags index: %s, flag bit: %s" % (ord(content_byte_flags_value), content_byte_flags_index, ord(content_byte_flags_value) & (2 ** content_byte_flags_index)))

							if content_byte_flags_value & (2 ** content_byte_flags_index):
								image_content_unpacked.append(content_byte)
								#print("Image index: %s, buffer index: %s, value: %s, literal" % (len(image_content_unpacked) - 1, image_buffer_index, ord(image_content_unpacked[len(image_content_unpacked) - 1])))
								#print("---")

								image_buffer[image_buffer_index] = content_byte
								image_buffer_index += 1
								if image_buffer_index == 4096:
									image_buffer_index = 0

								content_byte_flags_index += 1
							else:
								if content_byte_reference:
									content_byte_reference_value_second = content_byte
									reference_index = ((content_byte_reference_value_second & 0xf0) << 4) + content_byte_reference_value_first
									reference_length = ((content_byte_reference_value_second & 0x0f) + 3)

									for x in range(reference_length):
										real_index = reference_index + x
										if real_index >= 4096:
											real_index -= 4096

										image_content_unpacked.append(image_buffer[real_index])
										#print("Image index: %s, buffer index: %s, value: %s, reference index: %s, length: %s, step: %s, real index: %s" % (len(image_content_unpacked) - 1, image_buffer_index, ord(image_content_unpacked[len(image_content_unpacked) - 1]), reference_index, reference_length, x, real_index))

										image_buffer[image_buffer_index] = image_buffer[real_index]
										image_buffer_index += 1
										if image_buffer_index == 4096:
											image_buffer_index = 0

									#print("---")

									content_byte_reference = False
									content_byte_flags_index += 1
								else:
									content_byte_reference_value_first = content_byte
									content_byte_reference = True

							if content_byte_flags_index > 7:
								content_byte_flags = True
								content_byte_flags_value = None
								content_byte_flags_index = None

					#image_content_unpacked = "".join(image_content_unpacked)

					i = Image.frombytes("P", (image.content.width, image.content.height), bytes(image_content_unpacked))
					i.putpalette(image_colormap)
					i.save("%s%04d.png" % (self.PATH_DATA_REMAKED, int(image_index)))

				# RGB565, no compression
				# 0x0005 - M5 (#11+)
				# 0x0105 - M261 (#11+)
				elif image.content.mode == 0x0005 or image.content.mode == 0x0105:
					with open(image.content.data.content.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
						image_content = f.read()

						i = Image.frombytes("RGB", (image.content.width, image.content.height), image_content, "raw", "BGR;16")
						i.save("%s%04d.png" % (self.PATH_DATA_REMAKED, int(image_index)))

				# RGBX8888, custom Huffman compression
				# 0x0004 - M4 (#06+)
				elif image.content.mode == 0x0004:
					os.system("%s/scripts/unhuff.so %s %s %s %s %s %s" % (
						self.ROOT_ROOT,
						image.content.width,
						image.content.height,
						image.content.data.quality,
						image.content.data.hufftree.replace("decompiled://", self.PATH_PHASE_DECOMPILED),
						image.content.data.content.replace("decompiled://", self.PATH_PHASE_DECOMPILED),
						"%s%04d.tmp" % (self.PATH_DATA_REMAKED, int(image_index))
					))

					with open("%s%04d.tmp" % (self.PATH_DATA_REMAKED, int(image_index)), "rb") as f:
						image_content = f.read()

						i = Image.frombytes("RGB", (image.content.width, image.content.height), image_content, "raw", "BGRX")
						i.save("%s%04d.png" % (self.PATH_DATA_REMAKED, int(image_index)))

					os.remove("%s%04d.tmp" % (self.PATH_DATA_REMAKED, int(image_index)))

				if status:
					self.items_hit += 1
				else:
					self.items_miss += 1


	def fill_meta(self):
		super(ImagesRemaker, self).fill_meta()

		self.meta_remaked.images = ObjDict()

		for image_index, image in self.meta_decompiled.data.images.items():
			if image.content:
				data_image = ObjDict()
				data_image.width = image.content.width
				data_image.height = image.content.height
				data_image.mode = image.content.mode
				data_image.title = ""
				data_image.asset = "remaked://%s/%s/%s/%04d.png" % (self.issue.number, self.source.library, self.source_index, int(image_index))

				if hasattr(self.descriptions, "descriptions") and hasattr(self.descriptions.descriptions, str(image_index)):
					data_image.title = self.descriptions.descriptions[str(image_index)].title

				self.meta_remaked.images[image_index] = data_image
