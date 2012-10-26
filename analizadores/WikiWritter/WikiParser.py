#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################################################################
# Module:    WikiParser.py
# Author:    C.Kibleur
# Date:      2008/27/07
# Modified : 2008/11/10
# Version:   Draft 0.6
#######################################################################

'''
WikiParser is a project to parse my own wiki-text like language,
because :
    - reStructuredText is too heavy for a 
      litlle app inside Google App Engine;
    - Markdown does not satisfies me because it's only HTML;
    - Textile is indeed very limited;
'''
# 0.6 CHANGES
# - Added the LaTeX handler, but it does not render images yet
# (uses urllib to retrieve images from Internet).



# TODO
# - better approach for paragraph handling;
# - maths : what to choose ? A lot of choices, but no one seems *really* fun.
# - a LaTeX handler;

#######################################################################
# Imports
#######################################################################
# First class imports
import codecs
import string
import re
import cgi
from urllib import urlretrieve

from docs_templates import *
# Third party Imports
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter, LatexFormatter
    HAVE_PYGMENTS = True
except:
    HAVE_PYGMENTS = False

# Import Psyco if available to gain speed
try:
    import psyco
    psyco.full()
except ImportError:
    pass

#######################################################################
#   Constants
#######################################################################
# This will be usefull to separate paragraphs
# Note the optionnal \r for Windows users.
NEWLINE = re.compile(r"(\r?\n){2}") 

#######################################################################
#   Classes
#######################################################################

# ========================================================= HANDLERS
class Tex_handler(object):
    """A special format handler  
    """
    def __init__(self,parent, full=False):
        self.parent = parent
        self.para_start = "\par\n"
        self.para_end = ""
        self.formatter = LatexFormatter(linenos=False)
        
        self.doc_start = tex_doc_start
        self.doc_end = tex_doc_end
        self.extension = "tex"
              
    def _title_repl(self, matched):
        level = len(matched.group('level'))
        # handling of the table of contents
        self.parent.toc.append((matched.group("title"), level))
        
        def get_section(level):
            if level == 1 : return "\\section*{"
            elif level == 2 : return "\\subsection*{"
            else : return "\\subsection*{"
        
        
        return '%s%s%s'%(get_section(level),matched.group("title"),"}")
        
    def _bold_repl(self, matched):
        return r'\\textbf{%s}'%matched.group(1)
        
    def _hrule_repl(self, matched):
        return "\\hrule\n"
        
    def _italic_repl(self, matched):
        return r"\\textit{%s}"%matched.group("italics")

    def _underline_repl(self, matched):
        #return '<span style="text-decoration: underline;">%s</span>'%matched.group(1)
        return r'\\underline{%s}'%matched.group(1)
        
    def _stroked_repl(self, matched):
        return r'\\sout{%s}'%matched.group(1)
        
    def _exponant_repl(self, matched):
        return '_{%s}' %matched.group(1)
        
    def _indice_repl(self, matched):
        return '^{%s}' %matched.group(1)
        
    def _monospace_repl(self, matched):
        return r'\\begin{verbatim}%s\\end{verbatim}' %matched.group(1)
        
    def _math_repl(self, matched):
        return r'$%s$'%matched.group(2)

    def _url_repl(self, matched):
        s = matched.group(1)
        try :
            rep = matched.group("replacement")
        except:
            rep = s
        return r'\\href{%s}{%s}'% (cgi.escape(s),rep)
        
    def _image_repl(self, matched):
        """[[im url|link|align|alt]]"""
        url   = matched.group(1)
        link  = matched.group(2)
        align = matched.group(3) or "center"
        alt   = matched.group(4) or "alt text here"
        
        name = url.split('/')[-1]
        if url.startswith('http'):
            
            urlretrieve(url, name)
            
        return r'%%\\includegraphics{../%s}'%(name)
        
    def _image_repl2(self, matched):
        """[[im url|link|align|alt]]"""
        url   = matched.group(1)
        link  = matched.group(2)
        align = matched.group(3) or "center"
        alt   = matched.group(4) or "alt text here"
        
        name = url.split('/')[-1]
        if url.startswith('http'):
            
            urlretrieve(url, name)
        #return r'\\includegraphics{%s}'%(url)
        return r'%%\\includegraphics{../%s}'%(name)

  
    def _lists_repl(self, matched):
        """
        Lists are constructed like this :
            
        [list] (or [list=1] for numbered ones, or [list=a] for enumerated ones)
        - blabla
        - bla
        [/list]"""
        # check the list type (normal, numeric, alphabetic)
        listype = matched.group('listype')
        
        if listype is None :
            truc_s = 'itemize'
            truc_e = truc_s
        else :
            listype = listype.replace('=','').replace(' ','')
            
        if listype == '1':
            truc_s = 'enumerate'
            truc_e = truc_s
            
        elif listype == 'a' :
            truc_s = 'itemize'
            truc_e = 'itemize'
            
        sortie = [r'\\begin{%s}'%truc_s,]
        
        for el in matched.group('contents').split('- ') :
            if el not in ("",'\r\n','\n') :
                sortie.append('\\item %s'%el.strip())
        sortie.append(r'\\end{%s}'%truc_e)
        
        return '\n'.join(sortie)
        
    def _newline_repl(self, matched):
        """Force a new line character.
        """
        return r"\\newline"
        
    def _quote_repl(self, matched):
        s = matched.group(1)
        return r"\\begin{quote}%s\\end{quote}"%cgi.escape(s)


