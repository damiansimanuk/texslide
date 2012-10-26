#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

alltext='''
autor:
date:
# # # # # # # # #
Prmier slide
-------------------------------
Prmier subtítulo del mismo slide que en realida es el prmier subtítulo del mismo slide, el prmier subtítulo como díje antes

a continuación un código:
``` #! python
print("hola mundo")
```

``` #! css
section.middle {
  line-height: 68px;
/*
  text-align: center;
*/
  display: table-cell;
  vertical-align: middle;
  height: 600px;
  width: 900px;
  padding:20px;
}

```


yea

Segundo slide #id3
------------------


Este no tiene subtítulo



A continuación un código trucho:

```
codigo 
trucho
```

Ahora un **principio**  sin fin de bloque de código

```

Y esta es una lista:


------------------------------------


Ups se me dividió el slide

- Esta es una lista  solo termina con un salto de linea  osea un
  renglón vacío.
- Osea que esta debe __ser    otra__ linea del mismo item. Porque si
  escribo en __emcas
con__ la opción fill "auto-fill-mode" me hace el salto  
  automático de lineas 

Debería funcionar lo anterior

Tercer Slide:
...................
Listas combinadas


Ahora una lista combinada ¡tachan!:

1. item 1
  - Hola mundo
     1. y el 1-1
     2. y el 1-2
2. item 2
  - y otro item
3. y ahora el 3


cuarto slide
=================
Las tablas locas:


|   Esta es una          | tabla          | como           |
| 1 columnas             | y dos filas    | yea            |
| Nueva tabla muy simple | sería que sigue acá |  necesita |

dos divisores a menos Esta \| yu 
es una imágen de nada solo \\ sirve para \n probar.Esta es una 
imágen de nada solo sirve para probar.


por ejemplo:

hola | mundo | bien


texto 4 ``para nada`` **yea** o no



Quinto Slide
-----------------
y ahora las imágenes


[logo.png ]"Este es el logo"


Yea mundo.


Esta es una imágen de nada solo sirve para probar.

Todo bien che

-----------------

[openbox.png ]


Notas al pie
---------------------

Y ahora notas **al pie^[id1] ad
será^[2] que** O NO ANDA **anda^[#]** bien^[#] o esta la segunda^[#]

[^id1]: Yea acá está la nota al pie
[^#]: O no es una  nota al pie


Notas al pie
---------------------

Ahora una lista combinada ¡tachan!:

1. item 1
  - Hola mundo
     1. y el 1-1
     2. y el 1-2
2. item 2
  - y otro item
3. y ahora el 3
1. item 1
  - Hola mundo
     1. y el 1-1
     2. y el 1-2
2. item 2
  - y otro item
3. y ahora el 3


Y ahora notas al pie^[id1] ad
será^[2] que anda^[id1] bien^[#] o esta la segunda^[#]

[^id1]: Yea acá está la nota al pie  O no es una  nota al pie digo que si es porque me parece que es... dale dale
[^#]: Primer nota pie automática
[^#]: Segunda

YEA
[id2]: porque este es el pie
yea esta es la ultima linea

hola

'''

DEBUG=True
COLOR_DEBUG=True

MACROS   = {'date' : '%Y%m%d',  'infile': '%f',
            'mtime': '%Y%m%d', 'outfile': '%f'}
            
HEADER_TEMPLATE = {
    'xhtml': """\
<?xml version="1.0"
      encoding="%(ENCODING)s"
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\
 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>%(HEADER1)s</title>
<meta name="generator" content="http://txt2tags.org" />
<link rel="stylesheet" type="text/css" href="%(STYLE)s" />
</head>
<body bgcolor="white" text="black">
<div align="center">
<h1>%(HEADER1)s</h1>
<h2>%(HEADER2)s</h2>
<h3>%(HEADERn3)s</h3>
</div>
""",
    'tex': \
r"""\documentclass{article}
\usepackage{graphicx}
\usepackage{paralist} %% needed for compact lists
\usepackage[normalem]{ulem} %% needed by strike
\usepackage[urlcolor=blue,colorlinks=true]{hyperref}
\usepackage[%(ENCODING)s]{inputenc}  %% char encoding
\usepackage{%(STYLE)s}  %% user defined
n
\title{%(HEADER1)s}
\author{%(HEADER2)s}
\begin{document}
\date{%(HEADER3)s}
\maketitle
\clearpage
"""
}

