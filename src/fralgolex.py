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

from ply.lex import lex

reserved = {
  'Variable':   'VAR_DECL',
  'Variables':  'VARS_DECL',
  'en':         'TYPE_DECL',
  'Booléen':    'TYPE_BOOLEAN',
  'Entier':     'TYPE_INTEGER',
  'Chaîne':     'TYPE_STRING',
  'Numérique':  'TYPE_FLOAT',
  'Début':      'PROG_START',
  'Fin':        'PROG_END',
  # 'Ecrire':     'PRINT',
  # 'Lire':       'READ',
  # 'Si':         'COND_IF',
  # 'Sinon':      'COND_ELSE',
  # 'SinonSi':    'COND_ELSIF',
  # 'FinSi':      'COND_ENDIF',
  # 'TantQue':    'LOOP_WHILE',
  # 'FinTantQue': 'LOOP_ENDWHILE',
  # 'Pour':       'LOOP_FOR',
  # 'à':          'LOOP_FOR_RANGE',
  # 'Suivant':    'LOOP_FOR_NEXT',
}

tokens = (
  # 'PLUS', 'MINUS', 'MUL', 'DIV', 'DIVBY',
  # 'EQ', 'NE', 'GT', 'GE', 'LT', 'LE',
  # 'POWER',
  # 'LPAREN', 'RPAREN', 'ARROW', 'COMMA',
  'ARROW',
  'BOOL_TRUE', 'BOOL_FALSE', 'FLOAT', 'INTEGER', 'STRING',
  'COMMA',
  'NEWLINE',
  'ID',
) + tuple(reserved.values())

t_ARROW = '←'
# t_PLUS = r'\+'
# t_MUL = r'\*'
# t_DIV = r'/'
# t_DIVBY = r'dp'
# t_EQ = r'='
# t_GT = r'>'
# t_LT = r'<'
# t_GE = r'>='
# t_LE = r'<='
# t_NE = r'<>'
# t_LPAREN = r'\('
# t_RPAREN = r'\)'
t_COMMA = r'\,'

t_ignore = ' \t'

def t_STRING(t):
  r'\".*?\"|\'.*?\''
  t.value = bytes(t.value[1:-1], 'latin-1').decode('unicode-escape')
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

# def t_MINUS(t):
#   r'-'
#   return t

def t_ID(t):
  r'[A-Za-zàéî\-_][A-Za-zàéî0-9\-_]*'
  t.type = reserved.get(t.value, 'ID')
  return t

def t_NEWLINE(t):
  r'\n+'
  t.lexer.lineno += len(t.value)
  return t


def t_error(t):
  print(f'****** caractère invalide {t.value[0]!r}')
  print(f'erreur: ligne n° {t.lineno}.')
  t.lexer.skip(1)

lexer = lex()
