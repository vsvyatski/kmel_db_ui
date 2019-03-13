#!/bin/sh

currentDir=$(dirname "$0")

echo Generating virtual environment...
python3 -m venv --system-site-packages "$currentDir/venv"
"$currentDir/venv/bin/pip3" install -r "$currentDir/requirements.txt"