ALLTAGS = {
    'html': {
        'paragraph'             : '\n<P>%s</P>'      ,
        'list'	       			: '\n<UL>%s</UL>'    ,
        'numlist'               : '\n<OL>%s</OL>'    ,
        'item'                  : '\n<LI>%s</LI>'    ,

        'table'                 :'\n<TABLE>%s\n</TABLE>',
        'tableRow'              :'\n<TR>%s</TR>',
        'tableCell'             :'<TD>%s</TD>',

        'img'                   : '\n<IMG %s SRC="%s" alt="%s" />',
        'figure'                : '\n<div class="%s">%s \n</div>',
        'caption'               : '\n<P><B>Fig:</B> %s</P>',

        'fnote'                 :
        '<sup class="footnote"><a href="#fn%(id)s">%(id)s</a></sup>',
        
        'title1'                : '<H1>%s</H1>'       ,
        'title2'                : '<H2>%s</H2>'    ,
        'title3'                : '<H3>%s</H3>'    ,
        'title4'                : '<H4>%s</H4>'  ,
        'title5'                : '<H5>%s</H5>'   ,
        'blockQuote'            : '<BLOCKQUOTE>%s</BLOCKQUOTE>'   ,
        'fontMono'              : '<CODE>%s</CODE>'         ,
        'blockVerb'             : '<PRE>%s</PRE>'         ,
        
        
        'anchor'                : '<A NAME="\a"></A>\n',
        
        'fontBold'              : '<B>\\1</B>',
        'fontItalic'            : '<I>\\1</I>',
        'fontUnderline'         : '<U>\\1</U>',
        'fontStrike'            : '<S>\\1</S>',
        'fontMono'              : '<CODE>\\1</CODE>',

        
        'deflist'                  : '<DL>%s</DL>'          ,
        'deflistItem'             : '<DT>%s</DT>'          ,
        'deflistItem2'             : '<DD>'           ,
        'bar1'                     : '<HR NOSHADE SIZE=1>'        ,
        'bar2'                     : '<HR NOSHADE SIZE=5>'        ,
        
        'url'                  : '<A HREF="%s">%s</A>'        ,
        'urlMark'              : '<A HREF="%s">%s</A>'        ,
        'email'                : '<A HREF="mailto:%s">%s</A>' ,
        'emailMark'            : '<A HREF="mailto:%s">%s</A>' ,
        
        'prueba':
        ['hola',1],
        
        'tableOpen'            : '<TABLE~A~~B~ CELLPADDING="4">',
        'tableClose'           : '</TABLE>'       ,

        'tableRowOpen'         : '<TR>'           ,
        'tableRowClose'        : '</TR>'          ,
        'tableCellOpen'        : '<TD~A~~S~>'     ,
        'tableCellClose'       : '</TD>'          ,
        'tableTitleCellOpen'   : '<TH~S~>'        ,
        'tableTitleCellClose'  : '</TH>'          ,
        '_tableBorder'         : ' BORDER="1"'    ,
        '_tableAlignCenter'    : ' ALIGN="center"',
        '_tableCellAlignRight' : ' ALIGN="right"' ,
        '_tableCellAlignCenter': ' ALIGN="center"',
        '_tableCellColSpan'    : ' COLSPAN="\a"'  ,
        'cssOpen'              : '<STYLE TYPE="text/css">',
        'cssClose'             : '</STYLE>'       ,
        'comment'              : '<!-- %s -->'    ,
        'EOD'                  : '</BODY></HTML>'
    },
    'tex': {
        'title1'               : '~A~\section*{\a}'     ,
        'title2'               : '~A~\\subsection*{\a}'   ,
        'title3'               : '~A~\\subsubsection*{\a}',
        # title 4/5: DIRTY: para+BF+\\+\n
        'title4'               : '~A~\\paragraph{}\\textbf{\a}\\\\\n',
        'title5'               : '~A~\\paragraph{}\\textbf{\a}\\\\\n',
        'numtitle1'            : '\n~A~\section{\a}'      ,
        'numtitle2'            : '~A~\\subsection{\a}'    ,
        'numtitle3'            : '~A~\\subsubsection{\a}' ,
        'anchor'               : '\\hypertarget{\a}{}\n'  ,
        'blockVerbOpen'        : '\\begin{verbatim}'   ,
        'blockVerbClose'       : '\\end{verbatim}'     ,
        'blockQuoteOpen'       : '\\begin{quotation}'  ,
        'blockQuoteClose'      : '\\end{quotation}'    ,
        'fontMonoOpen'         : '\\texttt{'           ,
        'fontMonoClose'        : '}'                   ,
        'fontBoldOpen'         : '\\textbf{'           ,
        'fontBoldClose'        : '}'                   ,
        'fontItalicOpen'       : '\\textit{'           ,
        'fontItalicClose'      : '}'                   ,
        'fontUnderlineOpen'    : '\\underline{'        ,
        'fontUnderlineClose'   : '}'                   ,
        'fontStrikeOpen'       : '\\sout{'             ,
        'fontStrikeClose'      : '}'                   ,
        'listOpen'             : '\\begin{itemize}'    ,
        'listClose'            : '\\end{itemize}'      ,
        'listOpenCompact'      : '\\begin{compactitem}',
        'listCloseCompact'     : '\\end{compactitem}'  ,
        'listItemOpen'         : '\\item '             ,
        'numlistOpen'          : '\\begin{enumerate}'  ,
        'numlistClose'         : '\\end{enumerate}'    ,
        'numlistOpenCompact'   : '\\begin{compactenum}',
        'numlistCloseCompact'  : '\\end{compactenum}'  ,
        'numlistItemOpen'      : '\\item '             ,
        'deflistOpen'          : '\\begin{description}',
        'deflistClose'         : '\\end{description}'  ,
        'deflistOpenCompact'   : '\\begin{compactdesc}',
        'deflistCloseCompact'  : '\\end{compactdesc}'  ,
        'deflistItem1Open'     : '\\item['             ,
        'deflistItem1Close'    : ']'                   ,
        'bar1'                 : '\\hrulefill{}'       ,
        'bar2'                 : '\\rule{\linewidth}{1mm}',
        'url'                  : '\\htmladdnormallink{\a}{\a}',
        'urlMark'              : '\\htmladdnormallink{\a}{\a}',
        'email'                : '\\htmladdnormallink{\a}{mailto:\a}',
        'emailMark'            : '\\htmladdnormallink{\a}{mailto:\a}',
        'img'                  : '\\includegraphics{\a}',
        'tableOpen'            : '\\begin{center}\\begin{tabular}{|~C~|}',
        'tableClose'           : '\\end{tabular}\\end{center}',
        'tableRowOpen'         : '\\hline ' ,
        'tableRowClose'        : ' \\\\'    ,
        'tableCellSep'         : ' & '      ,
        '_tableColAlignLeft'   : 'l'        ,
        '_tableColAlignRight'  : 'r'        ,
        '_tableColAlignCenter' : 'c'        ,
        '_tableCellAlignLeft'  : 'l'        ,
        '_tableCellAlignRight' : 'r'        ,
        '_tableCellAlignCenter': 'c'        ,
        '_tableCellColSpan'    : '\a'       ,
        '_tableCellMulticolOpen'  : '\\multicolumn{\a}{|~C~|}{',
        '_tableCellMulticolClose' : '}',
        'tableColAlignSep'     : '|'        ,
        'comment'              : '% \a'     ,
        'TOC'                  : '\\tableofcontents',
        'pageBreak'            : '\\clearpage',
        'EOD'                  : '\\end{document}'
    }
}    

