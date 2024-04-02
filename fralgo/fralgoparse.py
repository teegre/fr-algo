import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fralgo.lib.ast import Node, Declare, DeclareArray, ArrayGetItem, ArraySetItem, ArrayResize
from fralgo.lib.ast import Assign, Variable, Print, Read, BinOp, Neg
from fralgo.lib.ast import If, While, For, Len, Mid, Trim, Chr, Ord, Find
from fralgo.lib.ast import ToFloat, ToInteger, ToString, Random
from fralgo.lib.datatypes import map_type
from fralgo.lib.symbols import reset_variables
from fralgo.lib.exceptions import FatalError
import fralgo.fralgolex as lex
from fralgo.ply.yacc import yacc


# --> FOR DEBUGGING ONLY.

def parse_prog(name):
  with open(name, 'r') as f:
    prog = f.read()
    prog = prog[:-1]
  return parser.parse(prog)

def reset():
  parser.restart()
  reset_variables()

# <--

tokens = lex.tokens

precedence = (
    ('left', 'EQ', 'GT', 'LT', 'GE', 'LE'),
    ('left', 'CONCAT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV', 'MODULO'),
    ('left', 'POWER'),
    ('right', 'UMINUS')
)

# GRAMMAR

def p_program(p):
  '''
  program : var_declarations statements
          | var_declarations
          | statement
          | START NEWLINE statements END
          | var_declarations START NEWLINE statements END
  '''
  root = Node()
  if len(p) == 5:
    root.append(p[3])
  elif len(p) == 6:
    root.append(p[1])
    root.append(p[4])
  # FOR FUTURE REPL
  elif len(p) == 3:
    root.append(p[1])
    root.append(p[2])
  else:
    root.append(p[1])

  p[0] = root

def p_var_declarations(p):
  '''
  var_declarations : var_declarations var_declaration
                   | var_declaration
  '''
  if len(p) == 2:
    p[0] = Node(p[1], p.lineno(1))
  else:
    p[1].append(p[2])
    p[0] = p[1]

def p_var_declaration(p):
  '''
  var_declaration : ARRAY_DECL array TYPE_DECL type NEWLINE
                  | ARRAYS_DECL array_list TYPE_DECL type NEWLINE
                  | VAR_DECL ID TYPE_DECL type NEWLINE
                  | VARS_DECL var_list TYPE_DECL type NEWLINE
  '''
  if p[1].startswith('Tableau'):
    # p[2] is a list of this form:
    # ['name1', ['name2', [x1, x2, ..., xN]], 'name3', ..., ['nameN', [x1, x2, ..., xN]]]
    # name being the variable name and x being indexes.
    declarations = Node(lineno=p.lineno(1))
    for params in p[2]:
      if not isinstance(params, list):
        name = params
        indexes = [-1]
      else:
        name, indexes = (params[0], params[1])
      declarations.append(DeclareArray(name, p[4], *indexes))
    p[0] = declarations
  else:
    if isinstance(p[2], list):
      declarations = Node(lineno=p.lineno(1))
      for name in p[2]:
        declarations.append(Declare(name, p[4]))
      p[0] = declarations
    else:
      p[0] = Node(Declare(p[2], p[4]), p.lineno(1))

def p_array_list(p):
  '''
  array_list : array_list COMMA array
             | array
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = p[1] + p[3]

def p_array(p):
  '''
  array : ID LBRACKET RBRACKET
        | ID LBRACKET array_max_indexes RBRACKET
  '''
  if len(p) == 4:
    p[0] = [p[1]]
  else:
    p[0] = [[p[1], p[3]]]

def p_array_max_indexes(p):
  '''
  array_max_indexes : array_max_indexes COMMA array_max_index
                    | array_max_index
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = p[1] + p[3]

def p_array_max_index(p):
  '''
  array_max_index : INTEGER
  '''
  p[0] = [p[1]]

