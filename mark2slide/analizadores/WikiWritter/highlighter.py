import re
from PyQt4 import QtCore, QtGui

# Copyright (C) 2008 Christophe Kibleur <kib2@free.fr>
#
# This file is part of WikiParser (http://thewikiblog.appspot.com/).
#

class Highlighter(QtGui.QSyntaxHighlighter):

    def __init__(self, parent):
        QtGui.QSyntaxHighlighter.__init__(self, parent)
        self.rules = []

    def resetRules(self):
        self.rules = []

    def addRule(self, pattern, color, texformats = []):
        if len(texformats) > 0:
            tcf = QTextCharFormat()
            for f in texformats:
                if f == 'bold':
                    kk.append(QFont.Bold)
                if f == 'italic':
                    kk.append(QFont.Italic)

        if isinstance(pattern, tuple):
            pattern = (re.compile(pattern[0]), re.compile(pattern[1]))
        else:
            pattern = (re.compile(pattern), None)

        color = QtGui.QColor(color)

        self.rules.append((pattern, color))

    def modeRest(self):

        self.resetRules()

        # regexps
        bold = r"[*]{2}.*?[*]{2}"
        italic = r"[/]{2}.*?[/]{2}"
        titles = r"(?ms)^([=]+) (.+?)$"
        hrule = r"-{4,}"
        underline = r"(?ms)__(.+?)__"
        stroked = r"(?ms)--(.+?)--"
        exponant = r"(?s)\^{2}(.+?)\^{2}"
        indice = r"(?s)[.]{2}(.+?)[.]{2}"
        url = r"\[(https?:.*?)(?:\|(?P<replacement>.+?))]"
        monospace = r"(?ms)[{]{2}(.+?)[}]{2}"
        image = r"(?ms)\[\[im (?P<url>.+?)\|(?P<align>.+?)\|(?P<alt>.+?)\|(?P<link>.+?)\]\]"
        
        # associated colors
        self.addRule(bold, QtGui.QColor('#003366'))
        self.addRule(italic, QtGui.QColor('#FF0000'))
        self.addRule(titles, QtGui.QColor('#CC3333'))
        self.addRule(hrule, QtGui.QColor('#660033'))
        self.addRule(underline, QtGui.QColor('#666666'))
        self.addRule(stroked, QtGui.QColor('#663300'))
        self.addRule(exponant, QtGui.QColor('#9900CC'))
        self.addRule(indice, QtGui.QColor('#9900CC'))
        self.addRule(url, QtGui.QColor('#3300CC'))
        self.addRule(monospace, QtGui.QColor('#999999'))
        self.addRule(image, QtGui.QColor('#336600'))

    def _spanFindEnd(self, pos, pattern, text):
        while pos < len(text):
            match = pattern.match(text, pos)
            if match is not None:
                self.setCurrentBlockState(-1)
                return match.end()
            pos += 1
        return pos

    def highlightBlock(self, text):
        """We have to overide this method in each
        QtGui.QSyntaxHighlighter subclass. 
        """
        if self.previousBlockState() >= 0:
            self.setCurrentBlockState(self.previousBlockState())
            ((pattern, span), color) = self.rules[self.previousBlockState()]
            pos = self._spanFindEnd(0, span, text)
            self.setFormat(0, pos, color)
            pos += 1
        else:
            pos = 0

        while pos < len(text):

            index = 0
            for ((pattern, span), color) in self.rules:
                match = pattern.match(unicode(text), pos)
                if match is not None:
                    pos = match.end()
                    if span is not None:
                        self.setCurrentBlockState(index)
                        pos = self._spanFindEnd(pos, span, text)

                    self.setFormat(match.start(), pos - match.start(), color)
                    pos -= 1
                    break
                index += 1

            pos += 1