def Debug(msg,id_=0):
    if not DEBUG: return
    if int(id_) not in range(10): id_ = 0
    # 0:black 1:red 2:green 3:yellow 4:blue 5:pink 6:cyan 7:white ;1:light
    #~ ids            = ['INI','CFG','SRC','BLK','HLD','GUI','OUT','DET','NAD','Import']
    #~ colors_bgdark  = ['7;1','1;1','3;1','6;1','4;1','5;1','2;1','7;1']
    colors_bglight = ['7'  ,'1'  ,'3'  ,'6'  ,'4'  ,'5'  ,'2'  ,'2;1','7;1','1;1']
    if COLOR_DEBUG:
        color = colors_bglight[id_]
        msg = '\033[3%sm%s\033[m'%(color,msg)
    print("--- %s"%(msg))


def getRegexes():
    """
    Retorna las expreciones regulares compiladas para las marcas de
    texslide 
    """
    bank = {
        'lineVoid':
        re.compile(r'^\s*$'),
        'title':
        re.compile(r'^(\w.+)$'),
        # la \w es para que no empieze con ` que corresponden a ```
        # de códigos multilinea (hay que mejorar)
        'titleRule':
        re.compile(r'^\s*([.=-]{4,})\s*$'),
        'titleSub':
        re.compile(r'^\s*(.+)$'),

        'blockVerbOpen':
        re.compile(r'^```\s*((#!)\s*(\w*))*\s*$'),
        'blockVerbClose':
        re.compile(r'^```\s*$'),
        'blockQuoteOpen':
        re.compile(r'^"""\s*(.*)$'),
        'blockQuoteClose':
        re.compile(r'^"""\s*$'),
        'blockQuote2Open':
        re.compile(r"^'''\s*(.*)$"),
        'blockQuote2Close':
        re.compile(r"^'''\s*$"),       
        

        'listOpen':
        re.compile(r'^( *|\t*)- (.*)$'),
        'listClose':
        re.compile(r'^ *$'),
        
        'numlistOpen':
        re.compile(r'^( *|\t*)(\d)[.] (.+)$'),
        'numlistClose':
        re.compile(r'^ *$'),

        'tableOpen':
        re.compile(r'\|.*[^\\]\|'),
        'tableClose':
        re.compile(r'^ *$'),
        

#         'table': # ¿esto vá (se usa))?
        # re.compile(r'\|.*[^\\]\|'),
        
        # imagenes
        'imageOpen':
        re.compile(\
r'\[([\w_,.+%$#@!?+~/-]+\.(png|jpe?g|gif|eps|bmp))( +.*)?\] ?(".*)?'),
        'imageClose':
        re.compile(r'.*'),

        # footnotes [id] \\ [^id]: ejemplo de nota al pie
        'ids':
        re.compile(r'^\[(\^?(?:#?|\w+))\]:(.+)'),
        'footnote':
        re.compile(r'\^\[(\w+|#)\]',re.S|re.U),
        
        
        'blockCommentClose':
        re.compile(r'^%%%\s*$'),
        'quote':
        re.compile(r'^\t+'),
        '1lineVerb':
        re.compile(r'^``` (?=.)'),
        '1lineRaw':
        re.compile(r'^""" (?=.)'),
        '1lineTagged':
        re.compile(r"^''' (?=.)"),
        
        'Comment':
        re.compile(r'\s+//(.*)$'),
        
                
        # mono, bold, italic, underline:
        'fontMono':
        re.compile(  r'``([^\s](|.*?[^\s])`*)``',re.S|re.U),
        'tagged':
        re.compile(  r"''([^\s](|.*?[^\s])'*)''",re.S|re.U),
        'fontBold':
        re.compile(r'\*\*([^\s](|.*?[^\s])\**)\*\*',re.S|re.U),
        'fontItalic':
        re.compile(  r'//([^\s](|.*?[^\s])/*)//',re.S|re.U),
        'fontUnderline':
        re.compile(  r'__([^\s].+\s*.*[^\s])__'),
        'fontStrike':
        re.compile(  r'--([^\s](|.*?[^\s])-*)--'),

        'raw':
        re.compile(  r'""([^\s](|.*?[^\s])"*)""'),
        'list':
        re.compile(r'^( *)(-) (?=[^ ])'),
    'numlist':
        re.compile(r'^( *)(\+) (?=[^ ])'),
    'deflist':
        re.compile(r'^( *)(:) (.*)$'),
    'listclose':
        re.compile(r'^( *)([-+:])\s*$'),
    'bar':
        re.compile(r'^(\s*)([_=-]{20,})\s*$'),
#    'table':
#        re.compile(r'^ *\|\|? '),
    'blankline':
        re.compile(r'^\s*$'),
    'comment':
        re.compile(r'^%'),
        
    'indent':
        re.compile(r'^( {3,})(.*)$'),
    
    # Auxiliary tag regexes
    '_imgAlign'        : re.compile(r'~A~', re.I),
    '_tableAlign'      : re.compile(r'~A~', re.I),
    '_anchor'          : re.compile(r'~A~', re.I),
    '_tableBorder'     : re.compile(r'~B~', re.I),
    '_tableColAlign'   : re.compile(r'~C~', re.I),
    '_tableCellColSpan': re.compile(r'~S~', re.I),
    '_tableCellAlign'  : re.compile(r'~A~', re.I),
    }
    
    # Special char to place data on TAGs contents  (\a == bell)
    bank['x'] = re.compile('\a')
    
    # %%macroname [ (formatting) ]
    bank['macros'] = re.compile(r'%%%%(?P<name>%s)\b(\((?P<fmt>.*?)\))?' % (
        '|'.join(MACROS.keys())), re.I)
    
    # %%TOC special macro for TOC positioning
    bank['toc'] = re.compile(r'^ *%%toc\s*$', re.I)
    
    # Almost complicated title regexes ;)
    titskel = r'^ *(?P<id>%s)(?P<txt>%s)\1(\[(?P<label>[\w-]*)\])?\s*$'
    
    ### Complicated regexes begin here ;)
    #
    # Textual descriptions on --help's style: [...] is optional, | is OR
    
    
    ### First, some auxiliary variables
    #
    
    # [image.EXT]
    patt_img = r'\[([\w_,.+%$#@!?+~/-]+\.(png|jpe?g|gif|eps|bmp))\]'
    
    # Link things
    # http://www.gbiv.com/protocols/uri/rfc/rfc3986.html
    # pchar: A-Za-z._~- / %FF / !$&'()*+,;= / :@
    # Recomended order: scheme://user:pass@domain/path?query=foo#anchor
    # Also works      : scheme://user:pass@domain/path#anchor?query=foo
    # TODO form: !'():
    urlskel = {
        'proto' : r'(https?|ftp|news|telnet|gopher|wais)://',
        'guess' : r'(www[23]?|ftp)\.',         # w/out proto, try to guess
        'login' : r'A-Za-z0-9_.-',             # for ftp://login@domain.com
        'pass'  : r'[^ @]*',                   # for ftp://login:pass@dom.com
        'chars' : r'A-Za-z0-9%._/~:,=$@&+-',   # %20(space), :80(port), D&D
        'anchor': r'A-Za-z0-9%._-',            # %nn(encoded)
        'form'  : r'A-Za-z0-9/%&=+:;.,$@*_-',  # .,@*_-(as is)
        'punct' : r'.,;:!?'
    }
    
    # username [ :password ] @
    patt_url_login = r'([%s]+(:%s)?@)?'%(urlskel['login'],urlskel['pass'])
    
    # [ http:// ] [ username:password@ ] domain.com [ / ]
    #     [ #anchor | ?form=data ]
    retxt_url = r'\b(%s%s|%s)[%s]+\b/*(\?[%s]+)?(#[%s]*)?'%(
        urlskel['proto'],patt_url_login, urlskel['guess'],
        urlskel['chars'],urlskel['form'],urlskel['anchor'])
    
    # filename | [ filename ] #anchor
    retxt_url_local = r'[%s]+|[%s]*(#[%s]*)'%(
        urlskel['chars'],urlskel['chars'],urlskel['anchor'])
    
    # user@domain [ ?form=data ]
    patt_email = r'\b[%s]+@([A-Za-z0-9_-]+\.)+[A-Za-z]{2,4}\b(\?[%s]+)?'%(
        urlskel['login'],urlskel['form'])
    
    # Saving for future use
    bank['_urlskel'] = urlskel
    
    ### And now the real regexes
    #
    
    bank['email'] = re.compile(patt_email,re.I)
    
    # email | url
    bank['link'] = re.compile(r'%s|%s'%(retxt_url,patt_email), re.I)
    
    # \[ label | imagetag    url | email | filename \]
    bank['linkmark'] = re.compile(
        r'\[(?P<label>%s|[^]]+) (?P<link>%s|%s|%s)\]'%(
            patt_img, retxt_url, patt_email, retxt_url_local),
        re.L+re.I)
    
    # Image
    bank['img'] = re.compile(patt_img, re.L+re.I)
    
    # Special things
    bank['special'] = re.compile(r'^%!\s*')
    return bank
