#!/usr/bin/python

import os, sys
sys.path.insert(0, '../libs/')

from objdict import ObjDict
from klan_font import KlanFont

data = ObjDict()
font = KlanFont.from_file('../data/sources/00/font.lib')

data.header = ObjDict()
data.header.magic = font.header.magic
data.header.version = font.header.version
data.header.type = font.header.type
data.header.filesize = font.header.filesize
data.header.filetime = font.header.filetime
data.header.filedate = font.header.filedate
data.header.foo_1 = font.header.foo_1
data.header.foo_2 = font.header.foo_2
data.header.crc = font.header.crc

if not os.path.exists('../data/blobs/00/font/'):
	os.makedirs('../data/blobs/00/font/')

if not os.path.exists('../data/meta/00/font/'):
	os.makedirs('../data/meta/00/font/')

print data.dumps()

f = open('../data/meta/00/font.json', 'w')
f.write(data.dumps())
f.close

#print "Count: %d" % font.fat.count

#for index, offset in enumerate(font.fat.offsets):
	#print "Offset #%d: %d" % (index, offset)

#for index, font in enumerate(font.fonts):
	#if font:
		#print "Font #%d: offset=%d, datalength=%d, height=%d" % (index, font.offset, font.datalength, font.height)

		##print "\tColors"
		##for index, color in enumerate(font.colors):
			##print "\t\tColor #%d: R=%d, G=%d, B=%d" % (index, color.r, color.g, color.b)

		#print "\tCharacters"
		#for index, character in enumerate(font.characters):
			#if character.width:
				#print "\t\tCharacter #%d: offset=%d, width=%d" % (index, character.offset, character.width)

		#print "\tMatrices"
		#for index, matrix in enumerate(font.matrices):
			#if matrix:
				#print "\t\tMatrix #%d: width=%d, height=%d" % (index, matrix.width, matrix.height)

				#print "\t\t\tRows"
				#for index, row in enumerate(matrix.rows):
					#print "\t\t\t\tRow #%d:" % (index)

					#print "\t\t\t\t\tColumns"
					#for index, column in enumerate(row.columns):
						#print "\t\t\t\t\t\tColumn #%d: %d" % (index, column)
