#!/usr/bin/python

import os, sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../libs/")

from pprint import pprint
import pycdlib
import requests
from io import BytesIO
from tqdm import tqdm

from structs.klan_mods_v1 import KlanModsV1

#iso = pycdlib.PyCdlib()
#extracted = BytesIO()

#iso.open("/mnt/bigboss/backup/deefha/klan2011/klan-00.iso")

##for child in iso.list_dir(iso_path='/'):
	##print(child.file_identifier())

#iso.get_file_from_iso_fp(extracted, iso_path="/MODS.LIB;1")
#iso.close()

#extracted.seek(0)

#library = KlanModsV1.from_io(extracted)

session = requests.Session()
response = session.get("https://docs.google.com/uc?export=download", params = { "id": "0Bw1iZK6iA4_xT1hUTjJ3Zkwwa0k" }, stream = True)

for key, value in response.cookies.items():
	if key.startswith("download_warning"):
		response = session.get("https://docs.google.com/uc?export=download", params = { "id": "0Bw1iZK6iA4_xT1hUTjJ3Zkwwa0k", "confirm": value }, stream = True)

response_size = 575526912
chunk_size = 32 * 1024

with open("./download.iso", "wb") as f:
	with tqdm(total=response_size, unit='B', unit_scale=True, unit_divisor=1024, ascii=True) as pbar: 
		for chunk in response.iter_content(chunk_size):
			if chunk:
				f.write(chunk)
				pbar.update(len(chunk))
