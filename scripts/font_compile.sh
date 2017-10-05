#!/bin/bash

ksc --target python --outdir ../libs/ --import-path ../structs/ ../structs/font.ksy

# ksc -t graphviz ./font.ksy
# dot ./klan_font.dot -Tpng -o ./klan_font.png
# dot ./klan_font.dot -Tsvg -o ./klan_font.svg
