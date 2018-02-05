# common imports
import os, sys, datetime
from objdict import ObjDict

# specific imports
from CommonDecompiler import CommonDecompiler



class ImagesDecompiler(CommonDecompiler):

	PATTERN_PATH_IMAGE = "%s%04d/"
	PATTERN_FILE_COLORMAP = "%s%04d/colormap.bin"
	PATTERN_FILE_CONTENT = "%s%04d/content.bin"
	PATTERN_FILE_HEADER = "%s%04d/header.bin"

	def fill_meta_data(self):
		super(ImagesDecompiler, self).fill_meta_data()

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
				data_image.content.data.param_data_size = image.content.data.param_data_size

				if image.content.mode == 1 or image.content.mode == 256 or image.content.mode == 257:
					data_image.content.data.colormap = "blobs://%s/%s/%s/%04d/colormap.bin" % (self.issue.number, self.source.library, self.source_index, image_index)

					print "\tColormap"
					f = open(file_colormap, "wb")
					f.write(image.content.data.colormap)
					f.close

				elif image.content.mode == 4:
					data_image.content.data.foo = image.content.data.foo
					data_image.content.data.header_size = image.content.data.header_size
					data_image.content.data.header = "blobs://%s/%s/%s/%04d/header.bin" % (self.issue.number, self.source.library, self.source_index, image_index)

					print "\tHeader"
					f = open(file_header, "wb")
					f.write(image.content.data.header)
					f.close

				data_image.content.data.content = "blobs://%s/%s/%s/%04d/content.bin" % (self.issue.number, self.source.library, self.source_index, image_index)

				print "\tContent"
				f = open(file_content, "wb")
				f.write(image.content.data.content)
				f.close

			else:
				print "Image #%d: param_offset=%d, no content" % (image_index, image.param_offset)

			self.meta.data.images[str(image_index)] = data_image
