#!/bin/bash

currentDir=$(dirname "$0")
PYTHONPATH="${PYTHONPATH}:$currentDir"
export PYTHONPATH

"$currentDir/venv/bin/python3" "$currentDir/program.py" "$@"