### END OF regex nightmares






# def header2():
#     """
#     Procesa la cabecera para determinar ciertas 
#     configuraciones útiles
#     """
#     print("Hay cabecera")
    
    

CONFIG = {
    'target'    : 'html',                        # default
    'title'     : 'Slide hecho con TexSlide',     # default
    'author'    : 'TexSlide',                     # default
    'email'        : 'github.texslide.org',         # ¿direccion de github?
    'Licencia'     : 'GPL V3',
}


# # # Definicion de los bloques
BLOCKS = {
    """ BLOCKS contiene los distintos bloques y los bloques internos
    que se  permiten en TexSlide
    """
    'para'      :['comment','raw','tagged'],
    'verb'      :[],
    'table'     :['comment'],
    'raw'       :[],
    'tagged'    :[],
    'comment'   :[],
    'quote'     :['quote','comment','raw','tagged'], # 'bar'
    'list'      :['list','numlist','deflist','para','verb','comment',\
                  'raw','tagged'],
    'numlist'   :['list','numlist'],
    'deflist'   :['list','numlist','deflist','para','verb','comment',\
                  'raw','tagged'],
    'bar'       :[],
    'title'     :[],
    'numtitle'  :[],
}
EXCLUSIVE = ['comment','verb','raw','tagged']

