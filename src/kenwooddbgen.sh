#!/bin/sh

message() {
    local TITLE="Kenwood Database Generator"
    if [ -n "`which kdialog`" ]; then
        kdialog --error "$1" --title "$TITLE"
    elif [ -n "`which zenity`" ]; then
        zenity --error --title="$TITLE" --text="$1"
    elif [ -n "`which xmessage`" ]; then
        xmessage -center "ERROR: $TITLE: $1"
    elif [ -n "`which notify-send`" ]; then
        notify-send "ERROR: $TITLE: $1"
    else
        echo "ERROR: $TITLE\n$1"
    fi
}

currentDir=$(dirname "$0")
PYTHONPATH="${PYTHONPATH}:$currentDir"
export PYTHONPATH

if [ ! -d "$currentDir/venv" ]
then
    message "The application installation seems to be broken: it's missing Python virtual environment. If you installed the program manually without any package manger you might forget to run \"install-venv.sh\"."
    exit 1
fi

"$currentDir/venv/bin/python3" "$currentDir/program.py" "$@"
