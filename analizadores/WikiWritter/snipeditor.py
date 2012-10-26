#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import string
import re
import xml.etree.cElementTree as ET # Phone home ?!

from PyQt4 import QtGui, QtCore
from SnipEngine import *
#import generic_highlighter
#from HL import genericHighlighter

def readSnippetsDefs(file):

    """Reads an XML file containing the snippets definitions and
    returns a dictionnary-like whose keys are the triggers
    to type, and the values are a 2-uplet(description',snippet).
    """
    templates = {}
    doc = ET.parse(str(file))
    entries = doc.findall("entry")
    for entry in entries:
        templates[entry.find("trigger").text] = (entry.find("description").text,entry.find("snippet").text)
    return templates

APPLIREP = os.path.abspath(os.path.dirname(__file__))
SNIPREP = os.path.join(APPLIREP,"Snippets")
SNIPDEFS = os.path.join(SNIPREP,"wiki_snippets.xml")
# Snippets
DICSNIP = readSnippetsDefs(SNIPDEFS)


class SnipEditor(QtGui.QTextEdit):

    def __init__(self, parent):
        QtGui.QTextEdit.__init__(self, parent)
        self.parent = parent
        
        
        ## EXTENSION MANAGEMENT
        self.setAcceptRichText(False)
        
        ## Customizations : show spaces, highlight current line, limit line
        self.line_col = QtGui.QColor("#502F2F")
        self.limit_color = QtGui.QColor("#C0000F")
        
        self.showSpaces = False         # not very useful, nor beautiful
        self.highlightCurrentLine = 0
        self.LimitLine = 78

        #self.doc = QtGui.QTextDocument(self)
        self.tab_long = 4
        self.setTabEditorWidth(self.tab_long)
        
        # Snippets special Variables
        self.insideSnippet = False
        self.start_snip = 0
        
        # Current field
        self.snippets = []
        self.field = None
        self.field_start = 0
        self.field_long = 0
        self.oldsnip = None
        
        self.connect(self, QtCore.SIGNAL("textChanged()"), self.updateChilds)

        
    def keyPressEvent(self, event):
        """Since PyQt4.4 we have to reimplement this to use 
        a Tab or Shift+Tab shortcut.
        """
        if event.key() == QtCore.Qt.Key_Tab:
            self.whatToDoOnTab()
        else:
            QtGui.QTextEdit.keyPressEvent(self, event)
            
    def printWhiteSpaces(self, e):
        # @param e : the event transmitted to the painEvent
        # p is our painter from paintEvent
        p = QtGui.QPainter(self.viewport())
        qp = QtGui.QPixmap("Images/pixmaps/spaces.png")
        contentsY = self.verticalScrollBar().value()
        pageBottom = contentsY + self.viewport().height()
        fm = QtGui.QFontMetrics(self.font())

        doc = self.document()
        block = doc.begin()

        while block.isValid() :

            layout = block.layout()
            boundingRect = layout.boundingRect()
            position = layout.position()

            if position.y() + boundingRect.height() < contentsY :
                block = block.next()
                continue
            if position.y() > pageBottom :
                break

            txt = block.text()
            tlen = txt.length()

            for i in range(tlen):
                cursor = self.textCursor()
                cursor.setPosition( block.position() + i, QtGui.QTextCursor.MoveAnchor)
                r = self.cursorRect(cursor)

                if txt[i] in [' ','\t']:
                    p1 = qp
                else:
                    continue
