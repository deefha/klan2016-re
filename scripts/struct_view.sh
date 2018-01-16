#!/bin/bash

STRUCT=$1
ISSUE=$2
SOURCE=$3

ksv ../data/sources/$ISSUE/$SOURCE.lib ../structs/$STRUCT.ksy
