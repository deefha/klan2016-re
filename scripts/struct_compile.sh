#!/bin/bash

STRUCT=$1

ksc --target python --outdir ../libs/structs/ --import-path ../structs/ ../structs/$STRUCT.ksy

# ksc -t graphviz ./font.ksy
# dot ./klan_font.dot -Tpng -o ./klan_font.png
# dot ./klan_font.dot -Tsvg -o ./klan_font.svg
