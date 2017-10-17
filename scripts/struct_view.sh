#!/bin/bash

STRUCT=$1
ISSUE=$2

ksv ../data/sources/$ISSUE/$STRUCT.lib ../structs/$STRUCT.ksy
