#!/bin/bash

for FILENAME in ../structs/*.ksy; do
	echo "Compiling $FILENAME"
	ksc --target python --outdir ../libs/structs/ --import-path ../structs/ $FILENAME
done
