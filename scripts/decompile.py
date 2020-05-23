#!/usr/bin/env python
# -*- coding: utf-8 -*-

# common imports
import datetime, os, sys
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
CHECK_PATH = "../data/initialized/%s.check"
ISSUE_PATH = "../data/initialized/%s.iso"



def decompile_loop_issues(config, issue_number, library):
	if issue_number == "all":
		for issue_id, issue in sorted(config.issues.iteritems()):
			decompile_loop_libraries(config, issue, library)
	else:
		try:
			decompile_loop_libraries(config, config.issues[issue_number], library)
		except KeyError as err:
			print('I got a KeyError - reason "%s"' % str(err)) # TODO message



def decompile_loop_libraries(config, issue, library):
	print(Fore.BLACK + Back.GREEN + "Issue #%s" % issue.number)

	if library == "all":
		for library, sources in issue.libraries.items():
			if sources:
				for source_index, source in enumerate(sources):
					decompile(config, issue, source, source_index)
	else:
		if issue.libraries[library]:
			for source_index, source in enumerate(issue.libraries[library]):
				decompile(config, issue, source, source_index)

	return True



def decompile(config, issue, source, source_index):
	if source.library == "audio":
		decompiler = AudioDecompiler.AudioDecompiler(issue, source, source_index)

	elif source.library == "cursors":
		decompiler = CursorsDecompiler.CursorsDecompiler(issue, source, source_index)

	elif source.library == "descriptions":
		decompiler = DescriptionsDecompiler.DescriptionsDecompiler(issue, source, source_index)

	elif source.library == "fonts":
		decompiler = FontsDecompiler.FontsDecompiler(issue, source, source_index)

	elif source.library == "images":
		decompiler = ImagesDecompiler.ImagesDecompiler(issue, source, source_index)

	elif source.library == "music":
		decompiler = MusicDecompiler.MusicDecompiler(issue, source, source_index)

	elif source.library == "screens":
		decompiler = ScreensDecompiler.ScreensDecompiler(issue, source, source_index)

	elif source.library == "texts":
		decompiler = TextsDecompiler.TextsDecompiler(issue, source, source_index)

	else:
		return False

	decompiler.decompile()

	print(Fore.GREEN + "\tDecompiling OK")

	return True



def main():
	config = KlanTools.config_load(CONFIG_PATH)
	decompile_loop_issues(config, ARG_ISSUE_NUMBER, ARG_LIBRARY)



if __name__ == "__main__":
	main()
