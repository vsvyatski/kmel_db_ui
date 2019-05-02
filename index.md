---
layout: page
title: Kenwood Database Generator
---
Kenwood Database Generator is a replacement of Kenwood Music Editor Light for Linux. Basically it represents a graphic shell for [kmel_db command line utility](https://github.com/chrrrisw/kmel_db) created by Chris Willoughby.

## Purpose

It takes a FAT32 formatted USB drive with MP3 and WMA files and then creates a Kenwood DAP database on that drive, containing info about those files. The database can be later accessed by Kenwood Car Audio to index and play audio files. I created this application because the original Kenwood Music Editor light doesn't exist for Linux.

## Requirements

The application requires Python 3.5 or newer. Among packages it needs [PyQt5](https://pypi.org/project/PyQt5/), [asyncqt](https://pypi.org/project/asyncqt/) and [hsaudiotag3k](https://pypi.org/project/hsaudiotag3k/).

## Manual installation

If you choose to use tar.gz archive (because, for instance, you posess a Linux distribution using a package manager that do not understand Debian or ArchLinux packages), then you need to perform an additional step after unpacking the archive. There will be the *create-venv.sh* file in your destination folder. It needs to be laucned before the first use of the program in order to generate a Python virtual environment in the destination folder. The virtual environment is needed to run the application. The distribution archive contains the *kenwooddbgen.sh* file. It's the program's launcher. Just emit the following command in your terminal:

```bash
sh kenwooddbgen.sh
```

But an easier way would be to just create a shortcut on the desktop or in a menu somewhere for the aforementioned command. The icon for it can be found in the archive.
