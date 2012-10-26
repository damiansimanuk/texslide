Docutils
========

El programa Docutils (http://docutils.sourceforge.net/) es un sistema de
procesamiento de texto escrito en Python, que puede pasar ficheros escritos en
el lenguaje reStructuredText (reST, http://docutils.sourceforge.net/rst.html)
a HTML, LaTeX y más formatos.

¿Por qué reST?
--------------

La gracia de escribir reST en lugar de LaTeX o incluso de utilizar un editor
tipo LyX es que

* Es muy *visual*
* Es **texto plano** (igual que LaTeX o un programa Fortran) así que no hay
  problemas de formatos binarios, incompatibilidades... es igual en todas partes.

Lo anterior es una lista en reST. Fíjate también en la cursiva y en la negrita.
En LaTeX habría que escribir::

  \begin{itemize}

  \item Es muy \emph{visual}
  \item Es \textbf{texto plano} [...]

  \end{itemize}

Conclusión
----------

Si es verdad que se cumple

.. math::

  E = m c^2

entonces no hay más que hablar: es hora de aprender reST. Para generar un
documento a partir de este texto, solamente hay que ejecutar en un
terminal::

  $ rst2html intro_rest.rst intro_rest.html

Y fin de la cuestión. 
