#!/usr/bin/python

import os, sys
sys.path.insert(0, '../libs/')

from PIL import Image

from objdict import ObjDict
from klan_font import KlanFont

data = ObjDict()
font = KlanFont.from_file('../data/sources/00/font.lib')

data.header = ObjDict()
data.header.magic = font.header.magic
data.header.version = font.header.version # TODO hexa?
data.header.type = font.header.type
data.header.filesize = font.header.filesize
data.header.filetime = font.header.filetime # TODO ISO date
data.header.filedate = font.header.filedate # TODO ISO date
data.header.foo_1 = font.header.foo_1
data.header.foo_2 = font.header.foo_2
data.header.crc = font.header.crc # TODO check?!

data.fat = ObjDict()
data.fat.count = font.fat.count
data.fat.offsets = ObjDict()

data.data = ObjDict()
data.data.fonts = ObjDict()

if not os.path.exists('../data/blobs/00/font/'):
	os.makedirs('../data/blobs/00/font/')

if not os.path.exists('../data/meta/00/font/'):
	os.makedirs('../data/meta/00/font/')

print "Count: %d" % font.fat.count

for offset_index, offset in enumerate(font.fat.offsets):
	print "Offset #%d: %d" % (offset_index, offset)

	data.fat.offsets[str(offset_index)] = offset

for font_index, font in enumerate(font.data.fonts):
	data_font = ObjDict()
	data_font.offset = font.offset
	data_font.content = ObjDict()

	if font.content:
		print "Font #%d: offset=%d, matrices_size=%d, height=%d" % (font_index, font.offset, font.content.matrices_size, font.content.height)

		data_font.content.matrices_size = font.content.matrices_size
		data_font.content.height = font.content.height
		data_font.content.colormap = 'blobs://00/font/%02d/colormap.bin' % font_index
		data_font.content.characters = ObjDict()
		data_font.content.matrices = ObjDict()

		if not os.path.exists('../data/blobs/00/font/%02d/' % font_index):
			os.makedirs('../data/blobs/00/font/%02d/' % font_index)

		if not os.path.exists('../data/blobs/00/font/%02d/matrices/' % font_index):
			os.makedirs('../data/blobs/00/font/%02d/matrices/' % font_index)

		if not os.path.exists('../data/objects/00/font/%02d/characters/' % font_index):
			os.makedirs('../data/objects/00/font/%02d/characters/' % font_index)

		print "\tColormap"
		f = open('../data/blobs/00/font/%02d/colormap.bin' % font_index, 'wb')
		f.write(font.content.colormap)
		f.close

		print "\tCharacters"
		for character_index, character in enumerate(font.content.characters):
			data_character = ObjDict()
			data_character.offset_and_width = character.offset_and_width
			data_character.offset = character.offset
			data_character.width = character.width

			if character.width:
				print "\t\tCharacter #%d: offset=%d, width=%d" % (character_index, character.offset, character.width)

			data_font.content.characters[str(character_index)] = data_character

		print "\tMatrices"
		for matrix_index, matrix in enumerate(font.content.matrices):
			data_matrix = ObjDict()

			if matrix.content:
				print "\t\tMatrix #%d" % (matrix_index)

				data_matrix.content = 'blobs://00/font/%02d/matrices/%03d.bin' % (font_index, matrix_index)

				f = open('../data/blobs/00/font/%02d/matrices/%03d.bin' % (font_index, matrix_index), 'wb')
				f.write(matrix.content)
				f.close

				i = Image.frombytes('P', (font.content.characters[matrix_index].width, font.content.height), matrix.content)
				i.putpalette(font.content.colormap)
				i.save('../data/objects/00/font/%02d/characters/%03d.gif' % (font_index, matrix_index))

			data_font.content.matrices[str(matrix_index)] = data_matrix

	else:
		print "Font #%d: offset=%d, no content" % (font_index, font.offset)

	data.data.fonts[str(font_index)] = data_font

f = open('../data/meta/00/font.json', 'w')
f.write(data.dumps())
f.close
