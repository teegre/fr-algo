from lib.ast import Node, Declare, DeclareArray, ArrayGetItem, ArraySetItem, ArrayResize
from lib.ast import Assign, Variable, Print, Read, BinOp, Neg, If, While, For
from lib.datatypes import map_type, Number
from lib.symbols import reset_variables
from lib.exceptions import BadType
import lexer as lex
from ply.yacc import yacc


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
    ('left', 'MUL', 'DIV'),
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
    # ['name1', ['name2', [index1, index2, ..., indexN]], 'name3', ..., ['nameN', [index1, index2, indexN]]]
    # name being the variable name and index being indexes.
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
            | READ ID NEWLINE
            | expression NEWLINE
  '''
  if p[1] == 'Ecrire':
    p[0] = Node(Print(p[2]), p.lineno(1))
  elif p[1] == 'Lire':
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

def p_expression_binop_div(p):
  '''
  expression : expression DIV expression
  '''
  a = p[1]
  b = p[3]

  # Make sure we're dealing with numbers.
  if isinstance(a.eval(), int) and isinstance(b.eval(), int):
    binop = BinOp('//', a, b)
  # Return a Float if one of the value is a float.
  elif isinstance(a.eval(), float) or isinstance(b.eval(), float):
    binop = BinOp(p[2], a, b)

  p[0] = binop

def p_expression_logical(p):
  '''
  expression : expression AND expression
             | expression OR expression
             | expression XOR expression
  '''
  a = p[1]
  b = p[3]

  # if not isinstance(a, Boolean) or not isinstance(b, Boolean):
  #   raise BadType('type Booléen attendu')

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
    print(f'*** erreur de syntaxe >> {value} <<')
    print(f'-v- ligne {p.lineno}')
    print(f'->- position {p.lexpos+1}')
  else:
    print('*** fin de fichier prématurée.')

parser = yacc()
