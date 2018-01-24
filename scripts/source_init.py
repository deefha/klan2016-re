#!/usr/bin/python

import os, sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../libs/")

from pprint import pprint
import pycdlib
from io import BytesIO
from io import StringIO

from structs.klan_mods_v1 import KlanModsV1

iso = pycdlib.PyCdlib()
extracted = BytesIO()

iso.open("/mnt/bigboss/backup/deefha/klan2011/klan-00.iso")

#for child in iso.list_dir(iso_path='/'):
	#print(child.file_identifier())

iso.get_file_from_iso_fp(extracted, iso_path="/MODS.LIB;1")
iso.close()

extracted.seek(0)

library = KlanModsV1.from_io(extracted)
