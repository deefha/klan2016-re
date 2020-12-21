#!/usr/bin/env python3

# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from tqdm import tqdm
from colorama import init as colorama_init, Fore, Back, Style

PATH_SELF = os.path.dirname(os.path.realpath(__file__))

# specific imports
sys.path.insert(0, "%s/%s" % (PATH_SELF, "../libs/"))
import tools.KlanTools as KlanTools
import libarchive.public


colorama_init(autoreset=True)

# TODO argparse
if len(sys.argv) != 2:
	# TODO message
	sys.exit()

ARG_ISSUE_NUMBER = sys.argv[1]

FILE_CONFIG = "%s/%s" % (PATH_SELF, "../data/config.yml")
PATH_INITIALIZED = "%s/%s" % (PATH_SELF, "../data/initialized/")
PATTERN_FILE_CHECK = "%s/%s" % (PATH_SELF, "../data/initialized/%s.check")
PATTERN_FILE_ISSUE_ISO = "%s/%s" % (PATH_SELF, "../data/initialized/%s.iso")
PATTERN_FILE_ISSUE_PACKED = "%s/%s" % (PATH_SELF, "../data/initialized/%s.7z")


def initialize_loop_issues(config, issue_number):
	if issue_number == "all":
		for issue_id, issue in sorted(config.issues.items()):
			initialize(config, issue)
	else:
		try:
			initialize(config, config.issues[issue_number])
		except KeyError as err:
			print('I got a KeyError - reason "%s"' % str(err)) # TODO message


def initialize(config, issue):
	print(Fore.BLACK + Back.GREEN + "Issue #%s" % issue.number)

	file_check = PATTERN_FILE_CHECK % issue.number
	file_issue_iso = PATTERN_FILE_ISSUE_ISO % issue.number
	file_issue_packed = PATTERN_FILE_ISSUE_PACKED % issue.number

	if os.path.isfile(file_check):
		os.remove(file_check)

	while True:
		status = True

		# check ISO issue existence
		if os.path.isfile(file_issue_iso):
			print("\tISO exists")
		else:
			print("\tISO not exists")
			status = False

		# check ISO issue size by config
		if os.path.isfile(file_issue_iso):
			print("\tChecking ISO size...")

			issue_iso_size = os.path.getsize(file_issue_iso)

			if issue_iso_size == issue.origin.size:
				print(Style.DIM + "\tISO size OK (%s)" % issue_iso_size)
			else:
				print(Fore.RED + "\tISO size error (%s != %s)" % (issue_iso_size, issue.origin.size))
				status = False

		# check ISO issue MD5 by config
		if os.path.isfile(file_issue_iso):
			print("\tChecking ISO MD5...")

			issue_iso_md5 = KlanTools.issue_iso_md5(config, issue, file_issue_iso)

			if issue_iso_md5 == issue.origin.md5:
				print(Style.DIM + "\tISO MD5 OK (%s)" % issue_iso_md5)
			else:
				print(Fore.RED + "\tISO MD5 error (%s != %s)" % (issue_iso_md5, issue.origin.md5))
				status = False

		# is issue ok?
		if status:
			break

		# if not, first remeove issue file
		if os.path.isfile(file_issue_iso):
			os.remove(file_issue_iso)

		# download packed issue
		if os.path.isfile(file_issue_packed):
			print("\tPacked origin exists, not downloading (%s)" % os.path.basename(file_issue_packed))
		else:
			print("\tDownloading packed origin... (%s => %s)" % (issue.origin.key, os.path.basename(file_issue_packed)))
			KlanTools.issue_download(config, issue, file_issue_packed)

		# check packed size by config
		if os.path.isfile(file_issue_packed):
			print("\tChecking packed size...")

			issue_packed_size = os.path.getsize(file_issue_packed)

			if issue_packed_size == issue.origin.size_packed:
				print(Style.DIM + "\tPacked size OK (%s)" % issue_packed_size)
			else:
				print(Fore.RED + "\tPacked size error (%s != %s)" % (issue_packed_size, issue.origin.size_packed))
				return

		# check packed md5 by config
		if os.path.isfile(file_issue_packed):
			print("\tChecking packed MD5...")

			issue_packed_md5 = KlanTools.issue_packed_md5(config, issue, file_issue_packed)

			if issue_packed_md5 == issue.origin.md5_packed:
				print(Style.DIM + "\tPacked MD5 OK (%s)" % issue_packed_md5)
			else:
				print(Fore.RED + "\tPacked MD5 error (%s != %s)" % (issue_packed_md5, issue.origin.md5_packed))
				return

		# unpack issue
		if os.path.isfile(file_issue_packed):
			print("\tUnpacking origin... (%s/%s => %s)" % (os.path.basename(file_issue_packed), issue.origin.filename, os.path.basename(file_issue_iso)))

			with libarchive.public.file_reader(file_issue_packed) as e:
				for entry in e:
					# TODO check existence
					if entry.pathname == issue.origin.filename:
						with open(file_issue_iso, "wb") as f:
							with tqdm(total=entry.size, unit="B", unit_scale=True, ascii=True, leave=False) as pbar: 
								for block in entry.get_blocks():
									f.write(block)
									pbar.update(len(block))

		# is packed issue ok?
		if os.path.isfile(file_issue_iso):
			print(Style.DIM + "\tUnpacking OK")
		else:
			print(Fore.RED + "\tUnpacking error, file %s not found" % issue.origin.filename)
			return

	# issue done
	print(Fore.GREEN + "\tChecking OK")

	# write check file
	with open(file_check, "w") as f:
		print("\tWriting check file...")
		f.write(datetime.datetime.utcnow().replace(microsecond=0).isoformat())


def main():
	config = KlanTools.config_load(FILE_CONFIG)
	initialize_loop_issues(config, ARG_ISSUE_NUMBER)


if __name__ == "__main__":
	main()
