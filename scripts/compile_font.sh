#!/bin/bash

# ksc -t php --php-namespace "Klan\Parser" ./font.ksy
# ksc --debug --target python --outdir "../libs/" --import-path "../libs/" ../structs/font.ksy
ksc -t python ../structs/font.ksy

# ksc -t graphviz ./font.ksy
# dot ./klan_font.dot -Tpng -o ./klan_font.png
# dot ./klan_font.dot -Tsvg -o ./klan_font.svg
