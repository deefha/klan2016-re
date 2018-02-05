#!/usr/bin/python

# common imports
import os, sys, datetime
from pprint import pprint
from colorama import init as colorama_init, Fore, Back, Style

# specific imports
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../libs/")
import tools.KlanTools as KlanTools
from decompilers import *



colorama_init(autoreset=True)

if len(sys.argv) != 3:
	# TODO message
	sys.exit()

ARG_ISSUE_NUMBER = sys.argv[1]
ARG_LIBRARY = sys.argv[2]

CONFIG_PATH = "../data/config.yml"
CHECK_PATH = "../data/origins/%s.check"
ISSUE_PATH = "../data/origins/%s.iso"



def decompile_loop_issues(config, issue_number, library):
	if issue_number == "all":
		for issue_id, issue in sorted(config.issues.iteritems()):
			decompile_loop_libraries(config, issue, library)
	else:
		try:
			decompile_loop_libraries(config, config.issues[issue_number], library)
		except KeyError, e:
			print 'I got a KeyError - reason "%s"' % str(e) # TODO message



def decompile_loop_libraries(config, issue, library):
	if library == "all":
		for library, sources in issue.libraries.iteritems():
			if sources:
				for source_index, source in enumerate(sources):
					decompile(config, issue, source, source_index)
	else:
		if issue.libraries[library]:
			for source_index, source in enumerate(issue.libraries[library]):
				decompile(config, issue, source, source_index)

	return True



def decompile(config, issue, source, source_index):
	print "Issue: %s" % issue.number
	print "Path: %s" % source.path
	print "Library: %s" % source.library
	print "Version: %s" % source.version
	print "Index: %s" % source_index

	if source.library == "cursors":
		decompiler = CursorsDecompiler.CursorsDecompiler(issue, source, source_index)

	elif source.library == "fonts":
		decompiler = FontsDecompiler.FontsDecompiler(issue, source, source_index)

	elif source.library == "images":
		decompiler = ImagesDecompiler.ImagesDecompiler(issue, source, source_index)

	elif source.library == "audio":
		decompiler = AudioDecompiler.AudioDecompiler(issue, source, source_index)

	elif source.library == "music":
		decompiler = MusicDecompiler.MusicDecompiler(issue, source, source_index)

	else:
		return False

	decompiler.fill_meta_header()
	decompiler.fill_meta_fat()
	decompiler.fill_meta_data()
	decompiler.export_meta()

	return True



def main():
	config = KlanTools.config_load(CONFIG_PATH)
	decompile_loop_issues(config, ARG_ISSUE_NUMBER, ARG_LIBRARY)



if __name__ == "__main__":
	main()