ORDEN_BLOCKS=['blockVerb','list','numlist','table','image']

# # # END definicion de bloques    
     
CONFIG['target']='html'




        

class ConvertFunction():
    def __init__(self):
        global CONFIG,ALLTAGS,BLOCKS

        self.b_list     = BLOCKS["list"]
        self.b_numlist  = BLOCKS["numlist"]
        self.b_list     = BLOCKS["list"]
        self.regex      = getRegexes()
        self.lang       = None
        self.target     = CONFIG['target']
        self.tags       = ALLTAGS[self.target]
        """
        Se analizan los distintos bloques y devuelve el valor para
        saber a que linea saltar. Generalmente se devuelve > 1, por
        ejemplo para `code` multilinea.
        Se devuelve 0 en realidad no es un bloque como se suponía que
        era                             '
        """
        self.func={
            'blockVerb' :self.codeVerb,
            'list'      :self.list,
            'numlist'   :self.numlist,
            'table'     :self.table,
            'image'     :self.image,
            'funcion1'  :self.funcion1,
        }
            
        
    def reset(self):
        pass

    def funcion1(self,lines):
        Debug("funcion1: ",1)
        Debug(lines,0)
        return 0, ''

    def image(self,lines):
        Debug(":IMAGE: ",1)
        Debug(lines,0)
        find = self.regex['imageOpen'].search(lines[0])
        arg=find.group(3)
        cap=find.group(4)
        src=find.group(1)
        # alignh='center'
        # if re.search(r'[ ,]r[ ,]',arg):
        #     alignh='right'
        # elif re.search(r'[ ,]l[ ,]',arg):
        #     alignh='left'

        alh= 'right' if re.search(r'[ ,]r( |,|$)',arg) else 'left' if\
             re.search(r'[ ,]l( |,|$)',arg) else 'center'

        alv= 'top' if re.search(r'[ ,]t( |,|$)',arg) else 'booton' if\
             re.search(r'[ ,]b( |,|$)',arg) else 'center'

        size=re.search(r'[ ,](\d+(px|%))( |,|$)',arg)
        if size:
            size=size.group(1)
        else:
            size=''

        index=0
        caption=''
        if cap:
            c=re.match(r'^"(.*)"',cap)
            if c:
                caption=c.group(1)
            elif lines[1]:
                c=re.match(r'(.*)"( |$)',lines[1])
                if c:
                    caption=cap[1:] +'\n'+ c.group(1)
                    index=1
                    
        elif lines[1]:
            c=re.match(r'^ ?"(.*)"( |$)',lines[1])
            if c:
                caption=c.group(1)
                index=1
            
        # para implementar lo siguiente es necesario trabajar un poco
        # con los css y las variables anterires alh alv y en cuanto
        # a el size hay que obtener ancho y alto.
        clas='image' 
        arg=''
        res=self.tags['img']%(arg,src,caption)
        if caption:
            caption=self.newPara([caption],False)
            caption = self.tags['caption']%(caption)
        res=self.tags['figure']%(clas,res + caption)

        print(res)
           
        return index, res


    def table(self,lines):
        Debug(":tableOpen: ",1)
        Debug(lines,0)
                       
        line_a = lines[0]
        rows = [line_a.strip().strip('\\').strip('|').split('|')]
        # print(rows)

        i=-1
        for line in lines[1:]:
            i+=1
            find = self.regex['tableOpen'].search(line)
            if not find:
                lines = lines[:i] 
                Debug(":tabla: trunca .......................",0)
                break

            # Si line_a (fila anterior ) termina en \\ y extiende la
            # fila con la siguiente linea o si no agrega una nueva
            # fila  
            if line_a.strip().endswith('\\'):                
                rows[-1].extend(line.strip().strip('\\').strip('|').\
                               split('|'))
            else:
                rows.append(line.strip().strip('\\').strip('|').\
                               split('|'))
            line_a = line

        # ahora ya se tiene la tabla correcta en rows se pueden
        # analizar los espacios para saber como estan centrados los
        # textos pero no se hace eso todavía...
        table =''
        for ro in rows:
            cells='' 
            for cel in ro:
                # Debug(":table:cel:|%s|"%cel,3)
                cell = self.newPara([cel],False)
                cells += self.tags['tableCell']%(cell)
            table += self.tags['tableRow']%(cells)
        table = self.tags['table']%(table)
        Debug(table,2)
                
            # Debug(' | '.join(row),4)
                
        # Debug(rows,3)

        return i, table
        
   
    def list(self,lines):        
        # Debug(":list: ingresa ",2)
        ## yas 
        find = self.regex['listOpen'].search(lines[0])
        nivel = len(find.group(1))
        curItem=[find.group(2)]
        items=''
        tempIndex=0
        for line in lines[1:-1]:
            find = self.regex['listOpen'].search(line)
            if find:
                nnivel = len(find.group(1))
                if nnivel < nivel:
                    tempIndex -=1 
                    break
                    #~ return tempIndex, items
                elif nnivel == nivel:
                    items += self.tags['item']%\
                        (self.parser(curItem,self.b_numlist))
                    curItem=[find.group(2)]
                    #~ j+=1
                else:
                    curItem.append(line)
            else:
                curItem.append(line)
            tempIndex +=1 
            
        items += self.tags['item']%\
                 (self.parser(curItem,self.b_numlist))
        
        items = self.tags['list']%(items)
        # Debug(":lista: retorna",6)        
        # Debug(items,8)        
        return tempIndex, items

    def numlist(self,lines):        
        # Debug(":numlist: ingresa ",2)
        find = self.regex['numlistOpen'].search(lines[0])
        nivel = len(find.group(1))
        curItem=[find.group(3)]
        # Debug(":numlist: %s -- %s"%(nivel,curItem),3)
        items=''
        tempIndex=0
        for line in lines[1:-1]:
            find = self.regex['numlistOpen'].search(line)
            if find:
                nnivel = len(find.group(1))
                if nnivel < nivel:
                    tempIndex -=1 
                    break
                    #~ return tempIndex, items
                elif nnivel == nivel:
                    items += self.tags['item']%\
                             (self.parser(curItem,self.b_numlist))
                    curItem=[find.group(3)]
                    #~ j+=1
                else:
                    curItem.append(line)
            else:
                curItem.append(line)
            tempIndex +=1 
            
        items += self.tags['item']%\
                 (self.parser(curItem,self.b_numlist))
        
        items = self.tags['numlist']%(items)
        # Debug(":numlist: retorna",6)        
        # Debug(items,8)        
        return tempIndex, items

    def codeVerb(self,lines):
        Debug(":codeVerb: ingresa ",2)
        index=len(lines)    
        if self.target == 'html':
            return index-1, self.highlighting(lines)
        else:
            return index, ''
            
    def highlighting(self,code):
        """
        returns : A string of html code.
        
        ¿damian: debería andar para html y no html?        
        """
        #~ Debug(code[0],4)
        reg=re.compile(r'^```\s*((#!)\s*(\w*))*\s*$')
        res=reg.search(code[0])
        code.pop(0)
        if res:
            lang=res.group(3)    
            Debug(':Code: lang: %s'%lang,9)
        else:
            lang=None
        code='\n'.join(code).strip('\n').strip('`').strip('\n')
        try:
            from pygments import highlight
            from pygments.lexers import get_lexer_by_name,TextLexer
            from pygments.formatters import HtmlFormatter
            pygments = True
        except ImportError:
            pygments = False
            Debug('H: La librería pygments no está disponible:\
                  ImportError',9)

        if pygments:
            try:
                lexer = get_lexer_by_name(lang)
            except ValueError:
                lexer = TextLexer()
            
            formatter = HtmlFormatter()
            codeh=highlight(code, lexer, formatter)
            # Debug(codeh,5)
            return codeh
        else:
            # damian: aca se deberia hacer general (¿para latex?)
            txt = code.replace('&', '&amp;')
            txt = txt.replace('<', '&lt;')
            txt = txt.replace('>', '&gt;')
            txt = txt.replace('"', '&quot;')
            return txt

        
    
    def parser(self,lines,block_orden):
        lines.append('')
        ultimalinea = len(lines)
        lineref = 0
        body_parser=[]
        joinLines=[]
        result=''
        voidLine=True
                
        while lineref < ultimalinea:
            
            line = lines[lineref]
            #Debug(':parser: linea:',1)
            #Debug(line,0)
            lineref += 1
            
            
            analise=re.search(r'^~~\w~~(.*)',line,re.DOTALL|re.UNICODE)
            if analise:
                Debug(':parser: ------ linea analizada ------',2)
                newblock=True
                result=analise.group(1)
            # acá en adelante se podría hacer todo con if si se complican los
            # análisis de los bloques.
            else:
                newblock=False
                for block in block_orden:
                    # block contiene en orden los bloques a busacar, así
                    # primero se busca un bloque de código despues uno de
                    # xxx y por último un xxx

                    if self.regex[block+'Open'].search(line):
                        Debug(":parser: abre %s"%block,5)
                        aux_body=[line]
                        for j in range(lineref,ultimalinea):
                            aux_line= lines[j]
                            aux_body.append(aux_line)
                            if self.regex[block+'Close'].search(aux_line):
                                index,result = self.func[block](aux_body)
                                if index >= 0:
                                    lineref = lineref + index
                                    newblock=True
                                Debug(":parser: cierra %s"%block,6)
                                break
                                
                    elif newblock:
                        break
                    else:
                        pass
                    
            if newblock:
                # Si hay un nuevo bloque primero agrega el parrafo
                # pendiente luego incorpora el nuevo bloque 
                body_parser.append(self.newPara(joinLines))
                body_parser.append(result)
                joinLines=[]
            elif re.search(r'^\s*$',line):
                # Si no hay nuevo bloque pero hay salto de linea,
                # osea una linea vacia => hay un nuevo parrafo
                body_parser.append(self.newPara(joinLines))
                joinLines=[]
            else:
                # Concatena las lineas
                joinLines.append(line)

        return('\n'.join(body_parser))
        
    def newPara(self,joinLines,para=True):
        """
        Recibe una lista (un parrafo) y analiza sus partes.
        Para los enlaces y notas al pie es necesario detectar
        los #id (eso lo hace convert)
        ## USO:
        >>> ts=mark2slide.ConvertFunction()
        >>> text="hola __mundo__ como //estas//"
        >>> ts.newPara([text])
        '\n<P>hola <U>mundo</U> como <I>estas</I></P>'
        """
                
        if not joinLines:
            return ('')
        line = '\n'.join(joinLines)
        # Debug(line,0)

        for block in ['Mono', 'Bold', 'Italic', 'Underline','Strike']:
            subst=self.tags['font'+block]
            line = self.regex['font'+block].sub(subst,line)

        line=self.regex['footnote'].sub(self.fNotes,line)
        
        Debug(line,0)
        
        if para:
            line = self.tags['paragraph']%line
        return(line)

    def fNotes(self,match):
        _id=match.group(1)
        Debug(":fNotes: %s"%_id,2)
        x=self.addFootNote(_id)
        if x ==0:
            Debug("            YEA",8)
            print("------- No encontró nota para %s"%(match.group(0)))
            return("")
        y=self.tags['fnote']%{'id':x}
        return(y)

    def addFootNote(self,_id):
        if _id not in self.footnotes.keys():
            Debug("            YEA",8)
            return 0
        if _id =='#':
            x=self.cfna
            if x == len(self.footnotes[_id]):
                return 0
            self.Slides[-1]['footer']['footnote'].\
                append(self.footnotes[_id][self.cfna])
            self.cfna +=1
            self.cfn +=1
            x=self.cfn

        elif self.footnotes[_id][1]==0:
            self.cfn +=1
            x=self.footnotes[_id][1]=self.cfn
            print(self.footnotes[_id])
            self.Slides[-1]['footer']['footnote'].\
            append(self.footnotes[_id][0])
        else:
            x=self.footnotes[_id][1]
        return x

        
    def addSection(self,section):
        # mirá vos...
        """
        analiza las lineas a incorporar en el Slide o nada  
        """
        if not self.Slides:
            if section: 
              print("Cuidado: Texto perdido")
              print(section)
            return

        # antes de añadir al slide se pude llamar a parser()
        res=self.parser(section,ORDEN_BLOCKS)
        # Debug(":addSection:",7)
        # Debug(res,7)
        self.Slides[-1]['section']=res
        self.Slides[-1]['footer']['page']=self.n_slides
        # Debug(self.Slides[-1]['section'],8)
        return

    def newSlide(self,lineref):
        """
        Analiza si hay un nuevo Slide.

        Recibe el número de linea de referencia en self.bodylines y
        retorna el nuevo número de lineas.

        Retorna 0 si no es un encabezado, 2 si es un título y no tiene
        subtítulo ó 3 si tiene subtítulo.

        Pero ¡OJO! también modifica el miembro self.Slides
        """
        npre= self.regex['lineVoid'].search(self.bodylines[lineref-1]) 
        npos1=self.regex['lineVoid'].search(self.bodylines[lineref+1])
        npos2=self.regex['lineVoid'].search(self.bodylines[lineref+2]) 
        npos3=self.regex['lineVoid'].search(self.bodylines[lineref+3])
        rule=self.regex['titleRule'].search(self.bodylines[lineref]) 

        indexReturn = 0
        if npre and rule and npos1:
            indexReturn = 1

            self.addSection(self.section)
            self.section=[]
            
            self.Slides.append({
                'header':{'title':'','nivel':'h4','subti':''},
                'section':'',
                'footer':{'footnote':[],'page':0 },
                'notes':'',
            })

        elif npre and (npos2 or npos3):
            findH = self.regex['title'].\
                    search(self.bodylines[lineref])
            findR = self.regex['titleRule'].\
                    search(self.bodylines[lineref+1])
            
            if findR and findH:
                
                temp = findR.group(1)
                nivel = '1' if '=' in temp else '2' if '-'\
                             in temp else '3'
                findSubT = self.regex['title'].\
                           search(self.bodylines[lineref+2])
                title = self.tags['title'+nivel]%(findH.group(1))
                subti=''
                if findSubT :
                    subti=self.newPara([findSubT.group(1)])
                    indexReturn=3
                else:
                    indexReturn=2

                self.addSection(self.section)
                # reset variables x slides
                self.section=[]
                self.footnotes=dict()
                self.footnotes['#']=[]
                self.links=dict()
                self.cfn=0
                self.cfna=0
                
                # Debug(title,7)
                # Debug(nivel,6)
                # Debug(subti,4)

                self.Slides.append({
                    'header':{'title':title,'nivel':nivel,'subti':subti},
                    'section':'',
                    'footer':{'footnote':[],'page':0 },
                    'notes':'',
                })
                    
        return(indexReturn)
                        
    def convert(self,body):
        """
        Este método analiza el body recibido, que es directamente
        el *.ts y lo separa en distintos slides, analizando los
        códigos verbatin. Llama a parser() para que analice los
        distintos slides.         
        """
        
        # normaliza el texto
        body = body.replace('\u0002', "").replace('\u0003', "")
        body = body.replace("\n\r", "\n").replace("\r\n", "\n").\
               replace("\r", "\n")
        body = re.sub(r'\n(\s*\n)+', '\n\n', body)

        # separa la cabecera del contenido. La cabecera está al
        # principio del texto y separada por `####` ó `# # # #`
        find_heder = re.search(r'(.*)\n(# |#){4,}\n(.*)',\
                               body,re.DOTALL|re.UNICODE)        
        if find_heder:
            self.header = find_heder.group(1)
            self.body  = find_heder.group(3)
            Debug("Hay cabecera",4)
        else:
            self.body=body
            self.header=''

        self.bodylines = self.body.split("\n")
        self.bodylines.insert(0,"\n")
        self.bodylines.append("\n")
        self.bodylines.append("\n")
                
        Debug(":convert: body ",4)
        Debug(body,0)
        
        self.Slides=[]
        self.toc=[]
        self.n_slides=0
        lines = self.bodylines
        ultimalinea = len(lines)-4 #ver va -2
        
        body_parser=[]
        joinLines=[]
        result=''
        voidLine=True
        ## Este bucle se usa para preprocesar el texto.
        # - separan los slides,
        # - analizan los bloques de código
        # - escapes
        # - remplazar saltos de lineas y uniones de lineas `\\`
        # - buscar [id]: http://.... y ^[id]: nota al pie 
        
        self.section=[]
        lineref = 0
        while lineref < ultimalinea:
            lineref += 1
            newblock=False

            # busca título para separar los slides
            newI  = self.newSlide(lineref)
            if newI > 0:
                lineref = lineref + newI
                self.section=[]
                self.n_slides +=1
                
            line = lines[lineref]

            # Debug(':convert: linea:',1)
            # Debug(line,0)
            
            # ahora se fija si es un bloque de código porque puede
            # contener códigos ¡semejantes a títulos!
            if self.regex['blockVerbOpen'].search(line):
                Debug(":convert: abre code ",5)
                aux_body = [line]
                for j in range(lineref+1,ultimalinea):
                    aux_line= lines[j]
                    aux_body.append(aux_line)
                    if self.regex['blockVerbClose'].search(aux_line):
                        index,result = self.codeVerb(aux_body)
                        if index > 0:
                            lineref = lineref + index
                            newblock=True
                        Debug(":convert: cierra code ",5)
                        break

            # analiza (preprocesa) los ids para footnote and links
            if self.regex['ids'].search(line):
                Debug(":convert: abre ids ",9)
                aux_body = [line]
                for j in range(lineref+1,ultimalinea):
                    aux_line= lines[j]
                    aux_body.append(aux_line)
                    if self.regex['lineVoid'].search(aux_line):
                        index,result = self.Ids(aux_body)
                        if index >= 0:
                            lineref = lineref + index
                            newblock=True
                        Debug(":convert: cierra ids ",5)
                        break
                      
            if newblock:
                self.section.append("~~C~~"+result)
            else:                
                self.section.append(line)
            # END WHILE

        self.addSection(self.section)
        self.n_slides # es el número total de slides ahora

        # llamar a posProces()
        # self.posProces()
        
        # for slide in self.Slides:
        #     Debug(slide['header']['title'],4)
        #     if slide['header']['subti']:
        #         Debug(slide['header']['subti'],5)

        #     Debug(slide['section'],3)
        #     Debug(slide['footer']['page'],3)

        # print(self.n_slides)
                
        return({'slides':self.Slides,\
                'title':"No tiene título todavía",\
                'pages':self.n_slides,\
                'toc':self.toc,
            })
        
    def Ids(self,lines):
        Debug(":footnote: %s"%lines,1)
        index=len(lines)
        append=''
        for line in reversed(lines):
            find = self.regex['ids'].search(line)
            if find:
                _id=find.group(1)
                idd=re.search(r'^\^(.*)',_id)
                if idd:
                    _id=idd.group(1)
                    _footnote=find.group(2)+append
                    if _id =='#':
                        self.footnotes[_id].insert(0,_footnote)
                    else:
                        self.footnotes[_id] = [_footnote,0]
                    Debug(self.footnotes,4)
                else:
                    _links=find.group(2)+append
                    self.links[_id] = _links
                append=''
            else: # concatena con la linea anterior
                append = ' '+ line + append
            
        Debug("-----Links",1)
        Debug(self.links,0)
        
        Debug("-----Footnotes",1)
        Debug(self.footnotes,0)
        
        return(index-2,'')        
            
          