def p_var_list(p):
  '''
  var_list : var_list COMMA d_var
           | d_var
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    p[0] = p[1] + p[3]

def p_d_var(p):
  '''
  d_var : ID
  '''
  # A variable name in a multiple variables declaration.
  p[0] = [p[1]]

def p_var(p):
  '''
  var : ID
  '''
  # A variable.
  p[0] = Variable(p[1])

def p_type(p):
  '''
  type : TYPE_BOOLEAN
       | TYPE_FLOAT
       | TYPE_INTEGER
       | TYPE_STRING
  '''
  if len(p) == 2:
    p[0] = p[1]

def p_array_access(p):
  '''
  array_access : var LBRACKET array_indexes RBRACKET
  '''
  indexes = tuple(index for index in p[3])
  p[0] = [p[1], indexes]

def p_array_indexes(p):
  '''
  array_indexes : array_indexes COMMA array_index
                | array_index
  '''
  if len(p) == 4:
    p[0] = p[1] + p[3]
  else:
    p[0] = p[1]

def p_array_index(p):
  '''
  array_index : expression
  '''
  p[0] = [map_type(p[1])]

def p_array_resize(p):
  '''
  array_resize : RESIZE var LBRACKET array_indexes RBRACKET
  '''
  indexes = tuple(index for index in p[4])
  p[0] = Node(ArrayResize(p[2], *indexes), p.lineno(1))

def p_statements(p):
  '''
  statements : statements statement
             | statement
  '''
  if len(p) == 2:
    p[0] = Node(p[1], p.lineno(1))
  else:
    p[1].append(p[2])
    p[0] = p[1]

def p_statement(p):
  '''
  statement : var_assignment
            | array_assignment
            | array_resize NEWLINE
            | if_block
            | while_block
            | for_block
            | PRINT sequence NEWLINE
            | PRINT sequence BACKSLASH NEWLINE
            | READ ID NEWLINE
            | READ array_access NEWLINE
            | expression NEWLINE
  '''
  if p[1] == 'Ecrire':
    newline = len(p) < 5
    p[0] = Node(Print(p[2], newline), p.lineno(1))
  elif p[1] == 'Lire':
    if isinstance(p[2], list):
      # Array!
      p[0] = Node(Read(p[2][0].name, *p[2][1]), p.lineno(1))
    else:
      p[0] = Node(Read(p[2]), p.lineno(1))
  else:
    p[0] = Node(p[1], p.lineno(1))

def p_var_assignment(p):
  '''
  var_assignment : ID ARROW expression NEWLINE
  '''
  assignment = Assign(p[1], p[3])
  p[0] = Node(assignment, p.lineno(1))

def p_array_assignment(p):
  '''
  array_assignment : array_access ARROW expression NEWLINE
  '''
  p[0] = Node(ArraySetItem(p[1][0], p[3], *p[1][1]), p.lineno(1))

def p_array_get_item(p):
  '''
  array_get_item : array_access
  '''
  p[0] = ArrayGetItem(p[1][0], *p[1][1])

def p_if_block(p):
  '''
  if_block : IF expression THEN NEWLINE statements else_blocks
  '''
  p[0] = Node(If(p[2], p[5], p[6]), p.lineno(1))

def p_else_blocks(p):
  '''
  else_blocks : else_if_block
              | else_block
              | ENDIF NEWLINE
  '''
  p[0] = p[1] if len(p) == 2 else None

def p_else_if_block(p):
  '''
  else_if_block : ELSIF expression THEN NEWLINE statements else_blocks
  '''
  p[0] = Node(If(p[2], p[5], p[6]), p.lineno(1))

def p_else_block(p):
  '''
  else_block : ELSE NEWLINE statements ENDIF NEWLINE
  '''
  p[0] = p[3]

def p_while_block(p):
  '''
  while_block : WHILE expression NEWLINE statements ENDWHILE NEWLINE
  '''
  p[0] = Node(While(p[2], p[4]), p.lineno(1))

def p_for_block(p):
  '''
  for_block : FOR var ARROW expression TO expression NEWLINE statements var NEXT NEWLINE
            | FOR var ARROW expression TO expression STEP expression NEWLINE statements var NEXT NEWLINE
  '''
  if len(p) == 12:
    p[0] = Node(For(p[2], p[4], p[6], p[8], p[9]), p.lineno(1))
  else:
    p[0] = Node(For(p[2], p[4], p[6], p[10], p[11], p[8]), p.lineno(1))

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
  '''
  p[0] = [map_type(p[1])]

