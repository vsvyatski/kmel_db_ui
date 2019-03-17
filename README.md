# Kenwood Database Generator

A UI for the parser and generator for Kenwood Music Editor Light databases created by [Chris Willoughby](https://github.com/chrrrisw). I have actually forked it [here](https://github.com/vsvyatski/kmel_db) and added some improvements. The UI is based on [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro). Currently this program is meant to be used on Linux. Windows users can use the original [KENWOOD Music Editor Light](https://www2.jvckenwood.com/cs/ce/music_editor_light/english/index.html).

## Requirements
The application requires Python 3.5 or newer. Among packages it needs *PyQt5*, *asyncqt* and *hsaudiotag3k*.

## Building the application
There is the *build.sh* file in the root folder of the repository. Running it will create the *dist/kmeldb-ui* folder which is an unpacked redistributable of the application. The build script also supports the **-p** option that packs the build results into a target format and places the package into the *dist* directory. Supported formats are:
- *tgz* - a tar.gz archive, it's distribution independent, but requires manual installation
- *deb* - a deb package for Debian and derivatives
- *pacman* - a pkg.tar.xz package for ArchLinux and derivatives

## Manual installation
If you choose to use tar.gz archive (because, for instance, you posess a Linux distribution using a package manager that do not understand Debian or ArchLinux packages), then you need to perform an additional step after unpacking the archive. There will be the *install-venv.sh* file in your destination folder. It needs to be laucned before the first use of the program in order to generate a Python virtual environment in the destination folder. The virtual environment is needed to run the application. The distribution archive contains the *kenwooddbgen.sh* file. It's a launcher for the program. Just emit the following command in your terminal:
```bash
sh kenwooddbgen.sh
```
But an easier way would be to just create a shortcut on the desktop or in a menu somewhere for the aforementioned command.
