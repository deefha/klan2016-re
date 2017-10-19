#!/usr/bin/python

import os, sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../libs/")

from decompilers import *



if len(sys.argv) != 3:
	# TODO message
	sys.exit()

ARG_ISSUE = sys.argv[1]
ARG_SOURCE = sys.argv[2]



print "Issue: %s" % ARG_ISSUE
print "Source: %s" % ARG_SOURCE

if ARG_SOURCE == "font":
	decompiler = FontDecompiler.FontDecompiler(ARG_ISSUE, ARG_SOURCE)

else:
	sys.exit()



decompiler.fill_meta_header()
decompiler.fill_meta_fat()
decompiler.fill_meta_data()
decompiler.export_meta()
