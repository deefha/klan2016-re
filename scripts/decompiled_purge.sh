#!/bin/bash

find ../data/blobs -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} +
find ../data/meta -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} +