class Html_handler(object):
    """A special format handler  
    """
    def __init__(self,parent, tpl = 'out_html.tpl'):
        self.parent = parent
        self.para_start = "<p>"
        self.para_end = "</p>"
        self.formatter = HtmlFormatter(linenos=False)
        
        self.doc_start = html_doc_start
        self.doc_end = html_doc_end
        self.extension = "html"
        
    def _title_repl(self, matched):
        level = len(matched.group('level'))
        # handling of the table of contents
        self.parent.toc.append((matched.group("title"), level))
        return '<h%s>%s</h%s>'%(level,matched.group("title"),level)
        
    def _bold_repl(self, matched):
        return '<strong>%s</strong>'%matched.group(1)
        
    def _hrule_repl(self, matched):
        return "<hr/>"
        
    def _italic_repl(self, matched):
        return "<em>%s</em>"%matched.group("italics")

    def _underline_repl(self, matched):
        #return '<span style="text-decoration: underline;">%s</span>'%matched.group(1)
        return '<u>%s</u>'%matched.group(1)
        
    def _stroked_repl(self, matched):
        return '<del>%s</del>'%matched.group(1)
        
    def _exponant_repl(self, matched):
        return '<sup>%s</sup>' %matched.group(1)
        
    def _indice_repl(self, matched):
        return '<sub>%s</sub>' %matched.group(1)
        
    def _monospace_repl(self, matched):
        return r'<tt>%s</tt>' %matched.group(1)
        
    def _math_repl(self, matched):
        return r'<img alt="tex:%s"/>'%matched.group(2)

    def _url_repl(self, matched):
        s = matched.group(1)
        try :
            rep = matched.group("replacement")
        except:
            rep = s
        return '<a href="%s">%s</a>' % (cgi.escape(s),rep)
        
    def _image_repl(self, matched):
        """[[im url|link|align|alt]]"""
        url   = matched.group(1)
        link  = matched.group(2) or url
        align = matched.group(3) or "center"
        alt   = matched.group(4) or "an image here"
        return r'<div class="%s"><a href="%s"><img src="%s" alt="%s"></a></div>'%(align, link, url, alt)
  
    def _lists_repl(self, matched):
        """[list] or [list=1] or [list=a]
        - blabla
        - bla
        [/list]"""
        # check the list type (normal, numeric, alphabetic)
        listype = matched.group('listype')
        
        if listype is None :
            truc_s = 'ul'
            truc_e = truc_s
        else :
            listype = listype.replace('=','').replace(' ','')
            
        if listype == '1':
            truc_s = 'ol'
            truc_e = truc_s
            
        elif listype == 'a' :
            truc_s = 'ol style="list-style-type: lower-alpha"'
            truc_e = 'ol'
        sortie = ['<%s>'%truc_s,]
        
        for el in matched.group('contents').split('- ') :
            if el not in ("",'\r\n','\n') :
                sortie.append('<li>%s</li>'%el.strip())
        sortie.append('</%s>'%truc_e)
        
        return '\n'.join(sortie)
        
    def _newline_repl(self, matched):
        """Force a new line character.
        """
        return "<br />"
        
    def _quote_repl(self, matched):
        s = matched.group(1)
        return "<blockquote>%s</blockquote>"%cgi.escape(s)
 
