import os, sys

from objdict import ObjDict
from CommonRemaker import CommonRemaker



class FontRemaker(CommonRemaker):

	PATTERN_PATH_MATRICES = "%s%02d/matrices/"
	PATTERN_FILE_COLORMAP = "%s%02d/colormap.bin"
	PATTERN_FILE_MATRIX = "%s%03d.bin"
