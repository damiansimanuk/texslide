--------------------------------------------              -
 Hacer Presentaciones fácilmente (TexSlide)
--------------------------------------------              -

# los títulos:


Titulo del frame # 
=========================                                 = 
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
3. reemplazar escapes

- tabs al principio por 4 espacios


- en los parrafos 




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

||_     Alumos        |
|v3           | Pepe  | 
| Aprobados   | Seba  |
|             | Juan  |

o

|>2     Alumos        |
|v3           | Pepe  | 
| Aprobados   | Seba  |
|             | Juan  |

y otra mas


|>2v3           | 13 |
|      columna  | 23 | 
|       de 3x2  | 33 |
|  41  |   42   | 43 |   

o
      
|>     columna  | 13 | 
|^      de 3x2  | 23 |
|^              |    |
|  41  |   42   | 43 |   


o si nó así la tabla de arriba... esta si me gusta ;)

|      Alumos            <|                          
---------------- ----------     // cada --- es linea de 2px y si es el primer renglón => encabezado a todo
|l Aprobados    |r Pepe   | 	// con la `l` y la `r` le digo que van a la izq. y derecha.					
|^              | Seba    |
|^              | Juan    |
---------------- ----------
|  Desaprobados | José    | 
|^              | Nadia   |
|^              | Alfredo |
---------------- ----------
"Tercer parcial de Alumnos"



   
right left top bottom --> r l t b 

ie: v5rb  // combiana en vertical 5 filas con texto a la derecha y abajo
ie: v5L   // 5 filas combinadas con el texto a 90 grados

__note___________________________________________________________

- Cada celda que empieza con `*` sea `|*` o `|   *` son cabeceras
- Para combinar columnas se puede usar `||` o `|>4` donde 4 es el 
  número de columnas combinadas
- Para combinar filas se usa `|v4` para combinar 4 filas. 
   - Cuando se combinan filas, se unen todos los textos. los 
     espacios se ignoran así: ` {2,}` se convierte en ` ` 
   - los saltos de lineas se ignoran pero se pueden añadir saltos 
     manuales como siempre así: `\\`
- Cada celda se procesa por separado
__________________________________________________________________


# Notas, Ejemplos, Teoremas y más

En el texto anterior se hizo un ejemplo de notas ahora se veran varios:

//  Ejemplo de comentarios
//
//	Yea! este es un buen ejemplo de comentario el que 
//	aparece con la tecla `C` en los slides


 
Y a continuación: 
  
	__note_____________________ Ejemplo de nota _______
	Ejemplo de Notas

	Yea! este es un buen ejemplo de *Nota* Es un bloque
	fachero que aparece en por derecto en los slides 
	___________________________________________________

 
Y ahora un teorema:


__theorem__ Ejemplo de teorema que es lo mismo que las notas

Ejemplo de teorema

Yea! este es un buen ejemplo de *Nota* Es un bloque
fachero que aparece en por derecto en los slides 
___________________________________________________ 



__example__ Ejemplo de ejemplo____________________

Ejemplo de teorema

Yea! este es un buen ejemplo de *Nota* Es un bloque
fachero que aparece en por derecto en los slides 
___________________________________________________ 
	


	
Ni las notas ni los teoremas necesitan una sangria pero se puede usar
y se tiene que respetar porque se borra la misma cantidad si tiene y 
si tiene mas buen que sea lo que Dios quiera... jeje


###30tl###                                 // 30% arriba izq. (t l)

___block__ Cuando el lagarto piedre la cola__________

Ejemplo de Bloque... 

Yea! este es un buen ejemplo de *bloque* Es un bloque
fachero que aparece en por derecto en los slides 
- que contiene listas
- porque se saca el indentado o incluso ni es necesario
  sacar por los siguientes motivos
  - la forma de calcular los items ya soporta
  - los nivels estan dado por los espacios
  - 1 tab = 4 espacios
- yea
____________________________________________________
				

###70tr####                                // 70% arriba der. (t r)
		
___block__ Funcionan las definiciones _______________

Para que funcionen las definiciones es necesario que:

1. que se saquen los indentados
2. solo despues de analizar las listas
3. o calculo como en las listas... mmm eso puede andar
____________________________________________________
	

[logo.png 80x60]
"Logo de TexSlide **(Una masa ¿no?)**."

.###########




	
## Se definen los siguientes bloques:

- nota
- example
- theorem
- definicion
- alert 
- *block* 

jeje *block* es uno especial, o mejor dicho el común, que se usa 
en latex... jeje. ;)





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



# Columnas

para las columnas está buena la forma:

##30##

columna1

##40##

columna2

####   //fin de columnas

funciona con

<div style="vertical-align:middle; padding:10px; margin:10px; display: table-cell; width:30%;">

