'''Lexer'''
#  _______ ______        _______ _____   _______ _______
# |    ___|   __ \______|   _   |     |_|     __|       |
# |    ___|      <______|       |       |    |  |   -   |
# |___|   |___|__|      |___|___|_______|_______|_______|
#
# This file is part of FR-ALGO
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
  'Ajout':         'MODE_APPEND',
  'Alias':         'ALIAS',
  'Alors':         'THEN',
  'Aléa':          'RANDOM',
  'Booléen':       'TYPE_BOOLEAN',
  'Car':           'CHR',
  'Caractère':     'TYPE_CHAR',
  'Chaîne':        'TYPE_STRING',
  'Clef':          'KEY',
  'Clefs':         'KEYS',
  'CodeCar':       'ORD',
  'DP':            'DIVBY',
  'Dormir':        'SLEEP',
  'Droite':        'RTRIM',
  'Début':         'START',
  'ET':            'AND',
  'Ecrire':        'PRINT',
  'EcrireErr':     'PRINTERR',
  'EcrireFichier': 'WRITEFILE',
  'Ecriture':      'MODE_WRITE',
  'Entier':        'TYPE_INTEGER',
  'Existe':        'EXISTS',
  'Extraire':      'MID',
  'FDF':           'EOF',
  'Fermer':        'CLOSE',
  'Fin':           'END',
  'FinFonction':   'ENDFUNCTION',
  'FinProcédure':  'ENDPROCEDURE',
  'FinSi':         'ENDIF',
  'FinStructure':  'ENDSTRUCT',
  'FinTable':      'ENDTABLE',
  'FinTantQue':    'ENDWHILE',
  'Fonction':      'FUNCTION',
  'Gauche':        'LTRIM',
  'Importer':      'IMPORT',
  'Initialise':    'INIT',
  'Lecture':       'MODE_READ',
  'Librairie':     'LIB',
  'Lire':          'READ',
  'LireFichier':   'READFILE',
  'Longueur':      'LEN',
  'NON':           'NOT',
  'Numérique':     'TYPE_FLOAT',
  'OU':            'OR',
  'OUX':           'XOR',
  'Ouvrir':        'OPEN',
  'Pas':           'STEP',
  'Pour':          'FOR',
  'Procédure':     'PROCEDURE',
  'Quelconque':    'TYPE_ANY',
  'Redim':         'RESIZE',
  'Retourne':      'RETURN',
  'Si':            'IF',
  'Sinon':         'ELSE',
  'SinonSi':       'ELSIF',
  'Structure':     'STRUCT',
  'Suivant':       'NEXT',
  'Table':         'TYPE_TABLE',
  'Tableau':       'ARRAY_DECL',
  'Tableaux':      'ARRAYS_DECL',
  'Taille':        'SIZE',
  'TantQue':       'WHILE',
  'TempsUnix':     'UNIXTIMESTAMP',
  'Trouve':        'FIND',
  'Type':          'DATA_TYPE',
  'Valeur':        'VALUE',
  'Valeurs':       'VALUES',
  'Variable':      'VAR_DECL',
  'Variables':     'VARS_DECL',
  'en':            'TYPE_DECL',
  'sur':           'FD_ON',
  'à':             'TO',
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
  'COLON',
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
t_COLON = r':'
t_BACKSLASH = r'\\'

t_ignore = ' \t'

def t_STRING(t):
  r'\".*?\"|\'.*?\''
  t.value = t.value[1:-1].encode('latin-1', 'ignore').decode('unicode-escape', 'ignore')
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
  msg = f'*** caractère invalide {t.value[0]!r}'
  if 'FRALGOREPL' not in os.environ:
    msg += f'\n-v- ligne {t.lineno}.'
    raise FatalError(msg)
  t.lexer.skip(1)
  raise FralgoException(msg)

lexer = lex()
