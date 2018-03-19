# -*- coding: utf-8 -*-

# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
from PIL import Image
from CommonRemaker import CommonRemaker



class TextsRemaker(CommonRemaker):

	PATTERN_FILE_COLORMAP = "%s%04d/colormap.bin"
	PATTERN_FILE_CONTENT = "%s%04d/content.bin"

	chartable = u"ČüéďäĎŤčěĚĹÍľĺÄÁÉžŽôöÓůÚýÖÜŠĽÝŘťáíóúňŇŮÔšřŕŔ¼§▴▾                           Ë   Ï                 ß         ë   ï ±  ®©  °   ™"



	def export_assets(self):
		for text_index, text in tqdm(self.meta_decompiled.data.texts.iteritems(), total=len(self.meta_decompiled.data.texts), desc="data.texts", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"):
			self.items_total += 1
			status = True

			data_text = u""

			if text.linetable:
				for linetable_index, linetable in text.linetable.iteritems():
					if linetable.content.pieces:
						for piece_index, piece in linetable.content.pieces.iteritems():
							# konec radku
							if piece.raw == 0:
								data_text += "\n"
							# font
							elif piece.raw == 1:
								continue
							# bold
							elif piece.raw == 2:
								continue
							# italic
							elif piece.raw == 4:
								continue
							# obrazek
							elif piece.raw == 8:
								continue
							# odkaz
							elif piece.raw == 9:
								continue
							# mezera
							elif piece.raw == 32:
								data_text += " "
							# bezny znak
							else:
								if piece.raw < 128:
									data_text += chr(piece.raw)
								else:
									data_text += self.chartable[piece.raw - 128]

			with open("%s%04d.txt" % (self.PATH_DATA_REMAKED, int(text_index)), "w") as f:
				f.write(data_text.encode("utf8", "replace"))

					#i = Image.frombytes("RGB", (text.content.width, text.content.height), text_content, "raw", "BGR;16")
					#i.save("%s%04d.png" % (self.PATH_DATA_REMAKED, int(text_index)))

				## colormap, indexed, RLE compression
				## 1 (#00+)
				## 257 (#09+)
				#if text.content.mode == 1 or text.content.mode == 257:
					#with open(text.content.data.colormap.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
						#text_colormap = f.read()

					#with open(text.content.data.content.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
						#text_content = f.read()

					#text_content_unpacked = []
					#content_byte_break = True
					#content_byte_break_length = None
					#content_byte_break_count = None

					#for content_byte in text_content:
						#if content_byte_break:
							#if ord(content_byte) > 127:
								#content_byte_break_length = ord(content_byte) - 127
								#content_byte_break_count = None
							#else:
								#content_byte_break_length = None
								#content_byte_break_count = ord(content_byte) + 1

							#content_byte_break = False
						#else:
							#if content_byte_break_count:
								#text_content_unpacked.extend([content_byte] * content_byte_break_count)
								#content_byte_break = True
							#else:
								#text_content_unpacked.append(content_byte)
								#content_byte_break_length -= 1
								
								#if not content_byte_break_length:
									#content_byte_break = True

					#text_content_unpacked = "".join(text_content_unpacked)

					#i = Image.frombytes("P", (text.content.width, text.content.height), text_content_unpacked)
					#i.putpalette(text_colormap)
					#i.save("%s%04d.png" % (self.PATH_DATA_REMAKED, int(text_index)))

				## colormap, indexed, no compression
				## 256 (#00+)
				#elif text.content.mode == 256:
					#with open(text.content.data.colormap.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
						#text_colormap = f.read()

					#with open(text.content.data.content.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
						#text_content = f.read()

						#i = Image.frombytes("P", (text.content.width, text.content.height), text_content)
						#i.putpalette(text_colormap)
						#i.save("%s%04d.png" % (self.PATH_DATA_REMAKED, int(text_index)))

				## TODO, red placeholder
				## 4 (#06+)
				## 258 (#11+)
				#elif text.content.mode == 4 or text.content.mode == 258:
					#status = False

					#i = Image.new("RGB", (text.content.width, text.content.height), (255, 0, 0))
					#i.save("%s%04d.png" % (self.PATH_DATA_REMAKED, int(text_index)))

				## RGB565
				## 5 (#11+)
				## 261 (#11+)
				#elif text.content.mode == 5 or text.content.mode == 261:
					#with open(text.content.data.content.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
						#text_content = f.read()

						#i = Image.frombytes("RGB", (text.content.width, text.content.height), text_content, "raw", "BGR;16")
						#i.save("%s%04d.png" % (self.PATH_DATA_REMAKED, int(text_index)))

			if status:
				self.items_hit += 1
			else:
				self.items_miss += 1



	def fill_meta(self):
		super(TextsRemaker, self).fill_meta()

		self.meta_remaked.texts = ObjDict()

		for text_index, text in self.meta_decompiled.data.texts.iteritems():
			data_text = ObjDict()
			data_text.asset = "remaked://%s/%s/%s/%04d.txt" % (self.issue.number, self.source.library, self.source_index, int(text_index))

			self.meta_remaked.texts[text_index] = data_text
