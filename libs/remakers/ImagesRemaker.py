# -*- coding: utf-8 -*-

# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
from PIL import Image
from CommonRemaker import CommonRemaker



class ImagesRemaker(CommonRemaker):

	PATTERN_FILE_COLORMAP = "%s%04d/colormap.bin"
	PATTERN_FILE_CONTENT = "%s%04d/content.bin"



	def export_assets(self):
		for image_index, image in tqdm(self.meta_decompiled.data.images.iteritems(), total=len(self.meta_decompiled.data.images), desc="data.images", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"):
			if image.content:
				self.items_total += 1
				status = True

				# colormap, indexed, RLE compression
				# 1 (#00+)
				# 257 (#09+)
				if image.content.mode == 1 or image.content.mode == 257:
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
							if ord(content_byte) > 127:
								content_byte_break_length = ord(content_byte) - 127
								content_byte_break_count = None
							else:
								content_byte_break_length = None
								content_byte_break_count = ord(content_byte) + 1

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

					image_content_unpacked = "".join(image_content_unpacked)

					i = Image.frombytes("P", (image.content.width, image.content.height), image_content_unpacked)
					i.putpalette(image_colormap)
					i.save("%s%04d.png" % (self.PATH_DATA_REMAKED, int(image_index)))

				# colormap, indexed, no compression
				# 256 (#00+)
				elif image.content.mode == 256:
					with open(image.content.data.colormap.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
						image_colormap = f.read()

					with open(image.content.data.content.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
						image_content = f.read()

						i = Image.frombytes("P", (image.content.width, image.content.height), image_content)
						i.putpalette(image_colormap)
						i.save("%s%04d.png" % (self.PATH_DATA_REMAKED, int(image_index)))

				# TODO, red placeholder
				# 4 (#06+)
				# 258 (#11+)
				elif image.content.mode == 4 or image.content.mode == 258:
					status = False

					i = Image.new("RGB", (image.content.width, image.content.height), (255, 0, 0))
					i.save("%s%04d.png" % (self.PATH_DATA_REMAKED, int(image_index)))

				# RGB565
				# 5 (#11+)
				# 261 (#11+)
				elif image.content.mode == 5 or image.content.mode == 261:
					with open(image.content.data.content.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
						image_content = f.read()

						i = Image.frombytes("RGB", (image.content.width, image.content.height), image_content, "raw", "BGR;16")
						i.save("%s%04d.png" % (self.PATH_DATA_REMAKED, int(image_index)))

				if status:
					self.items_hit += 1
				else:
					self.items_miss += 1



	def fill_meta(self):
		super(ImagesRemaker, self).fill_meta()

		self.meta_remaked.images = ObjDict()

		for image_index, image in self.meta_decompiled.data.images.iteritems():
			if image.content:
				data_image = ObjDict()
				data_image.width = image.content.width
				data_image.height = image.content.height
				data_image.mode = image.content.mode
				data_image.asset = "remaked://%s/%s/%s/%04d.png" % (self.issue.number, self.source.library, self.source_index, int(image_index))

				self.meta_remaked.images[image_index] = data_image