# ========================================================= PARSER       
class Parser(object):
    """There must be several passes in the parsing process, as it is
       not so direct :
    
    1. Remove text parts that shouldn't be parsed like 
       [[nowiki]]...[[/nowiki]] and {{{code}}} and
       replace them with placeholders @@NOWIKI_TYPE_NUMBER@@ 
       as they must not be treated by the inline parser.
    
    2. Decompose into paragraphs.
    
    3. Each paragraph is then given to a specific handler :
       HTML, LaTeX, Lout, XML, etc.
    
    4. replace all placeholders with their initial values.
    
    5. The code blocks are then processed with Pygments 
    
    """
    # just a shortcut for convenience
    rec = re.compile
    
    sperules = (
        ('echap'  , rec(r'\\(.)'), "normal"),
        ('nowiki', rec(r'''(?ms)(?:\[\[nowiki\]\](.+?)\[\[/nowiki\]\])'''), 'normal'),
        ('code', rec(r'''(?ms)([{]{3} *?(?:(?P<language>\w+)?)(?:\r?\n)+(?P<code>.+?)[}]{3})'''), "code"),
        ('inline', rec(r'''(?ms)[{]{2}(.+?)[}]{2}'''), "normal")
        )

    # These rules define inline replacement of entities
    RULES =[
    ('title', rec(r"""(?ms)^(?P<level>[=]+) (?P<title>.+?)$""") ),
    ('hrule', rec(r'(-{4,})') ),
    ('bold', rec(r'(?:\*\*)(?P<bold>.+?)(?:\*\*)', re.M|re.S) ),
    ('italic', rec(r'(?<!http:)(?<!https:)//(?P<italics>.+?)//', re.M|re.S) ),
    ('underline', rec(r'__(?P<underline>.+?)__', re.M|re.S) ),
    ('stroked', rec(r'--(.+?)--', re.M|re.S) ),
    ('exponant', rec(r'\^{2}(.+?)\^{2}'  , re.S) ),
    ('indice', rec(r'[.]{2}(.+?)[.]{2}', re.S) ),
    ('url', rec(r'\[(https?:.*?)(?:\|(?P<replacement>.+?))]') ),
    ('monospace', rec(r'[{]{2}(.+?)[}]{2}', re.M|re.S) ),
    ('math', rec(r'([$])(.+?)\1', re.M|re.S) ),
    ('image', rec(r"\[\[im (?P<url>.+?)\|(?P<align>.+?)\|(?P<alt>.+?)\|(?P<link>.+?)\]\]", re.M|re.S) ),
    ('lists', rec(r'(?ms)\[list(?P<listype>\=\w+)?\](?:\r?\n)(?P<contents>.*?)\[/list\]')),
    ('newline', rec(r'(?m)[/]$')),
    ('quote', rec(r"(?ms)\[''(.*?)''\]")),
    ]
    
    def __init__(self, raw, handler, external_rules = []):
        self.debraw = raw
        self.raw = [p for p in raw.split('\n\n') if p !=""]
        self.handler = handler
        self.handler.parent = self

        # External rules
        self.ext_rule = external_rules
        
        # Tbale of contents
        self.toc = []
        
    def add_handler(self, handler):
        self.handler = handler
        
    def process(self, full=False):
       
        # Replace all sourcecode and nowiki by placeholders 
        no_wiki = self.replace_no_wiki()
        
        # Assemble in paragraphs
        sortie = []
        for para in [p for p in NEWLINE.split(no_wiki) if p not in ("","\n","\r\n")]:
            if para.startswith('- ') or para.startswith('=') or para.startswith('[list]'):
                sortie.append("%s"%para)
            else:
                # sortie.append("<p>%s</p>"%para)
                sortie.append("%s%s%s"%(self.handler.para_start, para, self.handler.para_end))

        paras = "\n".join(sortie)
        
        # Now, replace inline contents
        now = self.inline(paras)
        
        # Reset all nowiki and code placeholders
        out = self.reset_no_wiki(now)
        
        return out
                
    # ============================================== Special Rules
    def callb_normal(self,match):
        return '%s' % (match.group(1))
          
    def callb_code(self,match):
        try:
            lang = match.group('language').lower()
        except:
            lang = 'text'
        return (lang,match.group('code'))
                   
    def replace_no_wiki(self):
        test = '\n'.join(self.raw)
        self.res = {}
        for name,rule,callb in self.sperules :
            
            for match in rule.finditer(test):
                id = "@@%s_%s@@"%(name, len(self.res))
                test = rule.sub(id, test, 1)
                
                # callbacks
                method = getattr(self, "callb_" + callb, None)
                if callable(method):
                    rest = method(match)       
        
                self.res[id] = rest
                
        return test
        
    def reset_no_wiki(self,texte):

        for k,v in self.res.items():
            if isinstance(v, tuple):
                lang, code = v[0], v[1]
                lexer = get_lexer_by_name(lang, stripall=True)
                formatter = self.handler.formatter
                result = highlight(code, lexer, formatter) #.encode('utf-8')    
                texte = texte.replace( k , result, 1)
            else:
                texte = texte.replace(k,v)
        return texte
          
    # ============================================== Inline parsing
    
    def callback(self, prefix, m):
        """This callback function is used by the parser's inline method
        to call the parser's handler replace methods.
        """
        method = getattr(self.handler, "_" + prefix + "_repl", None)
        if callable(method):
            return method(m)
        
    def inline(self, rawtext):
        """Given rawtext, replace all the inline elements
        by their substitutes.
        """
        for rule_name, rule_reg in self.RULES :
            for mo in rule_reg.finditer(rawtext):
                rawtext = rule_reg.sub( self.callback( rule_name, mo), 
                                        rawtext, 1)
        return rawtext
    
    # ============================================== PLUGINS
    def _registerHandlerPlugin(self, plugrule, plugmethod):
        """You can add syntax rules dynamically within the parser.
        
        Given a syntax rule and a function, add the rule to 
        the RULES tuple. 
        """
        rule_name, rule_reg = plugrule[0], plugrule[1]
        self.RULES.append(plugrule)
        new_handler_method_name = "_"+rule_name+"_repl"
        if not hasattr(self.handler, new_handler_method_name):
            setattr(self.handler, new_handler_method_name, plugmethod) 
        
