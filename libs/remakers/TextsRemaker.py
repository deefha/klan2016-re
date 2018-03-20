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
		with open("%s%s/%s/%s.json" % (self.PATH_PHASE_REMAKED, self.issue.number, "fonts", 0), "r") as f:
			#content = f.read()
			lines = f.readlines() # TODO
			content = ''.join(lines) # TODO

			self.fonts_0 = ObjDict(content)

		for text_index, text in tqdm(self.meta_decompiled.data.texts.iteritems(), total=len(self.meta_decompiled.data.texts), desc="data.texts", ascii=True, leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"):
			self.items_total += 1
			status = True

			data_text = u""

			if text.linetable:
				lines_width = 0
				lines_height = 0
				lines = []

				for linetable_index, linetable in text.linetable.iteritems():
					line_width = 0
					line_height = text.linetable_meta[linetable_index].content.height
					line_pieces = []

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

								i_piece = Image.new("RGBA", (piece.data.length, line_height), (0, 0, 0, 0))
								line_width += piece.data.length
								line_pieces.append(i_piece)
							# bezny znak
							else:
								if piece.raw < 128:
									data_text += chr(piece.raw)
								else:
									data_text += self.chartable[piece.raw - 128]

								#print "%s: %s, %s" % (text_index, linetable_index, piece_index)
								if str(piece.raw) in self.fonts_0.fonts["1"].characters:
									i_piece = Image.open("%s%s/%s/%s/%02d/normal/%03d.png" % (self.PATH_PHASE_REMAKED, self.issue.number, "fonts", 0, 1, piece.raw))
									i_piece_width, i_piece_height = i_piece.size
									line_width += i_piece_width
									line_pieces.append(i_piece)

					i_line = Image.new("RGBA", (line_width, line_height), (0, 0, 0, 0))
					line_offset_x = 0

					for line_piece in line_pieces:
						line_piece_width, line_piece_height = line_piece.size
						i_line.paste(line_piece, (line_offset_x, 0))
						line_offset_x += line_piece_width

					if line_width > lines_width:
						lines_width = line_width
					lines_height += line_height
					lines.append(i_line)

				i_lines_temp = Image.new("RGBA", (lines_width, lines_height), (0, 0, 0, 0))
				lines_offset_y = 0

				for line in lines:
					line_width, line_height = line.size
					i_lines_temp.paste(line, (0, lines_offset_y))
					lines_offset_y += line_height

				i_lines = Image.new("RGBA", (lines_width, lines_height), (0, 0, 0, 255))
				i_lines = Image.alpha_composite(i_lines, i_lines_temp)
				i_lines.save("%s%04d.png" % (self.PATH_DATA_REMAKED, int(text_index)))

			with open("%s%04d.txt" % (self.PATH_DATA_REMAKED, int(text_index)), "w") as f:
				f.write(data_text.encode("utf8", "replace"))

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
