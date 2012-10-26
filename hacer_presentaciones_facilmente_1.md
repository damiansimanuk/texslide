# Hacer Presentaciones fácilmente 1
 
En este articulo dedicaré un poco a sobre un pequeño proyecto que estoy pensando hacer. Esta presentación tiene **varios** objetivos iguales de importantes:

- Contarles sobre las distintas formas actuales, existentes, conocidas y no conocidas de hacer presentaciones de forma fácil
- Contarles sobre los distintos lenguajes de marcado como ser:
    - txt2tag
    - Markdown
    - Textile
    - ReStructuredText

- Alguna comparación de Beamer con los slides html5
- Y pedir ayudas y consejos para tener en cuenta a la hora de realizar un editor wisywing wisywim para


## Presentaciones increíbles:

Para realizar presentaciones profesionales es nesesario usar mucho talento y trabajo o una buena herramienta. Usas Beamer, después de leer los manuales y las infinidades de articulos en todos los idiomas se logrará una presentación con esta característica: ¡increíble! pero notarás que de tanto compilar (F6, F6 y F6 en texstudio) y con el tiempo que tarda compilando, ¡como que cansa! Usando beamer en si, no es que hayan muchos problemas, pero le veo como lleva tiempo, y es justamente ahí donde estoy buscando una alternativa.

### Alternativas a Beamer

Después de leer la sección anterior se entiende que hay una ventaja muy difícil de superar de beamer que es LaTex y un problema a salvar que es compilar. 

Buscando alternativas observé que existen distintos slides hechos en html5 ¡Wow! y con css3 ¡Wow!. Algunos ejemplos les dejo a continuación:

- http://code.google.com/p/html5slides/
- https://github.com/imakewebthings/deck.js
- http://www.sitepoint.com/5-free-html5-presentation-systems/
- https://github.com/bartaz/impress.js
- http://zoomzum.com/6-best-html5css3-presentation-frameworks/ 

Con toda mi búsqueda, veo lo siguiente, hay muchas fórmas de realizar slides con html5, js y css3 pro ejemplo, con una calidad muy buena. Donde calidad digo por los efectos, posibilidad de poner lo que se de la gana en donde se de la gana. También es muy fácil agregar y quitar contenidos dinamicamente, ya que son script que se ejecutan. 


## Primera conclusión

Me detendré un poco acá para decir lo siguiente:

"Es posible hacer presentaciones con calidad semejante a beamer aunque una esté enfocada en un visor web y otra esté enfocada en pdf, al fin y al cabo esto no sería problema ya que practicamente cualquier máquina tiene ambos visores, aunque eso sí las no tan modernas no contarán con las características css3 ni html5."


## Todo muy lindo pero...

¡Claro! pero si comparamos escribir en latex o en html, ¡prefiero latex! y ahí es donde viene la cuestión ¿como escribir estas presentaciones? 

Hay varios lenguajes de marcado como ser Markdown, ReStructuredText, txt2tag, Wiki,etc. que permiten escribir textos planos y con pequeñas marcas indican si es un título, subtítulo, cita, etc. Así como markdown, existen varios y con características muy similares, **pero** no están diseñados para hacer estas presentaciones por los siguientes motivos indispensables para mi gusto (en comparación con beamer):

- Escribir (hacer) bloques como en beamer 
- dos columnas (para poner una figura en una y textos en la otra, o dos figuras)
- y muchas otras pequeñas cosas más.

Podrán decir que no tiene el paquete tal o el tal (como tikz)! es que yo, en particular, para varias cosas como dibujos y diagramas prefiero dia e inkscape.


En fin, veo que los distintos lenguajes de marcado son muy buenos para hacer wikis, tutoriles, pequeños y grandes manuales, y tienen mucha potencia a pesar de sus no mas de 20 marcas, e incluso permiten ver el contenido desde cualquier visor de texto, y entender y modificar fácilmente desde el mismo. 


**¡No están totalemente diseñados para hacer presentaciones! **

# ¿cuál es el plan?

Y aquí es donde todo se pone mas interesante... El plan es el siguiente:

### Desarrollar/modificar un lenguaje de marcado 

Desarrollar un lenguaje de marcado mucho mas extendido que markdown, el cual permita de forma fácil hacer las columnas, insertar boloques, etc. 

