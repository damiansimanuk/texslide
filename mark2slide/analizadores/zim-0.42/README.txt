====== ABOUT ======

Zim - A Desktop Wiki Editor

Zim brings the concept of a wiki to your desktop. Store information,
link pages and edit with WYSISYG markup. Creating a new page is as easy
as linking to a non-existing page. Pages are stored in a folder structure,
like in an outliner, and can have attachments.

This tool can be used to keep track of TODO lists or ideas, to take notes
during a meeting or to draft any other kind of text (blog entries,
important mails, etc.).


====== COPYRIGHT ======

Copyright 2008, 2009 Jaap Karssenberg <pardus@cpan.org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.

== Translations ==

Translations are copyrighted by their respective translators.
All translations that are entered through the launchpad website
are distributed under the BSD license.

See the translation files for detailed translator credits.

== Included Files ==

The following files were included from other sources:

* zim/_lib/xdot.py - Copyright 2008 Jose Fonseca

From the default Gnome icon theme:
* pixmaps/task-list.png (was: stock_todo.png)
* pixmaps/attachment.png (was: mail-attachment.png)

From Gtk+ 2.8
* pixmaps/link.png (was: stock_connect_24.png)

Other:
* pixmaps/calendar.png (was: stock_calendar-view-month.png)
  Copyright 2007 by Jakub Steiner, released under GPL
  modifications copyright 2009 by Gabriel Hurley


====== INSTALLING ======

NOTE: To test zim it is not needed to install. You should be able to run it
      directly from the source directory by calling `./zim.py`. (To run a
      translated version from the source first call `./setup.py build_trans`.)


First you should verify you have the dependencies zim needs. To list all
dependencies check `./setup.py --requires`.

You will at least need the following:

	* gtk+ >= 2.6
	* python >= 2.5
	* python-gtk
	* python-gobject
	* python-xdg (optional, but recommended)
	* xdg-utils (optional, but recommended)
	* python-simplejson (for python < 2.6)

To verify zim is working properly on your system you can call the test suite
using `./test.py`. Failures do not have to be critical, but in principle all
tests should pass.

Zim can be installed from source using:

  ./setup.py install

Most plugins have additional requirements. These are listed in the plugin
descriptions.


===== Ubuntu =====

On Ubuntu or other debian derived systems, the following packages should be 
installed:

	* python
	* libgtk2.0-0
	* python-gtk2
	* python-xdg


===== Windows =====

To install gtk, python and python-gtk on Windows see the instructions at
http://www.pygtk.org . If you use python 2.5 you will also need to install the
python simplejson module. This can be obtained from http://pypi.python.org .
The python-xdg module is not usefull on Windows, so you can skip it.

Once the dependencies are fulfilled you can run zim directly from the source
directory.


===== Mac OS X =====

You can run zim on mac if you have the proper dependencies installed.
If you are using Mac Ports packages installing the following ports should work:

	* python25
	* py25-gtk
	* py25-simplejson
	* py25-xdg


===== Install Paths =====

If you install in a non-default location you may need to set the PYTHONPATH
environment variable in order for zim to find it's python modules.
For example, if you installed the modules below "/home/user/lib/zim" you need
to set:

	PYTHONPATH=/home/user/lib

Also zim uses the XDG paths to locate data and config files. If you get
an error that zim can not find it's data files
For example, if you installed the zim data files to "/home/user/share/zim"
you need to set the data path like this:

	XDG_DATA_DIRS=/home/user/share:/usr/local/share:/usr/share



====== PACKAGING ======

To build a tree in a target directory you can use:

	./setup.py install --root=/path/to/package/build/dir

Special attention may be needed to run xdg update commands in a post-install
script. Recommended commands are:

	update-desktop-database
	update-mime-database
	xdg-icon-resource install --context mimetypes \
		--size 64 zim.png application-x-zim-notebook



====== TRANSLATING ======

To contribute to translations onlne please go to http://launchpad.net.

To test a new translation you can either download the snapshot from launchpad
and run:

	./tools/import-launchpad-translations.py launchpad-export.tar.gz


Or you can edit the template zim.pot with your favourite editor. In that case
you should add you new .po file to the po/ directory.

After adding the .po file(s) you can compile the translation using:

	./setup build_trans


