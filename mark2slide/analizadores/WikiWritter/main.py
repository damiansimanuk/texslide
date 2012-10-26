#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import tempfile
import codecs
import highlighter

from PyQt4 import QtGui, QtCore
from app_ui import Ui_MainWindow
from WikiParser import launch

__version__ = "0.1 beta"
__author__ = "Christophe Kibleur"

# GLOBALS
f = codecs.open('template.html', 'r', 'utf-8')
TPL = f.read()
f.close()

APPLIREP = os.path.abspath(os.path.dirname(__file__))
SNIPREP = os.path.join(APPLIREP,"Snippets")
VIEW = os.path.join(APPLIREP,"view.html")

# keys


# We start a new class here
# derived from QMainWindow and Ui_MainWindow

class TestApp(QtGui.QMainWindow, Ui_MainWindow):
    VIEWACTIVATOR = "F1" # To refresh the HTML View
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
               
        ## Syntax highlighting
        self.highlighter = highlighter.Highlighter(self.ui.orig_text.document())
        self.highlighter.modeRest()

        ## Connect the refresButton and F1 key to a message method.
        self.connect(self.ui.refresh, QtCore.SIGNAL("clicked()"), self.do_html)
        QtGui.QShortcut(QtGui.QKeySequence(self.VIEWACTIVATOR), 
                        self, self.do_html)
               
        ## SIGNALS AND SLOTS
        self.connect(self.ui.actionHelp, QtCore.SIGNAL("triggered()"), 
                    self.showHelp)
        
        ## STATUSBAR
        self.statusBar().showMessage("Welcome to WikiWriter, press F1 to update your Browser.")
        
        

    def do_html(self, orig_text=""):
        if orig_text=="" :
            SOURCE = unicode(self.ui.orig_text.document().toPlainText())
        else:
            SOURCE = orig_text
        #print SOURCE
        result = launch(SOURCE, full=True)
        #result = parse_text(SOURCE)

        f = codecs.open("view.html",'w','utf-8')
        f.write(TPL%result)
        f.close()
    
        self.ui.webView.setUrl(QtCore.QUrl.fromLocalFile(VIEW))
        
        # textedit
        self.ui.gen_text.setPlainText(result)
        
    def showHelp(self):
        helptext = """[[nowiki]]= header level 1[[/nowiki]]

= header level 1

----

[[nowiki]]== header level 2[[/nowiki]]

== header level 2

----

[[nowiki]]=== header level 3[[/nowiki]]

== header level 3

----

[[nowiki]]**bold**[[/nowiki]]  

**bold**

----

[[nowiki]]//italics//[[/nowiki]]  

//italics//

----

[[nowiki]]{{monospaced}}[[/nowiki]]

{{monospaced}}

----

[[nowiki]]--del--[[/nowiki]]

--del--

----

[[nowiki]]__underlined__[[/nowiki]]

__underlined__

----

[[nowiki]]//**bold** italics **--deleted--**//[[/nowiki]]  

//**bold** italics **--deleted--**//

----

[[nowiki]][http://twitter.com/|Twitter][[/nowiki]]  

[http://twitter.com/|Twitter]

----

[[nowiki]][[im http://assets0.twitter.com/images/twitter.png?1214697409|http://twitter.com/|center|Twitter image]][[/nowiki]]

[[im http://assets0.twitter.com/images/twitter.png?1214697409|http://twitter.com/|center|Twitter image]]

----"""

        self.ui.webView.setHtml(self.do_html(helptext))       
        
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ## Change le look de l'appli
    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
    ## et la palette correspondante
    QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
    window = TestApp()
    window.show()
    sys.exit(app.exec_())
