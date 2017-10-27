#!/bin/bash

find ../data/assets -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} +
find ../data/schemes -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} +