def convert(body):
    global CONFIG, ORDEN_BLOCKS, regex
    # target = CONFIG['target']
    # result = []
    # source = []
    # f_lastwasblank = 0
    
    
    inst = ConvertFunction()
    
    a=inst.convert(body)

    # for slide in a['slides']:
    #     Debug(slide['header']['title'],4)
    #     if slide['header']['subti']:
    #         Debug(slide['header']['subti'],5)
            
    #     Debug(slide['section'],3)
    #     print(slide['footer']['page'],'/',a['pages'])

    try:
        from jinja2 import Template
    except:
        use_jj = False
        print("W: jinja2 es necesario para procesar el template")
    else:
        use_jj = True
        template_base = open('google2/template.html').read()

    js1=css_s=''

    template = Template(template_base)
    aaa = template.render(
        a,
        css={
            'screen':"Nada de screen",
            'print':'imprimir que ta loco',
            },
        js="sin js",
        )
  
    # damian: la siguiente prueba ayuda...
    #~ js1=open("/usr/lib/python2.7/site-packages/landslide-1.0.1-py2.7.egg/landslide/themes/default/js/slides.js",'r').read()
    #css_s=open("css/plana.css",'r').read()
    #aaa = template.render(allslides,css={'screen':css_s,'print':'imprimir que ta loco'},js=js1)


    salida=open('google2/salida.html','w')
    salida.write(aaa)
    salida.close()
    # print(aaa)

    
if __name__ == "__main__":
    convert(alltext)

    """asdf"""

    '''asdf'''


#~ for i in range(10):
    #~ Debug("hola mundo %s"%i,i)
# Debug("En el convert se tiene",0)