#                # draw with pixmaps
#                x = r.x() + 4
#                y = r.y() + fm.height() / 2 - 5
#                p.drawPixmap( x, y, p1 )

                x = r.x() + fm.width("X")
                y = r.y() + fm.height()/2.
                p.drawPoint(x,y)

            block = block.next()

        p.end()
            
    def paintEvent(self, event):

        painter = QtGui.QPainter(self.viewport())

        # CurrentLine background
        if self.highlightCurrentLine:
            r = self.cursorRect()
            r.setX(0) #Sets the left edge of the rectangle to the given coordinate.
            r.setWidth( self.viewport().width() )

            painter.fillRect( r, QtGui.QBrush( self.line_col ) )
            painter.setPen( self.limit_color )
            painter.drawRect( r )

            #painter.setPen( self.limit_color )
            #painter.drawRoundRect ( r )

        # LimitLine
        if self.LimitLine > 0:
            x = ( QtGui.QFontMetrics( self.font() ).width( "X" ) * self.LimitLine ) - self.horizontalScrollBar().value()
            painter.setPen( self.limit_color )
            painter.drawLine( x, painter.window().top(), x, painter.window().bottom() )
        painter.end()

        # Tabs and spaces
        if self.showSpaces :
            self.printWhiteSpaces(event)

        QtGui.QTextEdit.paintEvent(self,event)
      
    def setTabEditorWidth(self,tw):
        self.setTabStopWidth( self.fontMetrics().width( "x" ) * tw ) 
            
    ## SNIPPETS RELATED
    def insertSnippet(self):
        """ Called from whatToDoOnTab's method
        
        Takes the word before the cursor thanks to wordLeftExtend's
        method and tries to find the word in the snippet dictionary
        DICSNIP.
        
        If so, the snippet is added to the stack and expanded, returning True.
        """
        # recupere le curseur et sa position
        tc = self.textCursor()
        p = tc.position()

        # recupere le mot le plus a gauche de celui-ci
        word = self.wordLeftExtend(tc)

        # position de depart du snippet
        # [Si on tape en (0,0) le mot 'link', le curseur
        # est alors en pos (4,0). Il faut alors corriger
        # ceci en enlevant la longeur du raccourci tape.]


        # On essaye de recuperer dans le dico des snippets
        # celui qui correspond au raccourci tape.
        try:
            # le mot est dans le dico
            tpl = DICSNIP[word][1]
            helptpl = DICSNIP[word][0]
            self.snippet = Snippet(unicode(tpl))
            self.snippet.help = helptpl
            self.snippet.start = p - len(word)
            ##
            self.snippets.append(self.snippet)

            self.snippet.fielditer = self.snippet.fieldIter()
            rendu = self.snippet.expanded()
            self.snippet.long=len(rendu)
            
            tc.beginEditBlock()
            
            self.blockSignals(True)
            tc.insertText(rendu)
            self.blockSignals(False)
            
            tc.endEditBlock()

            return True
        except :
            # word is not in DICSNIP
            self.removeSelection()
            return False    

    def whatToDoOnTab(self):
        """ Slot called when 'Tab' is pressed.

           - Tries to expand the word before the cursor;
           
           - if return value is True in insertSnippet's method:
                - the snipped has been added to the stack and is expanded,
                  we then go to the next snippet's field, if any.
             
           - if return value is False in insertSnippet's method:
                - if there are already snippets in stack, pass to the next one.
                - if there are no snippet in stack : stop and insert a tab char.
        """
        
        expanded = self.insertSnippet() # boolean
        #print 'what to do is %s'%expanded
        
        if expanded : # if a snippet has been entered previously
            self.nextField()
        else : # the word entered wasn't a shortcut
            if len(self.snippets) > 0:
                self.nextField()     
            else:
                #self.parent.statusBar().showMessage('insert spaces as no more snippet in stack %s'%(self.snippets)) 
                self.textCursor().insertText(" "*self.tab_long)
                
    def nextField(self):

        try: # to go to next field
            self.field = self.snippet.fielditer.next()
            self.snippet.current_field = self.field
            
            self.field.start = self.snippet.getFieldPos(self.field)
            self.field.long = self.field.getLengh()
            #self.statusBar().showMessage('Field=%s--Snippet=%s--Start=%s--Long=%s'%(self.field.code, self.snippet,self.field.start,self.field.long))
            self.selectFromTo(self.snippet.start + self.field.start, self.field.long)
        
            if self.field.isEnd:
                self.endSnip()
        except :
            #self.textCursor().insertText(" "*self.tab_long)
            pass
            #self.statusBar().showMessage('ds nextField %s %s'%(self.snippet, self.snippet.current_field))
       
        
    def endSnip(self):
        self.removeSelection()
        if len(self.snippets) < 1:
            self.snippets = []
            return

        oldval = self.snippet.expanded()
        self.snippets.pop() # the old snippet
        self.snippet = self.snippets[-1] # new snippet= last entry
        self.field = self.snippet.current_field
        self.updateChilds(given=oldval)
        self.whatToDoOnTab()

    def updateChilds(self, given=None):
        """ Slot called when textarea is modified.
        """
        if len(self.snippets) > 0:
            ## curseur
            c = self.textCursor()
            cursor_pos = c.position()

            ## variables utiles
            # pos de depart du snippet
            debut_snip = self.snippet.start
            old_long = self.snippet.long
            # le champ
            f = self.snippet.current_field
            if f :
                # le nbr d'esclaves
                nslaves = len(f.slaves)
                # la valeur de l'ancien champ (si existence)
                old_field_val = f.content
                # l'ancien champ
                self.oldfield = f
    
                ## Capture le texte du champ actuel
                # l'affiche dans la statusbar
                newpos = c.selectionStart()
                #c.setPosition(debutsnip+st, QtGui.QTextCursor.MoveAnchor)
                c.setPosition(self.field.start + self.snippet.start, QtGui.QTextCursor.MoveAnchor)
                c.setPosition(cursor_pos, QtGui.QTextCursor.KeepAnchor)
                if not given :
                    self.exp = c.selectedText()
                else: 
                    self.exp = given
                #self.statusBar().showMessage("Field %s replaced by '%s'"%(f.code,unicode(self.exp)))
    
                ## Selectionne et remplace le snippet
    
                # update du champ avec la valeur calculee
                f.content = unicode(self.exp)
    
                # nouveau contenu du snippet
                cont = self.snippet.expanded()
    
                # self.snip_long est l'ancienne longueur
                offset = len(f.content) - len(old_field_val)
                self.selectFromTo(self.snippet.start, self.snippet.long+offset)
                #time.sleep(1)
    
                # on update la longueur du snippet
                self.snippet.long = len(cont)
    
                # On doit faire attention a bloquer
                # l'emission du signal
                self.blockSignals(True)
                self.textCursor().insertText(cont)
                self.blockSignals(False)
    
                # Should I prefer this one-liner ?
                #self.selectFromTo(self.start_snip+f.start+len(self.exp), 0)
    
                c = self.textCursor()
                c.setPosition(self.field.start + self.snippet.start+len(self.exp))
                self.setTextCursor(c)
    ## ------------------------------------------
    ## Editor's functions
    ## ------------------------------------------
    # Find the word before the cursor and select it
    def wordLeftExtend(self, my_cursor):
        """ Recupère le mot le plus à gauche
            d'un curseur donné et le sélectionne.
        """
        oldpos = my_cursor.position()

        # manips curseur
        my_cursor.select(QtGui.QTextCursor.WordUnderCursor)
        #self.editor.setTextCursor(my_cursor)

        newpos = my_cursor.selectionStart()

        my_cursor.setPosition(newpos, QtGui.QTextCursor.MoveAnchor)
        my_cursor.setPosition(oldpos, QtGui.QTextCursor.KeepAnchor)
        self.setTextCursor(my_cursor)
        return unicode(my_cursor.selectedText())

    def showCursorPos(self):
        pass
        #tc = self.textCursor()
        #self.statusBar().showMessage( "Position: %s" %(tc.position()) )

    # selectionne le texte de pos à pos + nbr_car
    def selectFromTo(self, pos, nbr_car) :
        """ Selectionne la partie de texte comprise
            entre pos et pos + nbr_car
        """
        #print "Je dois Selectionner de ", pos," a ",lon
        c = self.textCursor()
        # on se positionne au debut
        c.setPosition(pos)
        # on va vers la droite de nbr_car caractères
        c.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor,nbr_car)
        # on repositionne alors le curseur
        self.setTextCursor(c)

    # enleve toute selection
    def removeSelection(self):
        """ Enleve la selection et deplace le
            curseur à la fin de celle-ci.
        """
        p = self.textCursor().position()
        self.selectFromTo(p,0)
        
    def wheelEvent(self, e):
        if e.modifiers() and QtCore.Qt.ControlModifier :
            delta = e.delta()
            if delta > 0:
                self.zoomOut(1)
            elif delta < 0:
                self.zoomIn(1)
            #self.parent.viewport().update()
            return
        QtGui.QAbstractScrollArea.wheelEvent(self,e)
        self.updateMicroFocus()