def p_expression(p):
  '''
  expression : BOOL_TRUE
             | BOOL_FALSE
             | FLOAT
             | INTEGER
             | STRING
             | var
  '''
  p[0] = map_type(p[1])

def p_expression_binop(p):
  '''
  expression : expression PLUS expression
             | expression MINUS expression
             | expression MUL expression
             | expression DIV expression
             | expression DIVBY expression
             | expression MODULO expression
             | expression POWER expression
             | expression EQ expression
             | expression LT expression
             | expression GT expression
             | expression LE expression
             | expression GE expression
             | expression NE expression
  '''

  a = p[1]
  b = p[3]

  p[0] = BinOp(p[2], a, b)

def p_expression_logical(p):
  '''
  expression : expression AND expression
             | expression OR expression
             | expression XOR expression
  '''
  a = p[1]
  b = p[3]

  p[0] = BinOp(p[2], a, b)

def p_expression_concat(p):
  '''
  expression : expression CONCAT expression
  '''
  a = p[1]
  b = p[3]

  p[0] = BinOp(p[2], a, b)

def p_expression_not(p):
  '''
  expression : NOT LPAREN expression RPAREN
  '''
  a = p[3]

  p[0] = BinOp(p[1], a, None)

def p_expression_array_get_item(p):
  '''
  expression : array_get_item
  '''
  p[0] = p[1]

def p_expression_len(p):
  '''
  expression : LEN LPAREN expression RPAREN
  '''
  p[0] = Len(p[3])

def p_expression_mid(p):
  '''
  expression : MID LPAREN expression COMMA expression COMMA expression RPAREN
  '''
  p[0] = Mid(p[3], p[5], p[7])

def p_expression_trim(p):
  '''
  expression : LTRIM LPAREN expression COMMA expression RPAREN
             | RTRIM LPAREN expression COMMA expression RPAREN
  '''
  p[0] = Trim(p[3], p[5], right=p[1] == 'Droite')

def p_expression_find(p):
  '''
  expression : FIND LPAREN expression COMMA expression RPAREN
  '''
  p[0] = Find(p[3], p[5])

def p_expression_chr_ord(p):
  '''
  expression : CHR LPAREN expression RPAREN
             | ORD LPAREN expression RPAREN
  '''
  if p[1] == 'Car':
    p[0] = Chr(p[3])
  else:
    p[0] = Ord(p[3])

def p_expression_type_conv(p):
  '''
  expression : TYPE_INTEGER LPAREN expression RPAREN
             | TYPE_FLOAT LPAREN expression RPAREN
             | TYPE_STRING LPAREN expression RPAREN
  '''
  match p[1]:
    case 'Entier':
      p[0] = ToInteger(p[3])
    case 'Numérique':
      p[0] = ToFloat(p[3])
    case 'Chaîne':
      p[0] = ToString(p[3])


def p_expression_random(p):
  '''
  expression : RANDOM LPAREN RPAREN
  '''
  p[0] = Random()

def p_expression_group(p):
  '''
  expression : LPAREN expression RPAREN
  '''
  p[0] = p[2]

def p_expression_uminus(p):
  '''
  expression : MINUS expression %prec UMINUS
  '''
  p[0] = Neg(p[2])

def p_error(p):
  if p:
    try:
      value = p.value.replace('\n', '↵')
    except:
      value = p.value
    print(f'*** Erreur de syntaxe >> {value} <<')
    if 'FRALGOREPL' not in os.environ:
      print(f'-v- ligne {p.lineno}')
      raise FatalError('*** Erreur fatale')
  else:
    print('*** Fin de fichier prématurée.')

parser = yacc()