Una idea por ejemplo es la siguiente y muy simple:

	Titulo del frame #
	----------------------
	subtítulo del mismo frame (vease beamer para entender la idea)
	
	Para que tome como subtítulo debe estar justo en el siguiente
	renglón despues de las lineas del subrayado, lo cu

  

Para hacer las columnas podría ser algo como:	


	Titulo del frame #
	-----------------------------------------
	subtítulo del mismo frame 
    

	texto antes de las doble columnas	

	texto en primer columna    |  texto en la segunda columna
	texto aquí también         |  bla bla
	                           |
	                           |  pero es difícil de escribir 
	y más texto                |  o modificar y no está diciendo nada
	                           |  del ancho de las columnas


	texto después de las doble columnas


Hu.... y me olvidaba de un problema muy importante... las imágenes, si se usa por ejemplo rst se pude elegir el tamaño pero faltaría elegir la posición en el slide, y en markdown y en general no tienen forma de setear el tamaño de las imágenes.


### Crear un editor Wysiwym/wysiwyg

Esta es una idea para futuro mucho mas trabajada, la idea sería que el editor tenga posibilidad de editar el slide, al estilo impress o el powerpoint con la característica que se guarda en html, con su correspondiente javascript y css.

La parte de wysiwyg es bastante importante para editar formulas, por supuesto, no me he olvidado de eso. Las formulas pueden ser integradas mediante mathjax.


### ¡Por lo menos un editor de código!

Si tienen un tiempo vean **ReText** es un editor de rst o md que permite visualizar en vivo el contenido que se está escribiendo

En base a este editor se pueden hacer muchas modificaciones y trabajar con script como **landslide** se pueden lograr varias mejoras, y sobre todo hacer de forma fácil presentaciones.

Yo me quiero inclinar, en principio por este lado, trabajar con un lenguaje de marcado para presentaciones, ya tiene un nombre y todo (**texslide**) y un editor para esto. 

El resultado (osea lo portable sería un directorio que contiene un archivo *index.html* y un directorio *files* en el cual se tendrán las figuras, css y js correspondientes)


*Me gustaría (**descaradamente**)  pedirles sus consejos para seguir con este pequeño proyecto!*




###### ####### ######## ####### ###### ####### ####### #######

# la cabecera

movido para abajo \/


# los títulos:


Titulo del frame #
=========================
subtítulo del mismo frame 


Titulo del frame #
-------------------------
subtítulo del mismo frame 


Titulo del frame #
.........................
subtítulo del mismo frame 


Para que tome como subtítulo debe estar justo en el siguiente
renglón despues de las lineas del subrayado. y aparecerá como en beamer.


# los bloques y columnas:

..col:40%

bla bal

..col:50%

bla bal

..end



## en vez de:

..block:
	..block: Título del bloque

	..end
..end

## me gusta mas la siguiente forma:


	# título del bloque
	
	sigue en el bloque
	sigue y sigue
	
	hasta que desaparezca el indentado
	
	
## y para los códiogos solo uso el ~~~  


texto después de las doble columnas

