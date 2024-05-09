'''Lexer'''
#  _______ ______        _______ _____   _______ _______
# |    ___|   __ \______|   _   |     |_|     __|       |
# |    ___|      <______|       |       |    |  |   -   |
# |___|   |___|__|      |___|___|_______|_______|_______|
#
# This file is part of FRALGO
# Copyright © 2024 Stéphane MEYER (Teegre)
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fralgo.lib.exceptions import FralgoException, FatalError
from fralgo.ply.lex import lex

reserved = {
  'Importer':      'IMPORT',
  'Variable':      'VAR_DECL',
  'Variables':     'VARS_DECL',
  'Tableau':       'ARRAY_DECL',
  'Tableaux':      'ARRAYS_DECL',
  'Redim':         'RESIZE',
  'Taille':        'SIZE',
  'en':            'TYPE_DECL',
  'Booléen':       'TYPE_BOOLEAN',
  'Caractère':     'TYPE_CHAR',
  'Chaîne':        'TYPE_STRING',
  'Entier':        'TYPE_INTEGER',
  'Numérique':     'TYPE_FLOAT',
  'Début':         'START',
  'Fin':           'END',
  'Librairie':     'LIB',
  'Initialise':    'INIT',
  'Ecrire':        'PRINT',
  'EcrireErr':     'PRINTERR',
  'Lire':          'READ',
  'DP':            'DIVBY',
  'ET':            'AND',
  'OU':            'OR',
  'OUX':           'XOR',
  'NON':           'NOT',
  'Si':            'IF',
  'Alors':         'THEN',
  'Sinon':         'ELSE',
  'SinonSi':       'ELSIF',
  'FinSi':         'ENDIF',
  'TantQue':       'WHILE',
  'FinTantQue':    'ENDWHILE',
  'Pour':          'FOR',
  'à':             'TO',
  'Pas':           'STEP',
  'Suivant':       'NEXT',
  'Longueur':      'LEN',
  'Extraire':      'MID',
  'Gauche':        'LTRIM',
  'Droite':        'RTRIM',
  'Trouve':        'FIND',
  'Car':           'CHR',
  'CodeCar':       'ORD',
  'Aléa':          'RANDOM',
  'Dormir':        'SLEEP',
  'TempsUnix':     'UNIXTIMESTAMP',
  'Ouvrir':        'OPEN',
  'Fermer':        'CLOSE',
  'LireFichier':   'READFILE',
  'EcrireFichier': 'WRITEFILE',
  'sur':           'FD_ON',
  'Lecture':       'MODE_READ',
  'Ecriture':      'MODE_WRITE',
  'Ajout':         'MODE_APPEND',
  'FDF':           'EOF',
  'Structure':     'STRUCT',
  'FinStructure':  'ENDSTRUCT',
  'Fonction':      'FUNCTION',
  'Retourne':      'RETURN',
  'FinFonction':   'ENDFUNCTION',
  'Procédure':     'PROCEDURE',
  'FinProcédure':  'ENDPROCEDURE',
}

tokens = (
  'PLUS', 'MINUS', 'MUL', 'DIV', 'POWER', 'CONCAT',
  'EQ', 'NE', 'GT', 'GE', 'LT', 'LE',
  'ARROW',
  'BOOL_TRUE', 'BOOL_FALSE', 'FLOAT', 'INTEGER', 'STRING',
  'MODULO',
  'LPAREN', 'RPAREN',
  'LBRACKET', 'RBRACKET',
  'COMMA',
  'DOT',
  'BACKSLASH',
  'NEWLINE',
  'ID',
) + tuple(reserved.values())

t_PLUS = r'\+'
t_ARROW = r'←|<\-' # AltGr + y
t_MUL = r'\*'
t_DIV = r'/'
t_MODULO = r'\%'
t_EQ = r'='
t_GE = r'>='
t_LE = r'<='
t_NE = r'<>'
t_GT = r'>'
t_LT = r'<'
t_POWER = r'\^'
t_CONCAT = r'&'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r'\,'
t_DOT = r'\.'
t_BACKSLASH = r'\\'

t_ignore = ' \t'

def t_STRING(t):
  r'\".*?\"|\'.*?\''
  t.value = bytes(t.value[1:-1], 'utf-8').decode('unicode-escape')
  return t

def t_FLOAT(t):
  r'\d+\.\d+'
  t.value = float(t.value)
  return t

def t_INTEGER(t):
  r'\d+'
  t.value = int(t.value)
  return t

def t_BOOL_TRUE(t):
  r'VRAI'
  t.value = True
  return t

def t_BOOL_FALSE(t):
  r'FAUX'
  t.value = False
  return t

def t_MINUS(t):
  r'-'
  return t

def t_ID(t):
  r'[A-Za-zàéèî\_][A-Za-zàéèî0-9\_]*'
  t.type = reserved.get(t.value, 'ID')
  return t

def t_COMMENT(t):
  r'\#.*\n*'
  t.lexer.lineno += 1

def t_NEWLINE(t):
  r'\n+'
  t.lexer.lineno += len(t.value)
  return t

def t_error(t):
  msg = (f'*** caractère invalide {t.value[0]!r}')
  if 'FRALGOREPL' not in os.environ:
    msg += f'\n-v- ligne {t.lineno}.'
    raise FatalError(msg)
  t.lexer.skip(1)
  raise FralgoException(msg)

lexer = lex()
