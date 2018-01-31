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
		for phase_dir in ("assets", "blobs", "meta", "schemes"):
			purge_loop_issues(config, issue_number, library, phase_dir)
	else:
		if phase == "decompiled":
			for phase_dir in ("blobs", "meta"):
				purge_loop_issues(config, issue_number, library, phase_dir)
		if phase == "remaked":
			for phase_dir in ("assets", "schemes"):
				purge_loop_issues(config, issue_number, library, phase_dir)



def purge_loop_issues(config, issue_number, library, phase_dir):
	if issue_number == "all":
		for issue_id, issue in sorted(config.issues.iteritems()):
			purge_loop_libraries(config, issue, library, phase_dir)

			issue_dir = "../data/%s/%s" % (phase_dir, issue.number)
			if os.path.exists(issue_dir) and not os.listdir(issue_dir):
				print issue_dir
				os.rmdir(issue_dir)
	else:
		try:
			purge_loop_libraries(config, config.issues[issue_number], library, phase_dir)

			issue_dir = "../data/%s/%s" % (phase_dir, issue_number)
			if os.path.exists(issue_dir) and not os.listdir(issue_dir):
				print issue_dir
				os.rmdir(issue_dir)
		except KeyError, e:
			print 'I got a KeyError - reason "%s"' % str(e) # TODO message



def purge_loop_libraries(config, issue, library, phase_dir):
	if library == "all":
		for library, sources in issue.libraries.iteritems():
			if sources:
				for source_index, source in enumerate(sources):
					purge(config, issue, source, phase_dir)
	else:
		if issue.libraries[library]:
			for source_index, source in enumerate(issue.libraries[library]):
				purge(config, issue, source, phase_dir)



def purge(config, issue, source, phase_dir):
	print "../data/%s/%s/%s/" % (phase_dir, issue.number, source.library)
	shutil.rmtree("../data/%s/%s/%s/" % (phase_dir, issue.number, source.library), ignore_errors=True)



def main():
	config = KlanTools.config_load(CONFIG_PATH)

	purge_loop_phases(config, ARG_ISSUE_NUMBER, ARG_LIBRARY, ARG_PHASE)



if __name__ == "__main__":
	main()