las citas van como en python: con las triples ''' o """ y el primer 
renglón o el último es el autor así:

	''' chapulín colorado

	mas vale ultimo hombre en pie que una casa rodante

	'''

o 

	'''

	mas vale ultimo hombre en pie que una casa rodante

	''' chapulín colorado


# Notas:

..note: esta es una nota hasta 
        que haya doble salto de linea

  
# Comentarios:

con // se comenta por lineas como en C/C++

# listas:

- item
- item
   1. <2>item interno 
   2. <1>item numerado con overlay
- item

# overlays:

los overlays se hacen con `<1,2,5>`, `<x-y>`, `<x->` o `<-y>` donde x 
es el inicio e y el final se puede poner en principio de cualquier 
cosa...

<2> este parrafo está en el nivel 2 de overlay

	# <1> // o con títulos de bloque:  # <1> Título del bloque
	
	Este bloque en uno
	
	yea, enjoin!
	
y ya está!


# que procesar primero:

1. códigos multi linea
2. slides
3. 




# ejemplo:

Titulo del frame #
--------------------------
subtítulo del mismo frame 

texto antes de las doble columnas	

..col:50%
	
	# título del bloque
	
	sigue en el bloque
	sigue y sigue
	
	hasta que desaparezca el indentado

..col:50%

	# título del bloque
	
	sigue en el bloque
	sigue y sigue
	
	hasta que desaparezca el indentado
	
..end

texto después de las doble columnas

'''
mas vale ultimo hombre en pie que una casa rodante
''' chapulín colorado



| Esta es una | tabla
| con dos columnas | y dos filas

y se puede escribir asi


| Esta es una       | tabla       |
-----------------------------------
| con dos columnas  | y dos filas |
| en realidad con 3 | y 2 filas   |



## método de programación:

- leo por lineas
- luego analizo si es encabezado o código....
- incorporo a self.Slide[]

Si agrego un escape estilo ~~A~~ al inicio sé que esa linea (que en
realidad puede ser varias ya concatenadas (code y títulos) puedo
saltear esas lineas)

--------------------
hola mundo
---------
yea yea


nada
--------------------

resultaría:

Slide[0]['h']    == <h1> hola mundo</h1> <p> yea yea</p> 
Slide[0]['b'][0] == []
Slide[0]['b'][1] == ["nada"]
Slide[0]['f']    == []



# Sobre las cabeceras:

me gustaría que se elijan:

..author: sima 
          alfredo
          alguien mas
          
..date:   hoy

..title:  Como usar texslide

..logo:   logo.png [XXX]   	// donde XXX son las posiciones absolutas del 
							// css: top,right,left,bottom  =44%  por ejemplo

..piedepagina: %title -- %date | %author |  %np/%nps   //  El %np/%nps van por defecto... 

// con las barras se separa así:  izquierda | centro | derecha

..makeindex: yes

..maketitle: yes // creo que esto no conviene
                 // ¿y conviene hacer una caratula siempre?

// tableofcontents   // no se si vá para que funcione con la t o...


:El tema:
	theme: default, moon, black   // entonces agrega esos tres temas (como el template de google)

:pie:
	foot: -- \title -- 

// termina con un barra de # 


# # # # # # # # # # # # # 


# Tablas

... Ejemplo de Tablas
| tabla 11 | tabla 12 |
| tabla 21 | tabla 22 |


## Otra:


|_ Alumnos |_ Notas |
| Alfredo  |      7 |
| Hugo     |      6 | 
... Notas de los vagos

## Otra:

||*     Alumos        |
|v3           | Pepe  | 
| Aprobados   | Seba  |
|             | Juan  |

  
   
right left top bottom --> r l t b 

ie: v5rb  // combiana en vertical 5 filas con texto a la derecha y abajo
ie: v5L   // 5 filas combinadas con el texto a 90 grados

..notas:--------------------------------------------------------
- Cada celda que empieza con `*` sea `|*` o `|   *` son cabeceras
- Para combinar columnas se puede usar `||` o `|>4` donde 4 es el número 
  de columnas combinadas
- Para combinar filas se usa `|v4` para combinar 4 filas. 
   - Cuando se combinan filas, se unen todos los textos. los espacios se 
     ignoran así: ` {2,}` se convierte en ` ` 
   - los saltos de lineas se ignoran pero se pueden añadir saltos 
     manuales como siempre así: `\\`
- Cada celda se procesa por separado
 ------------------------------------------------------------------

# Notas, Ejemplos, Teoremas y mas

En el texto anterior se hizo un ejemplo de notas ahora se veran varios:

//  Ejemplo de comentarios
//
//	Yea! este es un buen ejemplo de comentario el que 
//	aparece con la tecla `C` en los slides


 
Y a continuación: 

	__NOTA__ Ejemplo de nota __________________________
	Ejemplo de Notas

	Yea! este es un buen ejemplo de *Nota* Es un bloque
	fachero que aparece en por derecto en los slides 
	___________________________________________________

 
Y ahora un teorema:


__TEOREMA__ Ejemplo de teorema que es lo mismo que las notas

Ejemplo de teorema

Yea! este es un buen ejemplo de *Nota* Es un bloque
fachero que aparece en por derecto en los slides 
___________________________________________________ 


Ni las notas ni los teoremas necesitan una sangria pero se puede usar
y se tiene que respetar porque se borra la misma cantidad si tiene y 
si tiene mas buen que sea lo que Dios quiera... jeje


# Listas de definiciones

:Hola:
  Saludo copado
  
  lo que dice la gente
  
:Chau:
  Saludo de despedida
  
  cuando uno se va
  
Ups!... que complicado...
 
## Las listas empiezan y terminan:

- cada definición está entre os `:Definicion:` y cada definición
  está debajo con una indentación de a menos `2 espacios` OJO 
- La lista continua si encuentra otra definicion
- Termina cuando no encuntra otra definicion ni parrafo indentado


# 





 
