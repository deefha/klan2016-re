#!/usr/bin/python

import os, sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../libs/")

from remakers import *

ISSUES = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32-33", "34", "35", "36", "37", "38", "39", "40", "41", "42"]
SOURCES = ["font", "font2", "font_lt", "font2_lt", "imgs", "image1", "cache"]

if len(sys.argv) != 3:
	# TODO message
	sys.exit()

ARG_ISSUE = sys.argv[1]
ARG_SOURCE = sys.argv[2]



def remake_issue(issue, source):
	if (source == "all"):
		for source in SOURCES:
			remake_source(issue, source)
	else:
		remake_source(issue, source)

	return True



def remake_source(issue, source):
	if issue < "01" and source == "font2":
		return False
	if issue < "01" and source == "image1":
		return False
	if issue < "28" and source == "font_lt":
		return False
	if issue < "28" and source == "font2_lt":
		return False
	if issue < "28" and source == "cache":
		return False
	if issue >= "28" and source == "image1":
		return False

	print "Issue: %s" % issue
	print "Source: %s" % source

	if source == "font" or source == "font2" or source == "font_lt" or source == "font2_lt":
		remaker = FontRemaker.FontRemaker(issue, source)

	elif source == "imgs" or source == "image1" or source == "cache":
		remaker = ImgsRemaker.ImgsRemaker(issue, source)

	else:
		return False

	remaker.fill_scheme()
	remaker.export_scheme()
	remaker.export_assets()

	return True



def main():
	if ARG_ISSUE == "all":
		for issue in ISSUES:
			remake_issue(issue, ARG_SOURCE)
	else:
		remake_issue(ARG_ISSUE, ARG_SOURCE)



main()
