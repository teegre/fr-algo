'''Parser for the pseudo-language Algo'''
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

# import sys
import lexer as lex
from lib.absytr import Statements, Print, Read, BinOp
from lib.datatypes import map_type
from lib.symbols import declare_var, assign_value, get_variable
import lib.exceptions as ex
from ply.yacc import yacc

tokens = lex.tokens

precedence = (
    ('left', 'EQ', 'GT', 'LT', 'GE', 'LE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
    ('left', 'POWER'),
    ('right', 'UMINUS'),
)

def p_program(p):
  '''
  program : PROG_START NEWLINE statements PROG_END
          | var_declarations PROG_START NEWLINE statements PROG_END
  '''
  if len(p) == 6:
    p[0] = p[4]
  else:
    p[0] = p[3]

def p_var_declarations(p):
  '''
  var_declarations : var_declarations var_declaration
                   | var_declaration
  '''
  p[0] = None

def p_var_declaration(p):
  '''
  var_declaration : VAR_DECL ID TYPE_DECL type NEWLINE
                  | VARS_DECL var_list TYPE_DECL type NEWLINE
  '''
  if len(p) == 6:
    try:
      if isinstance(p[2], list):
        for var in p[2]:
          declare_var(var, p[4])
      else:
        declare_var(p[2], p[4])
      p[0] = None
    except ex.VarUndeclared as e:
      print(f'*** {e.message}')
      print(f'-v- ligne {p.lineno(1)}')
      print(f'->- position {p.lexpos(1)+1}')
      # sys.exit(1)

def p_type(p):
  '''
  type : TYPE_BOOLEAN
       | TYPE_FLOAT
       | TYPE_INTEGER
       | TYPE_STRING
  '''
  p[0] = p[1]

def p_var_list(p):
  # list of variables: a, b, c
  '''
  var_list : var_list COMMA u_var
           | u_var
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = p[1] + p[3]

def p_u_var(p):
  # variable not declared yet
  '''
  u_var : ID
  '''
  p[0] = [p[1]]

def p_var(p):
  # declared variable
  '''
  var : ID
  '''
  try:
    p[0] = get_variable(p[1])
  except ex.VarUndeclared as e:
    print(f'*** {e.message}')
    print(f'-v- ligne {p.lineno(1)}')
    print(f'->- position {p.lexpos(1)+1}')
    # sys.exit(1)

def p_statements(p):
  '''
  statements : statements statement
             | statement 
  '''
  if len(p) == 2:
    p[0] = Statements(p[1])
  else:
    p[1].append(p[2])
    p[0] = p[1]

def p_statement(p):
  '''
  statement : expression
  '''
  p[0] = map_type(p[1])

def p_sequence(p):
  '''
  sequence : sequence COMMA element
           | element
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = p[1] + p[3]

def p_element(p):
  '''
  element : expression
          | STRING
          | BOOL_TRUE
          | BOOL_FALSE
          | INTEGER
          | FLOAT
  '''
  p[0] = [map_type(p[1])]

def p_expression(p):
  '''
  expression : var_assignment
             | PRINT sequence NEWLINE
             | READ ID NEWLINE
             | FLOAT
             | INTEGER
             | STRING
             | BOOL_TRUE
             | BOOL_FALSE
             | var
             | ID

  '''
  if p[1] == 'Ecrire':
    Print(p[2]).eval()
  elif p[1] == 'Lire':
    Read(p[2]).eval()
  else:
    p[0] = map_type(p[1])

def p_expression_binop(p):
  '''
  expression : expression PLUS expression
             | expression MINUS expression
             | expression MUL expression
             | expression DIV expression
             | expression DIVBY expression
             | expression POWER expression
             | expression CONCAT expression
             | expression EQ expression
             | expression LT expression
             | expression GT expression
             | expression LE expression
             | expression GE expression
             | expression NE expression
             | expression AND expression
             | expression OR expression
             | expression XOR expression
  '''

  a = map_type(p[1])
  b = map_type(p[3])
  op = p[2]

  if op in ('ET', 'OU', 'XOR'):
    if not isinstance(a.eval(), bool) and not isinstance(b.eval(), bool):
      raise ex.BadType(f'type Booléen attendu')
    result = map_type(BinOp(op, a, b))
  elif op == '/':
    # Return an Integer if both value are int.
    if isinstance(a.eval(), int) and isinstance(b.eval(), int):
      result = map_type(BinOp(op, a, b))
    # Return a Float if at least one value is a float.
    elif isinstance(a.eval(), float) or isinstance(b.eval(), float):
      result = map_type(BinOp('//', a, b))
    else:
      raise ex.BadType('type Numérique ou Entier attendu')
  elif op == '&':
    if isinstance(a.eval(), str) and isinstance(b.eval(), str):
      result = map_type(a.eval() + b.eval())
    else:
      raise ex.BadType(f'concaténation de [{a}] et [{b}] impossible')
  else:
    result = map_type(BinOp(op, a, b))
  p[0] = result.eval()

def p_expression_uminus(p):
  '''
  expression : MINUS expression %prec UMINUS
  '''
  try:
    p[0] = map_type(-p[2].eval())
  except TypeError as e:
    raise ex.BadType('type Numérique ou Entier attendu') from e

def p_expression_not(p):
  '''
  expression : NOT LPAREN expression RPAREN
  '''
  result = map_type(BinOp(p[1], p[3], None))
  p[0] = result.eval()


def p_expression_group(p):
  '''
  expression : LPAREN expression RPAREN
  '''
  p[0] = p[2]

def p_var_assignment(p):
  '''
  var_assignment : ID ARROW BOOL_TRUE NEWLINE
                 | ID ARROW BOOL_FALSE NEWLINE
                 | ID ARROW FLOAT NEWLINE
                 | ID ARROW INTEGER NEWLINE
                 | ID ARROW STRING NEWLINE
                 | ID ARROW expression NEWLINE
  '''
  if len(p) == 5:
    try:
      assign_value(p[1], p[3])
    except (ex.VarUndeclared, ex.BadType) as e:
      print(f'*** {e.message}')
      print(f'-v- ligne {p.lineno(1)}')
      print(f'->- position {p.lexpos(1)+1}')
      # sys.exit(1)

  p[0] = None

def p_error(p):
  if p:
    value = p.value.replace('\n', '↵')
    print(f'*** erreur de syntaxe >> {value} <<')
    print(f'-v- ligne {p.lineno}')
    print(f'->- position {p.lexpos+1}')
  else:
    print('*** fin de fichier prématurée.')
  # sys.exit(1)

parser = yacc()
prog = '''Variable n en Entier
Variables x, y, z en Numérique
Variable s en Chaîne
Variable b en Booléen
Début
  x ← 1.2
  y ← 3.4
  z ← 5.6
  n ← 7
  s ← "Huit !"
  b ← VRAI
  Ecrire "Les valeurs de x, y et z sont " x ", " y ", " z
  Ecrire "n est égal à " n
  Ecrire "s vaut " s " et b est " b
  Ecrire n
Fin'''
