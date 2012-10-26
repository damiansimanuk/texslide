#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ==============================================================================
# LaTeX document template
# ==============================================================================
tex_doc_start = r"""\documentclass[a4,12pt]{article}
\usepackage{ucs}
\usepackage[utf8]{inputenc}
\usepackage[frenchb]{babel}
\usepackage{fancyhdr}
\usepackage[pdftex]{graphicx} % Pour l'insertion d'images
\DeclareGraphicsExtensions{.jpg,.mps,.pdf,.png} % Formats d'images
\usepackage{fancyvrb}
\usepackage{color}
\usepackage[pdftex]{thumbpdf}      % Vignettes
\usepackage[pdftex,                %
    bookmarks         = true,%     % Signets
    bookmarksnumbered = true,%     % Signets numérotés
    pdfpagemode       = None,%     % Signets/vignettes fermé à l'ouverture
    pdfstartview      = FitH,%     % La page prend toute la largeur
    pdfpagelayout     = SinglePage,% Vue par page
    colorlinks        = true,%     % Liens en couleur
    urlcolor          = magenta,%  % Couleur des liens externes
    pdfborder         = {0 0 0}%   % Style de bordure : ici, pas de bordure
    ]{hyperref}%                   % Utilisation de HyperTeX


\usepackage{ifpdf}
\ifx\pdftexversion\undefined %if using TeX
  \usepackage{graphicx}
\else %if using PDFTeX
  \usepackage[pdftex]{graphicx}
\fi
\ifpdf %if using PDFTeX in PDF mode
  \DeclareGraphicsExtensions{.pdf,.png,.mps}
  %\usepackage{pgf}
\else %if using TeX or PDFTeX in TeX mode
  \usepackage{graphicx}
  \DeclareGraphicsExtensions{.eps,.bmp}
  \DeclareGraphicsRule{.emf}{bmp}{}{}% declare EMF filename extension
  \DeclareGraphicsRule{.png}{bmp}{}{}% declare PNG filename extension
\fi

\usepackage[upright]{fourier}
\usepackage{eurosym}

\columnseprule0.25pt
\parindent 0pt\topmargin 0pt\headheight 0pt\headsep 0pt\footskip 0pt
\usepackage[dvips,a4paper,margin=6mm]{geometry}
\everymath{\displaystyle}

%\newcommand\at{@} %% seems to be defined before in LaTeX ?
\newcommand\lb{[}
\newcommand\rb{]}
\newcommand\PYbg[1]{\textcolor[rgb]{0.00,0.50,0.00}{\textbf{#1}}}
\newcommand\PYbf[1]{\colorbox[rgb]{0.88,0.88,0.88}{#1}}
\newcommand\PYbe[1]{\textcolor[rgb]{0.19,0.19,0.19}{#1}}
\newcommand\PYbd[1]{\colorbox[rgb]{1.00,0.94,0.94}{#1}}
\newcommand\PYbc[1]{\textcolor[rgb]{0.00,0.50,0.00}{\textbf{#1}}}
\newcommand\PYbb[1]{\textcolor[rgb]{0.00,0.00,0.50}{\textbf{#1}}}
\newcommand\PYba[1]{\textcolor[rgb]{0.00,0.44,0.00}{#1}}
\newcommand\PYaJ[1]{\colorbox[rgb]{1.00,0.94,0.94}{#1}}
\newcommand\PYaK[1]{\textcolor[rgb]{0.00,0.38,0.69}{\textbf{#1}}}
\newcommand\PYaH[1]{\colorbox[rgb]{0.94,0.63,0.63}{\textcolor[rgb]{0.94,0.00,0.00}{#1}}}
\newcommand\PYaI[1]{\textcolor[rgb]{0.19,0.19,0.56}{\textbf{#1}}}
\newcommand\PYaN[1]{\textcolor[rgb]{0.69,0.00,0.38}{\textbf{#1}}}
\newcommand\PYaO[1]{\textcolor[rgb]{0.78,0.36,0.04}{\textbf{#1}}}
\newcommand\PYaL[1]{\textcolor[rgb]{0.73,0.73,0.73}{#1}}
\newcommand\PYaM[1]{\textcolor[rgb]{0.31,0.44,0.56}{#1}}
\newcommand\PYaB[1]{\textcolor[rgb]{0.00,0.25,0.82}{#1}}
\newcommand\PYaC[1]{\textcolor[rgb]{0.31,0.31,0.31}{\textbf{#1}}}
\newcommand\PYaA[1]{\textcolor[rgb]{0.00,0.44,0.13}{#1}}
\newcommand\PYaF[1]{\textcolor[rgb]{1.00,0.00,0.00}{#1}}
\newcommand\PYaG[1]{\textcolor[rgb]{0.00,0.50,0.00}{\textbf{#1}}}
\newcommand\PYaD[1]{\textcolor[rgb]{0.50,0.50,0.50}{#1}}
\newcommand\PYaE[1]{\textcolor[rgb]{0.63,0.00,0.00}{#1}}
\newcommand\PYaZ[1]{\colorbox[rgb]{1.00,0.94,0.94}{#1}}
\newcommand\PYaX[1]{\colorbox[rgb]{1.00,0.94,0.94}{#1}}
\newcommand\PYaY[1]{\textcolor[rgb]{0.00,0.44,0.13}{#1}}
\newcommand\PYaR[1]{\textcolor[rgb]{0.19,0.19,0.69}{#1}}
\newcommand\PYaS[1]{\textcolor[rgb]{0.00,0.31,0.50}{\textbf{#1}}}
\newcommand\PYaP[1]{\textcolor[rgb]{0.00,0.00,0.75}{#1}}
\newcommand\PYaQ[1]{\textcolor[rgb]{0.38,0.00,0.88}{\textbf{#1}}}
\newcommand\PYaV[1]{\textcolor[rgb]{0.94,0.00,0.00}{\textbf{#1}}}
\newcommand\PYaW[1]{\textcolor[rgb]{0.05,0.52,0.71}{\textbf{#1}}}
\newcommand\PYaT[1]{\textcolor[rgb]{0.50,0.50,0.50}{#1}}
\newcommand\PYaU[1]{\textcolor[rgb]{0.50,0.00,0.50}{\textbf{#1}}}
\newcommand\PYaj[1]{\textcolor[rgb]{0.00,0.19,0.50}{\textbf{#1}}}
\newcommand\PYak[1]{\colorbox[rgb]{1.00,0.94,1.00}{\textcolor[rgb]{0.00,0.00,0.00}{#1}}}
\newcommand\PYah[1]{\textcolor[rgb]{0.56,0.44,0.00}{\textbf{#1}}}
\newcommand\PYai[1]{\textcolor[rgb]{0.56,0.38,0.19}{#1}}
\newcommand\PYan[1]{\textcolor[rgb]{0.00,0.00,0.00}{\textbf{#1}}}
\newcommand\PYao[1]{\colorbox[rgb]{1.00,0.94,0.94}{\textcolor[rgb]{0.38,0.38,0.38}{\textbf{#1}}}}
\newcommand\PYal[1]{\textcolor[rgb]{0.80,0.00,0.00}{\textbf{#1}}}
\newcommand\PYam[1]{\textbf{#1}}
\newcommand\PYab[1]{\textit{#1}}
\newcommand\PYac[1]{\textcolor[rgb]{0.00,0.25,0.82}{#1}}
\newcommand\PYaa[1]{\textcolor[rgb]{0.50,0.50,0.50}{#1}}
\newcommand\PYaf[1]{\textcolor[rgb]{0.50,0.50,0.50}{#1}}
\newcommand\PYag[1]{\textcolor[rgb]{0.00,0.00,0.82}{\textbf{#1}}}
\newcommand\PYad[1]{\colorbox[rgb]{1.00,0.94,0.94}{#1}}
\newcommand\PYae[1]{\textcolor[rgb]{0.25,0.00,0.88}{\textbf{#1}}}
\newcommand\PYaz[1]{\textcolor[rgb]{0.00,0.63,0.00}{#1}}
\newcommand\PYax[1]{\textcolor[rgb]{0.50,0.00,0.00}{\textbf{#1}}}
\newcommand\PYay[1]{\textcolor[rgb]{0.00,0.50,0.00}{\textbf{#1}}}
\newcommand\PYar[1]{\textcolor[rgb]{0.82,0.44,0.00}{\textbf{#1}}}
\newcommand\PYas[1]{\textcolor[rgb]{0.82,0.25,0.13}{#1}}
\newcommand\PYap[1]{\colorbox[rgb]{1.00,0.94,0.94}{\textcolor[rgb]{0.82,0.13,0.00}{#1}}}
\newcommand\PYaq[1]{\textcolor[rgb]{0.00,0.19,0.38}{\textbf{#1}}}
\newcommand\PYav[1]{\textcolor[rgb]{0.00,0.00,0.82}{\textbf{#1}}}
\newcommand\PYaw[1]{\textcolor[rgb]{0.38,0.00,0.88}{\textbf{#1}}}
\newcommand\PYat[1]{\textcolor[rgb]{0.19,0.38,0.56}{#1}}
\newcommand\PYau[1]{\textcolor[rgb]{0.63,0.38,0.00}{#1}}

\begin{document}
""".decode('utf-8')

tex_doc_end = r"""\end{document}""".decode('utf-8')

# ==============================================================================
#XHTML document template
# ==============================================================================
html_doc_start = r"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" >
<head>
    <title>wiKIBlog</title>
    <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
    <link rel="stylesheet" type="text/css" href="holy.css" />
    <link rel="stylesheet" type="text/css" href="pygments.css" />

</head>
<body>

            <div class="col1">""".decode('utf-8')
html_doc_end = r"""
            </div>

</body>
</html>
""".decode('utf-8')