import os, sys, pprint

from objdict import ObjDict
from PIL import Image

from CommonRemaker import CommonRemaker



class ImgsRemaker(CommonRemaker):

	PATTERN_FILE_COLORMAP = "%s%04d/colormap.bin"
	PATTERN_FILE_CONTENT = "%s%04d/content.bin"

	def export_assets(self):
		for image_index, image in self.meta.data.images.iteritems():
			if image.content:
				if image.content.mode == 1 or image.content.mode == 257:
					with open(image.content.data.colormap.replace("blobs://", self.ROOT_BLOBS), "rb") as f:
						image_colormap = f.read()

					with open(image.content.data.content.replace("blobs://", self.ROOT_BLOBS), "rb") as f:
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
					i.save("%s%04d.png" % (self.PATH_ASSETS, int(image_index)))

				elif image.content.mode == 256:
					with open(image.content.data.colormap.replace("blobs://", self.ROOT_BLOBS), "rb") as f:
						image_colormap = f.read()

					with open(image.content.data.content.replace("blobs://", self.ROOT_BLOBS), "rb") as f:
						image_content = f.read()

						i = Image.frombytes("P", (image.content.width, image.content.height), image_content)
						i.putpalette(image_colormap)
						i.save("%s%04d.png" % (self.PATH_ASSETS, int(image_index)))

				elif image.content.mode == 4:
					i = Image.new("RGB", (image.content.width, image.content.height), (255, 0, 0))
					i.save("%s%04d.png" % (self.PATH_ASSETS, int(image_index)))



	def fill_scheme(self):
		super(ImgsRemaker, self).fill_scheme()

		self.scheme.images = ObjDict()

		for image_index, image in self.meta.data.images.iteritems():
			if image.content:
				data_image = ObjDict()
				data_image.width = image.content.width
				data_image.height = image.content.height
				data_image.asset = "assets://%s/%s/%04d.png" % (self.issue, self.source, int(image_index))

				self.scheme.images[image_index] = data_image
