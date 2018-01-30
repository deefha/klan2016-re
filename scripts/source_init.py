#!/usr/bin/python

# common imports
import os, sys, datetime
from pprint import pprint
from colorama import init as colorama_init, Fore, Back, Style

# specific imports
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../libs/")
#import pycdlib
#from io import BytesIO
#from structs.klan_mods_v1 import KlanModsV1

import tools.KlanTools as KlanTools



colorama_init(autoreset=True)

if len(sys.argv) != 2:
	# TODO message
	sys.exit()

ARG_ISSUE = sys.argv[1]

CONFIG_PATH = "../data/config.yml"
CHECK_PATH = "../data/sources/%s.check"
ISSUE_PATH = "../data/sources/%s.iso"



#iso = pycdlib.PyCdlib()
#extracted = BytesIO()

#iso.open("/mnt/bigboss/backup/deefha/klan2011/klan-00.iso")

##for child in iso.list_dir(iso_path='/'):
	##print(child.file_identifier())

#iso.get_file_from_iso_fp(extracted, iso_path="/MODS.LIB;1")
#iso.close()

#extracted.seek(0)

#library = KlanModsV1.from_io(extracted)



def init(config, issue):
	print Fore.BLACK + Back.GREEN + "Issue #%s" % issue.id

	check_path = CHECK_PATH % issue.id
	issue_path = ISSUE_PATH % issue.id

	# download missing issues
	if os.path.isfile(issue_path):
		print "\tSource exists"
	else:
		print "\tDownloading source..."

		if os.path.isfile(check_path):
			os.remove(check_path)

		KlanTools.issue_download(config, issue, issue_path)

	# skip checking if checked
	if os.path.isfile(check_path):
		with open(check_path, "r") as f:
			check_date = f.read()

		print Fore.GREEN + "\tChecked already (%s)" % check_date
		return

	# check size by config
	if not os.path.isfile(issue_path):
		print Fore.RED + "\tCan not check size"
		return
	else:
		print "\tChecking size..."

		while True:
			issue_size = os.path.getsize(issue_path)

			if issue_size == issue.origin.size:
				print "\tSize OK (%s)" % issue_size
				break
			else:
				print "\tSize error (%s != %s)" % (issue_size, issue.origin.size)
				print "\tDownloading source..."
				KlanTools.issue_download(config, issue, issue_path)

	# check md5 by config
	if not os.path.isfile(issue_path):
		print Fore.RED + "\tCan not check MD5 signature"
		return
	else:
		print "\tChecking MD5 signature..."

		issue_md5 = KlanTools.issue_md5(config, issue, issue_path)

		if issue_md5 == issue.origin.md5:
			print "\tMD5 signature OK (%s)" % issue_md5
		else:
			print Fore.RED + "\tMD5 signature error (%s != %s)" % (issue_md5, issue.origin.md5)
			return

	# write check file
	with open(check_path, "w") as f:
		print "\tWriting check file..."
		f.write(datetime.datetime.utcnow().replace(microsecond=0).isoformat())

	# issue done
	if not os.path.isfile(issue_path):
		print Fore.RED + "\tChecking error"
	else:
		print Fore.GREEN + "\tChecking OK"



def main():
	config = KlanTools.config_load(CONFIG_PATH)

	if ARG_ISSUE == "all":
		for issue_id, issue in config.issues.iteritems():
			init(config, issue)
	else:
		init(config, config.issues[ARG_ISSUE])



if __name__ == "__main__":
	main()