#######################################################################
#   Main
#######################################################################
def parse_text(source):
    handler = Html_handler(None)
    parser = Parser(source, handler)
    return parser.process()
    
def launch(source, full=False, tex=False):
    if tex:
        handler = Tex_handler(None)
    else:
        handler = Html_handler(None)
    parser = Parser(source, handler)
    
    p = parser.process()
    if full :
        ds = parser.handler.doc_start
        de = parser.handler.doc_end
        ext = parser.handler.extension
        
        f = codecs.open('test_result.%s'%ext,'w', 'utf-8')
        f.write(ds)
        f.write(p)
        f.write(de)
        f.close()
    
    return p
   
def main():
    test = """= title level 1 

== title level 2

=== title level 3

A simple paragraph on one line.

Another paragraph taking 2 lines
inside an editor but is not rendered like this in HTML.

This paragraph taking 2 lines too, but I've added a linebreak at the end of the first line/
so that it renders differently.

Of course, you can write **funny** //paragraphs//, like this __silly__ one/
I can escape the wiki syntax like [[nowiki]]**this**[[/nowiki]]

Now, let's look some source code :

{{{python
print "toto"
for i in range(2,31,3):
    print "i is equal to %s"%i
}}}

== Lists

**normal lists :**

[list]
- first
- second
- third with //some// markup **text** __inside__
[/list]

**numbered lists:**

[list=1]
- first element
- second/
with nothing here.
- third with //some// markup **text** __inside__
[/list]

**alphabetical lists :**

[list=a]
- first element
- second/
with nothing here.
- third with //some// markup **text** __inside__
[/list]

== Images:

An image here : [[im http://forum.mathematex.net/styles/prosilver/imageset/site_logo.gif|http://forum.mathematex.net/styles/prosilver/imageset/site_logo.gif|center|du texte la]]

== Links :

They render like the following one : [https://addons.mozilla.org/en-US/firefox/addon/128|BBCode extension for FireFox]

== Quotes

You can [''quote someone
like this''] simple no ?!
"""

  
    
    #print launch(test,1,1)
    print parse_text(test)


if __name__ == "__main__":
    main()