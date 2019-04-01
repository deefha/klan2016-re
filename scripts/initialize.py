#!/usr/bin/python
# -*- coding: utf-8 -*-

# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm
from colorama import init as colorama_init, Fore, Back, Style

# specific imports
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../libs/")
import tools.KlanTools as KlanTools
import libarchive.public



colorama_init(autoreset=True)

if len(sys.argv) != 2:
	# TODO message
	sys.exit()

ARG_ISSUE_NUMBER = sys.argv[1]

FILE_CONFIG = "../data/config.yml"
PATH_INITIALIZED = "../data/initialized/"
TEMPLATE_FILE_CHECK = "../data/initialized/%s.check"
TEMPLATE_FILE_ISSUE_PACKED = "../data/initialized/%s.7z"
TEMPLATE_FILE_ISSUE = "../data/initialized/%s.iso"



def initialize_loop_issues(config, issue_number):
	if issue_number == "all":
		for issue_id, issue in sorted(config.issues.iteritems()):
			initialize(config, issue)
	else:
		try:
			initialize(config, config.issues[issue_number])
		except KeyError, e:
			print 'I got a KeyError - reason "%s"' % str(e) # TODO message



def initialize(config, issue):
	print Fore.BLACK + Back.GREEN + "Issue #%s" % issue.number

	file_check = TEMPLATE_FILE_CHECK % issue.number
	file_issue_packed = TEMPLATE_FILE_ISSUE_PACKED % issue.number
	file_issue = TEMPLATE_FILE_ISSUE % issue.number

	if os.path.isfile(file_check):
		os.remove(file_check)

	# download packed issue
	if os.path.isfile(file_issue_packed):
		print "\tPacked origin exists, not downloading (%s)" % os.path.basename(file_issue_packed)
	elif os.path.isfile(file_issue):
		print "\tPacked origin not needed"
	else:
		print "\tDownloading packed origin... (%s => %s)" % (issue.origin.key, os.path.basename(file_issue_packed))

		KlanTools.issue_download(config, issue, file_issue_packed)

	# check packed size by config
	if os.path.isfile(file_issue_packed):
		print "\tChecking packed size..."

		issue_packed_size = os.path.getsize(file_issue_packed)

		if issue_packed_size == issue.origin.size_packed:
			print "\tPacked size OK (%s)" % issue_packed_size
		else:
			print "\tPacked size error (%s != %s)" % (issue_packed_size, issue.origin.size_packed)
			return

	# check packed md5 by config
	if os.path.isfile(file_issue_packed):
		print "\tChecking packed MD5..."

		issue_packed_md5 = KlanTools.issue_packed_md5(config, issue, file_issue_packed)

		if issue_packed_md5 == issue.origin.md5_packed:
			print "\tPacked MD5 OK (%s)" % issue_packed_md5
		else:
			print Fore.RED + "\tPacked MD5 error (%s != %s)" % (issue_packed_md5, issue.origin.md5_packed)
			return

	# unpack issue
	if os.path.isfile(file_issue_packed):
		print "\tUnpacking origin... (%s/%s => %s)" % (os.path.basename(file_issue_packed), issue.origin.filename, os.path.basename(file_issue))

		if os.path.isfile(file_issue):
			os.remove(file_issue)

		with libarchive.public.file_reader(file_issue_packed) as e:
			for entry in e:
				# todo check existence
				if entry.pathname == issue.origin.filename:
					with open(file_issue, "wb") as f:
						with tqdm(total=entry.size, unit="B", unit_scale=True, ascii=True, leave=False) as pbar: 
							for block in entry.get_blocks():
								f.write(block)
								pbar.update(len(block))

	if os.path.isfile(file_issue):
		print "\tUnpacking OK"
	else:
		print Fore.RED + "\tUnpacking error, file not found"
		return

	## skip checking if checked
	#if os.path.isfile(file_check):
		#with open(file_check, "r") as f:
			#check_date = f.read()

		#print Fore.GREEN + "\tChecked already (%s)" % check_date
		#return

	# check size by config
	if os.path.isfile(file_issue):
		print "\tChecking size..."

		issue_size = os.path.getsize(file_issue)

		if issue_size == issue.origin.size:
			print "\tSize OK (%s)" % issue_size
		else:
			print "\tSize error (%s != %s)" % (issue_size, issue.origin.size)
			return

	# check md5 by config
	if os.path.isfile(file_issue):
		print "\tChecking MD5..."

		issue_md5 = KlanTools.issue_md5(config, issue, file_issue)

		if issue_md5 == issue.origin.md5:
			print "\tMD5 OK (%s)" % issue_md5
		else:
			print Fore.RED + "\tMD5 error (%s != %s)" % (issue_md5, issue.origin.md5)
			return

	# issue done
	if os.path.isfile(file_issue):
		print Fore.GREEN + "\tChecking OK"
	else:
		print Fore.RED + "\tChecking error"
		return

	# write check file
	with open(file_check, "w") as f:
		print "\tWriting check file..."
		f.write(datetime.datetime.utcnow().replace(microsecond=0).isoformat())



def main():
	config = KlanTools.config_load(FILE_CONFIG)
	initialize_loop_issues(config, ARG_ISSUE_NUMBER)



if __name__ == "__main__":
	main()
