#!/bin/bash

# ksc -t php --php-namespace "Klan\Parser" ./font.ksy
ksc -t python ./font.ksy

# ksc -t graphviz ./font.ksy
# dot ./klan_font.dot -Tpng -o ./klan_font.png
# dot ./klan_font.dot -Tsvg -o ./klan_font.svg
