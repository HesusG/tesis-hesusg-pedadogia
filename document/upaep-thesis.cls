%% upaep-thesis.cls — Clase para tesis UPAEP
%% Maestría en Pedagogía
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{upaep-thesis}[2024/01/01 Clase para tesis UPAEP]

% Base class
\LoadClass[12pt,letterpaper,oneside]{report}

% ── Packages ──
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage[spanish,es-tabla]{babel}
\RequirePackage{mathptmx}                    % Times New Roman
\RequirePackage[left=1in,right=1in,top=1in,bottom=1in]{geometry}
\RequirePackage{setspace}                    % 1.5 spacing
\RequirePackage[natbibapa]{apacite}          % APA style citations
\RequirePackage{graphicx}
\RequirePackage{booktabs}
\RequirePackage{longtable}
\RequirePackage{array}
\RequirePackage{multirow}
\RequirePackage{float}
\RequirePackage{caption}
\RequirePackage{subcaption}
\RequirePackage{hyperref}
\RequirePackage{url}
\RequirePackage{xcolor}
\RequirePackage{enumitem}
\RequirePackage{titlesec}
\RequirePackage{fancyhdr}
\RequirePackage{etoolbox}
\RequirePackage{csquotes}

% ── Spacing ──
\onehalfspacing

% ── Colors ──
\definecolor{upaep-blue}{RGB}{0,51,102}

% ── Hyperref setup ──
\hypersetup{
    colorlinks=true,
    linkcolor=upaep-blue,
    citecolor=upaep-blue,
    urlcolor=upaep-blue,
    bookmarks=true,
    bookmarksnumbered=true,
}

% ── Headers ──
\pagestyle{fancy}
\fancyhf{}
\fancyhead[R]{\thepage}
\renewcommand{\headrulewidth}{0pt}

% ── Chapter format ──
\titleformat{\chapter}[display]
  {\normalfont\Large\bfseries}
  {\chaptertitlename\ \thechapter}{20pt}{\LARGE}
\titlespacing*{\chapter}{0pt}{-20pt}{40pt}

% ── Section format ──
\titleformat{\section}
  {\normalfont\large\bfseries}
  {\thesection}{1em}{}
\titleformat{\subsection}
  {\normalfont\normalsize\bfseries}
  {\thesubsection}{1em}{}

% ── Caption format ──
\captionsetup{
    font=small,
    labelfont=bf,
    format=hang,
    margin=1cm,
}

% ── Paragraph ──
\setlength{\parindent}{1.27cm}  % APA standard
\setlength{\parskip}{0pt}

% ── Custom commands ──
\newcommand{\tesistitle}[1]{\def\@tesistitle{#1}}
\newcommand{\tesisauthor}[1]{\def\@tesisauthor{#1}}
\newcommand{\tesisdirector}[1]{\def\@tesisdirector{#1}}
\newcommand{\tesisprograma}[1]{\def\@tesisprograma{#1}}
\newcommand{\tesisfecha}[1]{\def\@tesisfecha{#1}}
\newcommand{\tesisciudad}[1]{\def\@tesisciudad{#1}}

% Defaults
\tesistitle{Título de la tesis}
\tesisauthor{Nombre del autor}
\tesisdirector{Nombre del director}
\tesisprograma{Maestría en Pedagogía}
\tesisfecha{\the\year}
\tesisciudad{Puebla, Puebla}

\endinput
