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
				if image.content.mode == 256:
					with open(image.content.data.colormap.replace("blobs://", self.ROOT_BLOBS), "rb") as f:
						image_colormap = f.read()

					with open(image.content.data.content.replace("blobs://", self.ROOT_BLOBS), "rb") as f:
						image_content = f.read()

						i = Image.frombytes("P", (image.content.width, image.content.height), image_content)
						i.putpalette(image_colormap)
						i.save("%s%04d.png" % (self.PATH_ASSETS, int(image_index)))



	def fill_scheme(self):
		super(ImgsRemaker, self).fill_scheme()

		self.scheme.images = ObjDict()

		for image_index, image in self.meta.data.images.iteritems():
			if image.content:
				data_image = ObjDict()
				data_image.width = image.content.width
				data_image.height = image.content.height
				data_image.asset = "assets://%s/imgs/%04d.png" % (self.issue, int(image_index))

				self.scheme.images[image_index] = data_image
