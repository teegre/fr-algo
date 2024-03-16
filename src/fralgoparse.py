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

import sys
import fralgoast
import fralgolex as lexer
import fralgoexception as ex
from ply.yacc import yacc

tokens = lexer.tokens

def p_program(p):
  '''
  program : var_declarations PROG_START NEWLINE statements PROG_END
          | PROG_START NEWLINE statements PROG_END
  '''

def p_statements(p):
  '''
  statements : statements statement
             | statement 
  '''

def p_statement(p):
  '''
  statement : expression
  '''

def p_expression(p):
  '''
  expression : var_assignment
             | PRINT ID NEWLINE
  '''
  if p[1] == 'Ecrire':
    try:
      var = fralgoast.get_variable(p[2])
      if var.type == 'Booléen':
        if var.value:
          print('VRAI')
        else:
          print('FAUX')
      else:
        print(var.value)
    except ex.FralgoException as e:
      print(f'***** {e.message}')
      print(f'----- ligne {p.lineno(1)}')
      print(f'----- position {p.lexpos(1)+1}')
      sys.exit(1)

def p_var_assignment(p):
  '''
  var_assignment : ID ARROW BOOL_TRUE NEWLINE
                 | ID ARROW BOOL_FALSE NEWLINE
                 | ID ARROW FLOAT NEWLINE
                 | ID ARROW INTEGER NEWLINE
                 | ID ARROW STRING NEWLINE
  '''
  if len(p) == 5:
    try:
      fralgoast.assign_value(p[1], p[3])
    except ex.FralgoException as e:
      print(f'****** {e.message}')
      print(f'------ ligne {p.lineno(1)}')
      print(f'------ position {p.lexpos(1)+1}')
      sys.exit(1)

def p_var_declarations(p):
  '''
  var_declarations : var_declarations var_declaration
                   | var_declaration
  '''

def p_var_declaration(p):
  '''
  var_declaration : VAR_DECL ID TYPE_DECL type NEWLINE
                  | VARS_DECL var_list TYPE_DECL type NEWLINE
  '''
  if len(p) == 6:
    try:
      if isinstance(p[2], list):
        for var in p[2]:
          fralgoast.declare_var(var, p[4])
      else:
        fralgoast.declare_var(p[2], p[4])
    except ex.FralgoException as e:
      print(f'****** {e.message}')
      print(f'------ ligne {p.lineno(1)}')
      print(f'------ position {p.lexpos(1)+1}')
      sys.exit(1)

def p_type(p):
  '''
  type : TYPE_BOOLEAN
       | TYPE_FLOAT
       | TYPE_INTEGER
       | TYPE_STRING
  '''
  p[0] = p[1]

def p_var_list(p):
  '''
  var_list : var_list COMMA var
           | var
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = p[1] + p[3]

def p_var(p):
  '''
  var : ID
  '''
  p[0] = [p[1]]

def p_error(p):
  if p:
    print(f'******* erreur de syntaxe >> {p.value} <<')
    print(f'------- ligne {p.lineno}')
    print(f'------- position {p.lexpos+1}')
  else:
    print('****** fin de fichier inattendue.')

parser = yacc()
