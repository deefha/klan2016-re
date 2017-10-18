#!/usr/bin/python

import os, sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../libs/")

from decompilators import *



if len(sys.argv) != 3:
	# TODO message
	sys.exit()

ARG_ISSUE = sys.argv[1]
ARG_SOURCE = sys.argv[2]



print "Issue: %s" % ARG_ISSUE
print "Source: %s" % ARG_SOURCE

if ARG_SOURCE == "font":
	decompilator = FontDecompilator.FontDecompilator(ARG_ISSUE, ARG_SOURCE)

else:
	sys.exit()



decompilator.fill_meta_header()
decompilator.fill_meta_fat()
decompilator.fill_meta_data()
decompilator.export_meta()
