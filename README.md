# Kenwood Database Generator

A UI for the parser and generator for Kenwood Music Editor Light databases created by [Chris Willoughby](https://github.com/chrrrisw). I have actually forked it [here](https://github.com/vsvyatski/kmel_db) and added some improvements. The UI is based on [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro). Currently this program is meant to be used on Linux. Windows users can use the original [KENWOOD Music Editor Light](https://www2.jvckenwood.com/cs/ce/music_editor_light/english/index.html).

## Requirements
The application requires Python 3.5 or newer. Among packages it needs *PyQt5*, *asyncqt* and *hsaudiotag3k*.

## Building the application
There is the *build.sh* file in the root folder of the repository. Running it will create the *dist/kmeldb-ui* folder which is an unpacked redistributable of the application. The build script also supports the **-p** flag that creates the *dist/kmeldb-ui.tar.gz* file, which is a packed redistributable. You can also use **-v \<version>** option together with **-p** to append the version number to the name of the archive. For instance, emitting
```bash
sh build.sh -p -v 0.2.0
```
will generate the *dist/kmeldb-ui-0.2.0.tar.gz* file.

## Launching the program
The distribution archive contains the *kenwooddbgen.sh* file. It's a launcher for the application. Just emit the following command in your terminal:
```bash
sh kenwooddbgen.sh
```
But an easier way would be to just create a shortcut on the desktop or in a menu somewhere for the aforementioned command.
