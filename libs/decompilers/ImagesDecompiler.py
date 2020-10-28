# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
from .CommonDecompiler import CommonDecompiler


class ImagesDecompiler(CommonDecompiler):

	PATTERN_PATH_IMAGE = "%s%04d/"

	PATTERN_FILE_COLORMAP = "%s%04d/colormap.bin"
	PATTERN_FILE_CONTENT = "%s%04d/content.bin"
	PATTERN_FILE_HUFFTREE = "%s%04d/hufftree.bin"

	PATTERN_DECOMPILED_COLORMAP = "decompiled://%s/%s/%s/%04d/colormap.bin"
	PATTERN_DECOMPILED_CONTENT = "decompiled://%s/%s/%s/%04d/content.bin"
	PATTERN_DECOMPILED_HUFFTREE = "decompiled://%s/%s/%s/%04d/hufftree.bin"


	def fill_meta_data(self):
		super(ImagesDecompiler, self).fill_meta_data()

		self.meta.data.images = ObjDict()

		for image_index, image in enumerate(tqdm(self.library.data.images, desc="data.images", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):
			data_image = ObjDict()
			data_image.param_offset = image.param_offset
			data_image.content = ObjDict()

			if image.content:
				#print "Image #%d: param_offset=%d, data_size=%d, width=%d, height=%d, mode=%d" % (image_index, image.param_offset, image.content.data_size, image.content.width, image.content.height, image.content.mode)

				file_colormap = self.PATTERN_FILE_COLORMAP % (self.PATH_DATA, image_index)
				file_content = self.PATTERN_FILE_CONTENT % (self.PATH_DATA, image_index)
				file_hufftree = self.PATTERN_FILE_HUFFTREE % (self.PATH_DATA, image_index)

				path_image = self.PATTERN_PATH_IMAGE % (self.PATH_DATA, image_index)

				if not os.path.exists(path_image):
					os.makedirs(path_image)

				data_image.content.data_size = image.content.data_size
				data_image.content.width = image.content.width
				data_image.content.height = image.content.height
				data_image.content.mode = image.content.mode
				data_image.content.data = ObjDict()
				data_image.content.data.param_data_size = image.content.data.param_data_size

				if image.content.mode == 1 or image.content.mode == 256 or image.content.mode == 257 or image.content.mode == 258:
					data_image.content.data.colormap = self.PATTERN_DECOMPILED_COLORMAP % (self.issue.number, self.source.library, self.source_index, image_index)

					#print "\tColormap"
					with open(file_colormap, "wb") as f:
						f.write(image.content.data.colormap)

				elif image.content.mode == 4:
					data_image.content.data.quality = image.content.data.quality
					data_image.content.data.hufftree_size = image.content.data.hufftree_size
					data_image.content.data.hufftree = self.PATTERN_DECOMPILED_HUFFTREE % (self.issue.number, self.source.library, self.source_index, image_index)

					#print "\tHuffTree"
					with open(file_hufftree, "wb") as f:
						f.write(image.content.data.hufftree)

				data_image.content.data.content = self.PATTERN_DECOMPILED_CONTENT % (self.issue.number, self.source.library, self.source_index, image_index)

				#print "\tContent"
				with open(file_content, "wb") as f:
					f.write(image.content.data.content)

			#else:
				#print "Image #%d: param_offset=%d, no content" % (image_index, image.param_offset)

			self.meta.data.images[str(image_index)] = data_image
