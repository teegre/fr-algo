
from lib.ast import Node, Declare, Assign, Print, Read, If
import lexer as lex
from ply.yacc import yacc

tokens = lex.tokens

precedence = (
    ('left', 'EQ', 'GT', 'LT', 'GE', 'LE'),
    ('left', 'PLUS, MINUS'),
    ('left', 'MUL', 'DIV'),
    ('left', 'POWER'),
    ('right', 'UMINUS')
)

# GRAMMAR

root = Node()

def p_program(p):
  '''
  program : START NEWLINE statements END
          | var_declarations START NEWLINE statements END
  '''
  if len(p) == 5:
    root.append(p[3])
  else:
    root.append(p[4])
  p[0] = root

def p_var_declarations(p):
  '''
  var_declarations : var_declarations var_declaration
                   | var_declaration
  '''
  if len(p) == 2:
    root.append(p[1])
  else:
    root.append(p[1] + p[2])

def p_var_declaration(p):
  '''
  var_declaration : VAR_DECL ID TYPE_DECL type NEWLINE
                  | VARS_DECL var_list TYPE_DECL type NEWLINE
  '''

def p_var_list(p):
  '''
  var_list : var_list COMMA var
           | var
  '''

def p_var(p):
  '''
  var : ID
  '''

def p_type(p):
  '''
  type : TYPE_BOOLEAN
       | TYPE_FLOAT
       | TYPE_INTEGER
       | TYPE_STRING
  '''

def p_statements(p):
  '''
  statements : statements statement
             | statement
  '''

def p_statement(p):
  '''
  statement : var_assignment
            | if_block
            | PRINT sequence NEWLINE
            | READ ID NEWLINE
  '''

def p_var_assignment(p):
  '''
  var_assignment : ID ARROW expression NEWLINE
  '''

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

def p_element(p):
  '''
  element : expression
  '''

def p_expression(p):
  '''
  expression : BOOL_TRUE
             | BOOL_FALSE
             | FLOAT
             | INTEGER
             | STRING
             | var
  '''

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

def p_expression_not(p):
  '''
  expression : NOT LPAREN expression RPAREN
  '''

def p_expression_group(p):
  '''
  expression : LPAREN expression RPAREN
  '''
def p_expression_uminus(p):
  '''
  expression : MINUS expression %prec UMINUS
  '''
