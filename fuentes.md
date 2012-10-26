

 * http://vincent.rabah.free.fr/slideshow.html#/4 
 * http://www.it-wars.com/article301/creer-une-presentation-html5-portable-avec-node-js-inliner
 
 
 
Pasos a seguir
==============

## 1. buscar toda la información sobre los js, css3, html5 que pueda servir
 
Están todos en la carpeta Fuentes


 
## 2. información sobre los distintos lenguajes de markup 

Aparentemente no hay un lenguaje de marcas apto para hacer slides (¿es algo relativamente nuevo?: 
talvez si porque con el html5 se facilita un poco la forma de hacer combianar los colores
y con el css3 también se mejora mucho la estética. y sobre el js no tengo idea cuando empezó a 
surgir los efectos y esas cosas, pero en sí lo necesario no son los efectos de movimientos, sino
los  de colores y translucidos)

¿dificil hacer un lenguaje de markup?
- no tanto

## 3. buscar todas las opciones que necesita tener ese nuevo lenguaje (markslide)

## 4. buscar la forma de escribir el html el css y algun js para lograr hacer el markslide

hacer el markslide



* programa zim que puede servir
* trac que está en python y tiene un markup exelente (las tablas, no son tan hinchabolas como las de rst)
* python markup puede servir?

* convierte texto a html (parser) : http://pp.com.mx/python/doc/ejemplos.html

* se pueden sacar muchas utilidades de markdown, como el footnote, el toc, las tablas... 
pero la idea de los headers son distintas porque son slides... tenía pensado la idea así:

	Titulo del slide
	----------------
	subtitulo del mismo slide
	
	texto
	...
	...
	
	
	------
	
las ----- solas con \n antes y despues dicen que son cambio de slide


* para hacer 2 columnas se puede usar la opción de multicolumna en css o
usar dos div..



* Pensando pensando....
parece que lo mejor será usar el qtextedit o qwebkit pero en modo edicion
así se analiza el texto, si se agregó un link ya se edita para que tome... 
como resultado va a quedar muy parecido al writer...

pero la joda es que no se editen las cosas, ya que es el css el que se va 
a mostrar despues... se podría usar un tamño de 800x500 ya para que se vea 
la ubicación de las cosas y luego se compila... mmmm ¡NO! poruqe despues de
compilar cambia el tamaño y la ubicación se pierde... 

mmmm

* un plugin de js para wysiwyg o wysiwym 
https://github.com/wymeditor/wymeditor/blob/master/src/wymeditor/editor/base.js 



### paginas copadas
- Insertar un texto entre otros en el cursor 
	http://stackoverflow.com/questions/7971095/accessing-qtexthtmlimporter-in-pyqt4
	
- http://www.pyside.org/docs/pyside/PySide/QtGui/QTextEdit.html#PySide.QtGui.PySide.QtGui.QTextEdit.textCursor






### decidido para terminar:

1. arreglar el markdown con un template.html
2. arreglar para que la vista Ctr+L sea por defecto y solo el html sin template
3. arreglar para trabajar con imagenes (¿estilo eluniversitario?)
4. ejemplos prácticos en un dock...
5. lo de la columna anda bien pero falta el resaltado de sintaxis, table-cell y el markdown






### Mirada a wiki2beamer sirven algunas ideas y tal vez el código fuente...

- textallion
- wiki2beamer


### slides:

- http://fobos.inf.um.es/R/introknitr/introknitrd.html#24.0



https://stat.ethz.ch/pipermail/r-help-es/2012-May/003917.html


# programas para slides, latex y ...

advi 1.10.2-1 (22)
    Unix-platform DVI previewer and a programmable presenter for slides written in LaTeX.

python-docutils 0.9.1-1 [installed]
    Set of tools for processing plaintext docs into formats such as HTML, XML, or LaTeX
    
beamerthemeprogressbar 0.42-4 (18)
    an alternative theme for latex beamer   
    
brightmare 0.34.2-1 (5)
    A tool that translates LaTeX equations to ASCII/UTF-8 text

cirkuit 0.4.3-1 (38)
    Cirkuit is a KDE4 GUI for the Circuit macros by Dwight Aplevich, for drawing high-quality line diagrams to include in 
    TeX, LaTeX, for similar documents. Cirkuit builds a live preview of the source code and can export the resulting images 
    in EPS, PDF, PNG
    
eqe 1.3.0-2 (15)
    Linux LaTeX equation editor.

gladtex 1.1-1 (1)
    a utility for writing LaTeX equations within HTML

jlatexmath 0.9.7-1 (15)
    Java API to display mathematical formulas written in LaTeX.

laeqed 1.2-1 (11)
    LaTeX equation editor targeted at producing PNG images.

lated 0.1-1 (2)
    A simple LaTeX editor with preview function.

plastex 0.9.2-1 (5)
    Python-based LaTeX document processing framework.

tomboy-latex 0.7-2 (4)
    A tomboy plugin to convert LaTeX math code into inline images and back
























    
    
    
