# -*- coding: utf-8 -*-

# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm

# specific imports
from .CommonRemaker import CommonRemaker



class DescriptionsRemaker(CommonRemaker):

	CHARTABLE = u"ČüéďäĎŤčěĚĹÍľĺÄÁÉžŽôöÓůÚýÖÜŠĽÝŘťáíóúňŇŮÔšřŕŔ¼§▴▾                           Ë   Ï                 ß         ë   ï ±  ®©  °   ™   "



	def export_assets(self):
		for description_index, description in self.meta_decompiled.data.descriptions.items():
			if description.content:
				self.items_total += 1
				status = True

				if status:
					self.items_hit += 1
				else:
					self.items_miss += 1



	def fill_meta(self):
		super(DescriptionsRemaker, self).fill_meta()

		self.meta_remaked.descriptions = ObjDict()

		for description_index, description in self.meta_decompiled.data.descriptions.items():
			if description.content:
				description_title = ""
				with open(description.content.data.title.replace("decompiled://", self.PATH_PHASE_DECOMPILED), "rb") as f:
					description_title_temp = f.read()

				for char_index, char in enumerate(description_title_temp):
					if char < 32:
						break
					elif char < 128:
						description_title += chr(char)
					else:
						description_title += self.CHARTABLE[char - 128]

				data_description = ObjDict()
				data_description.title = description_title

				self.meta_remaked.descriptions[description_index] = data_description
