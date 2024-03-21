from lib.ast import Node, Declare, Assign, Variable, Print, Read, BinOp, Neg, If
from lib.datatypes import map_type, Boolean, Number, String
from lib.exceptions import BadType
import lexer as lex
from ply.yacc import yacc

# For debugging

from lib.ast import print_tree

def parse_prog(name):
  with open(name, 'r') as f:
    prog = f.read()
    prog = prog[:-1]
  return parser.parse(prog)

tokens = lex.tokens

precedence = (
    ('left', 'EQ', 'GT', 'LT', 'GE', 'LE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
    ('left', 'POWER'),
    ('right', 'UMINUS')
)

# GRAMMAR

_ast = Node()

def p_program(p):
  '''
  program : START NEWLINE statements END
          | var_declarations START NEWLINE statements END
  '''
  if len(p) == 5:
    _ast.append(p[3])
  else:
    _ast.append(p[4])
  p[0] = _ast

def p_var_declarations(p):
  '''
  var_declarations : var_declarations var_declaration
                   | var_declaration
  '''
  if len(p) == 2:
    _ast.append(p[1])
  else:
    _ast.append(p[2])

def p_var_declaration(p):
  '''
  var_declaration : VAR_DECL ID TYPE_DECL type NEWLINE
                  | VARS_DECL var_list TYPE_DECL type NEWLINE
  '''
  if isinstance(p[2], list):
    declarations = Node()
    for name in p[2]:
      declarations.append(Declare(name, p[4]))
    p[0] = declarations
  else:
    declaration = Declare(p[2], p[4])
    p[0] = Node(declaration)

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
  p[0] = [p[1]]

def p_var(p):
  '''
  var : ID
  '''
  p[0] = Variable(p[1])

def p_type(p):
  '''
  type : TYPE_BOOLEAN
       | TYPE_FLOAT
       | TYPE_INTEGER
       | TYPE_STRING
  '''
  p[0] = p[1]

def p_statements(p):
  '''
  statements : statements statement
             | statement
  '''
  if len(p) == 2:
    p[0] = Node(p[1])
  else:
    p[1].append(p[2])
    p[0] = p[1]

def p_statement(p):
  '''
  statement : var_assignment
            | if_block
            | PRINT sequence NEWLINE
            | READ ID NEWLINE
  '''
  if p[1] == 'Ecrire':
    p[0] = Node(Print(p[2]))
  elif p[1] == 'Lire':
    p[0] = Node(Read(p[2]))
  else:
    p[0] = Node(p[1])

def p_var_assignment(p):
  '''
  var_assignment : ID ARROW expression NEWLINE
  '''
  assignment = Assign(p[1], p[3])
  p[0] = Node(assignment)

def p_if_block(p):
  '''
  if_block : IF expression THEN NEWLINE statements else_blocks
  '''

def p_else_blocks(p):
  '''
  else_blocks : else_if_block
              | else_block
              | ENDIF NEWLINE

  '''

def p_else_if_block(p):
  '''
  else_if_block : ELSIF expression THEN NEWLINE statements else_blocks
  '''

def p_else_block(p):
  '''
  else_block : ELSE NEWLINE statements ENDIF NEWLINE
  '''

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
  if not isinstance(a, Number) or not isinstance(b, Number):
    raise BadType('type Entier ou Numérique attendu')
  # Return an Integer if both value are int.
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

  # if not isinstance(a, String) or not isinstance(b, String):
  #   print(type(a), (type(b)))
  #   raise BadType('type Chaîne attendu')

  p[0] = BinOp(p[2], a, b)

def p_expression_not(p):
  '''
  expression : NOT LPAREN expression RPAREN
  '''
  a = p[3]

  p[0] = BinOp(p[1], a, None)

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
    value = p.value.replace('\n', '↵')
    print(f'*** erreur de syntaxe >> {value} <<')
    print(f'-v- ligne {p.lineno}')
    print(f'->- position {p.lexpos+1}')
  else:
    print('*** fin de fichier prématurée.')

parser = yacc()
