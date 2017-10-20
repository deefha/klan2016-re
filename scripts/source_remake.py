#!/usr/bin/python

import os, sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../libs/")

from remakers import *



if len(sys.argv) != 3:
	# TODO message
	sys.exit()

ARG_ISSUE = sys.argv[1]
ARG_SOURCE = sys.argv[2]



print "Issue: %s" % ARG_ISSUE
print "Source: %s" % ARG_SOURCE

if ARG_SOURCE == "font":
	remaker = FontRemaker.FontRemaker(ARG_ISSUE, ARG_SOURCE)

else:
	sys.exit()



remaker.fill_scheme()
remaker.export_scheme()
remaker.export_assets()
