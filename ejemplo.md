Welcome to ReText! S1
=====================


-----

# Presentación con texSlide N1

¡Hola mundo! Como siempre es la presentación de un programa fachero.


.col: 40%

###  Primer columna N2 


ReText is a simple but powerful editor for Markdown and reStructuredText markup
languages. 

ReText is a simple but powerful editor for Markdown and reStructuredText markup
languages. 

.col: 40%

### Segunda N3


ReText is written in Python language and works on Linux and other
ReText is a simple but powerful editor for Markdown and reStructuredText markup
languages. 

.notes: pero por que

ReText is a simple but powerful editor for Markdown and reStructuredText markup
languages. 

.end

ReText is a simple but powerful editor for Markdown and reStructuredText markup
languages. 


-----


## Hola mundo N2

con un texto en nivel 1


-------

##### asdf

ads

f
ff

First code block:

    ::python
    import jinja2
    import markdown

    with open('presentation.html', 'w') as outfile:
        slides_src = markdown.markdown(open('slides.md').read()).split('<hr />\n')

        slides = []

        for slide_src in slides_src:
            header, content = slide_src.split('\n', 1)
            slides.append({'header': header, 'content': content})

        template = jinja2.Template(open('base.html').read())

        outfile.write(template.render({'slides': slides}))
	temp_base = open('template.base.html').read()
	from jinja2 import *
	temp_base2 = '''
	{% for slide in slides %}



			<header trucho>{{ slide.header }}</header>
			<aaa>{{ slide.content }}</aaaa>
			<header>{{ slide.title }}</header>
	{% endfor%}
	'''     

	#~ file:///usr/lib/python2.7/site-packages/landslide-1.0.1-py2.7.egg/landslide/themes/default/js/slides.js
	js1=open("/usr/lib/python2.7/site-packages/landslide-1.0.1-py2.7.egg/landslide/themes/default/js/slides.js",'r').read()
	css_s=open("/usr/lib/python2.7/site-packages/landslide-1.0.1-py2.7.egg/landslide/themes/tango/css/screen.css",'r').read()

	template = Template(temp_base)
	#~ aaa = template.render(slides=['a','b'])
	aaa = template.render(allslides,css={'screen':css_s,'print':'imprimir que ta loco'},js=js1)
	#~ print(aaa)

	salida=open('salida.html','w')
	salida.write(aaa)
	salida.close()



------




hola mundo S2 
-------------


Footnotes[^1] have a label[^label] and a definition[^!DEF].

### perp


yea

[^1]: This is a footnote
[^label]: A footnote on "label"
[^!DEF]: The definition of a footnote.

- Put your markdown content in a file called `slides.md`
- Run `python render.py`
- Enjoy your newly generated `presentation.html`    
	


------


A slide in a subdirectory S3 
=========================

It also works.

An image:

![monkey](monkey.jpg)


	!800x600,r][monkey](monkey.jpg)
	left center right o backround l,c,r,b



-------



Slide #2 S4
========

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean magna tellus,
fermentum nec venenatis nec, dapibus id metus. Phasellus nulla massa, consequat
nec tempor et, elementum viverra est. Duis sed nisl in eros adipiscing tempor

Section #1
----------

Integer in dignissim ipsum. Integer pretium nulla at elit facilisis eu feugiat
velit consectetur.

Section #2
----------

[TOC]

nada de toc...
