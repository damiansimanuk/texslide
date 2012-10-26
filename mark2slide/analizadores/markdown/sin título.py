#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  sin título.py
#  
#  Copyright 2012 Damian Simanuk <sima@sima-arch>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


# -*- coding: utf-8 -*-
import cmd

class Console(cmd.Cmd):

    prompt = "> "

    _colors = {‘red’: ‘#FF0000′,
               ‘white’: ‘#FFFFFF’,
               ‘black’: ‘#000000′}

    def __init__ (self):
        """Constructor"""
        cmd.Cmd.__init__(self)

    def do_hello (self, name):
        """Says hello to someone"""
        print "Hello %s!" % name

    def do_get_color (self, color):
        """Prints out the hex representation of a color"""
        if color in self._colors:
            print "%s: %s" % (color, self._colors[color])
        else:
            print "I don’t know: %s" % color

    def complete_get_color (self, text, line, begidx, endix):
        """Complete function for get_color"""
        return [i for i in self._colors if i.startswith(text)]

    def do_quit (self, s):
        print "Bye, bye…"
        return True

    def help_quit (self):
        print "Quits the console"

    do_EOF = do_quit
    help_EOF = help_quit

if __name__ == "__main__":
    console = Console()
    try:
        console.cmdloop("Hola!")
    except KeyboardInterrupt:
        console.do_quit(None)
