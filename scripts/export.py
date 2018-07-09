#!/usr/bin/python
# -*- coding: utf-8 -*-

# common imports
import datetime, os, sys
from objdict import ObjDict
from pprint import pprint
from colorama import init as colorama_init, Fore, Back, Style

# specific imports
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../libs/")
import json
import tools.KlanTools as KlanTools



colorama_init(autoreset=True)

if len(sys.argv) != 2:
	# TODO message
	sys.exit()

ARG_ISSUE_NUMBER = sys.argv[1]

CONFIG_PATH = "../data/config.yml"
CHECK_PATH = "../data/initialized/%s.check"
ISSUE_PATH = "../data/initialized/%s.iso"
MANIFEST_PATH = "../data/exported/manifest.json"
ISSUE_MANIFEST_PATH = "../data/exported/%s/manifest.json"



def export_loop_issues(config, issue_number):
	if issue_number == "all":
		for issue_id, issue in sorted(config.issues.iteritems()):
			export(config, issue)
	else:
		try:
			export(config, config.issues[issue_number])
		except KeyError, e:
			print 'I got a KeyError - reason "%s"' % str(e) # TODO message



def export(config, issue):
	print Fore.BLACK + Back.GREEN + "Issue #%s" % issue.number

	issue_manifest_path = ISSUE_MANIFEST_PATH % issue.number

	if not os.path.exists(os.path.dirname(os.path.realpath(issue_manifest_path))):
		os.makedirs(os.path.dirname(os.path.realpath(issue_manifest_path)))

	# write manifest file
	with open(issue_manifest_path, "w") as f:
		print "\tWriting manifest file..."
		f.write(issue.dumps())



def export_main(config):
	print Fore.BLACK + Back.GREEN + "Main"

	manifest = []

	for issue_id, issue in sorted(config.issues.iteritems()):
		manifest.append(issue.number)

	manifest_path = MANIFEST_PATH

	# write manifest file
	with open(manifest_path, "w") as f:
		print "\tWriting manifest file..."
		f.write(json.dumps(manifest))



def main():
	config = KlanTools.config_load(CONFIG_PATH)
	export_loop_issues(config, ARG_ISSUE_NUMBER)
	export_main(config)



if __name__ == "__main__":
	main()
