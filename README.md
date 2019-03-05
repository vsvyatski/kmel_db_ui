# Kenwood Database Generator

A UI for the parser and generator for Kenwood Music Editor Light databases created by [Chris Willoughby](https://github.com/chrrrisw).
I have actually forked it [here](https://github.com/vsvyatski/kmel_db) and added some improvements.
The UI is based on [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro). Currently this program is meant to
be used on Linux.

## Requirements
The application requires Python 3.5 or newer. Among packages it needs *PyQt5*, *asyncqt* and *hsaudiotag3k*.

## Launching the program
The distribution archive contains the kenwooddbgen.sh file. It's a launcher for the application. Just emit the following command in your terminal:
```bash
sh kenwooddbgen.sh
```
But an easier way would be to just create a shorcut on the desktop or in a menu somewhere for the aforementioned command.
