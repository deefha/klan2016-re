#!/usr/bin/python

# common imports
import os, sys, datetime
from pprint import pprint
from colorama import init as colorama_init, Fore, Back, Style

# specific imports
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../libs/")
import shutil
import tools.KlanTools as KlanTools



colorama_init(autoreset=True)

if len(sys.argv) != 4:
	# TODO message
	sys.exit()

ARG_ISSUE_NUMBER = sys.argv[1]
ARG_LIBRARY = sys.argv[2]
ARG_PHASE = sys.argv[3]

CONFIG_PATH = "../data/config.yml"



def purge_loop_phases(config, issue_number, library, phase):
	if phase == "all":
		for phase in ("decompiled", "remaked"):
			purge_loop_issues(config, issue_number, library, phase)
	else:
		if phase == "decompiled":
			purge_loop_issues(config, issue_number, library, phase)

		elif phase == "remaked":
			purge_loop_issues(config, issue_number, library, phase)



def purge_loop_issues(config, issue_number, library, phase):
	if issue_number == "all":
		for issue_id, issue in sorted(config.issues.iteritems()):
			purge_loop_libraries(config, issue, library, phase)

			issue_dir = "../data/%s/%s" % (phase, issue.number)
			if os.path.exists(issue_dir) and not os.listdir(issue_dir):
				print issue_dir
				os.rmdir(issue_dir)
	else:
		try:
			purge_loop_libraries(config, config.issues[issue_number], library, phase)

			issue_dir = "../data/%s/%s" % (phase, issue_number)
			if os.path.exists(issue_dir) and not os.listdir(issue_dir):
				print issue_dir
				os.rmdir(issue_dir)
		except KeyError, e:
			print 'I got a KeyError - reason "%s"' % str(e) # TODO message



def purge_loop_libraries(config, issue, library, phase):
	if library == "all":
		for library, sources in issue.libraries.iteritems():
			if sources:
				for source_index, source in enumerate(sources):
					purge(config, issue, source, phase)
	else:
		if issue.libraries[library]:
			for source_index, source in enumerate(issue.libraries[library]):
				purge(config, issue, source, phase)



def purge(config, issue, source, phase):
	print "../data/%s/%s/%s/" % (phase, issue.number, source.library)
	shutil.rmtree("../data/%s/%s/%s/" % (phase, issue.number, source.library), ignore_errors=True)



def main():
	config = KlanTools.config_load(CONFIG_PATH)
	purge_loop_phases(config, ARG_ISSUE_NUMBER, ARG_LIBRARY, ARG_PHASE)



if __name__ == "__main__":
	main()
