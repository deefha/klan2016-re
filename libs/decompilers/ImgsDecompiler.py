import os, sys

from objdict import ObjDict
from CommonDecompiler import CommonDecompiler



class ImgsDecompiler(CommonDecompiler):

	PATTERN_PATH_IMAGE = "%s%04d/"
	PATTERN_FILE_COLORMAP = "%s%04d/colormap.bin"
	PATTERN_FILE_CONTENT = "%s%04d/content.bin"
	PATTERN_FILE_HEADER = "%s%04d/header.bin"

	def fill_meta_data(self):
		super(ImgsDecompiler, self).fill_meta_data()

		self.meta.data.images = ObjDict()

		for image_index, image in enumerate(self.library.data.images):
			data_image = ObjDict()
			data_image.param_offset = image.param_offset
			data_image.content = ObjDict()

			if image.content:
				print "Image #%d: param_offset=%d, data_size=%d, width=%d, height=%d, mode=%d" % (image_index, image.param_offset, image.content.data_size, image.content.width, image.content.height, image.content.mode)

				file_colormap = self.PATTERN_FILE_COLORMAP % (self.PATH_BLOBS, image_index)
				file_content = self.PATTERN_FILE_CONTENT % (self.PATH_BLOBS, image_index)
				file_header = self.PATTERN_FILE_HEADER % (self.PATH_BLOBS, image_index)

				path_image = self.PATTERN_PATH_IMAGE % (self.PATH_BLOBS, image_index)

				if not os.path.exists(path_image):
					os.makedirs(path_image)

				data_image.content.data_size = image.content.data_size
				data_image.content.width = image.content.width
				data_image.content.height = image.content.height
				data_image.content.mode = image.content.mode
				data_image.content.data = ObjDict()
				data_image.content.data.colormap = ""
				data_image.content.data.header = ""

				if image.content.mode == 1 or image.content.mode == 256 or image.content.mode == 257:
					data_image.content.data.colormap = "blobs://%s/imgs/%04d/colormap.bin" % (self.issue, image_index)

					print "\tColormap"
					f = open(file_colormap, "wb")
					f.write(image.content.data.colormap)
					f.close

				elif image.content.mode == 4:
					data_image.content.data.header = "blobs://%s/imgs/%04d/header.bin" % (self.issue, image_index)

					print "\tHeader"
					f = open(file_header, "wb")
					f.write(image.content.data.header)
					f.close

				data_image.content.data.content = "blobs://%s/imgs/%04d/content.bin" % (self.issue, image_index)

				print "\tContent"
				f = open(file_content, "wb")
				f.write(image.content.data.content)
				f.close

			else:
				print "Image #%d: param_offset=%d, no content" % (image_index, image.param_offset)

			self.meta.data.images[str(image_index)] = data_image
