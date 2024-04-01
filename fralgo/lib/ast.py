'''Abstract syntax tree'''
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
import operator
from fralgo.lib.datatypes import map_type
from fralgo.lib.datatypes import Array, Boolean, Number, Float, Integer, String
from fralgo.lib.symbols import declare_array, declare_var, get_variable, assign_value
from fralgo.lib.exceptions import FralgoException, BadType, InterruptedByUser, VarUndeclared
from fralgo.lib.exceptions import FatalError, ZeroDivide

class Node:
  def __init__(self, statement=None, lineno=0):
    self.children = [statement] if statement else []
    self.lineno = lineno
  def append(self, statement):
    if statement is not None:
      self.children.append(statement)
  def eval(self):
    result = None
    for statement in self.children:
      try:
        result = statement.eval()
      except FatalError as e:
        print(f'*** {e.message}')
      except FralgoException as e:
        print('***', e.message)
        if 'FRALGOREPL' not in os.environ:
          print(f'-v- Ligne {self.lineno}')
          print('*** Erreur fatale')
          sys.exit(666)
        return None
    return result
  def __getitem__(self, start=0, end=0):
    return self.children[start:end] if end != 0 else self.children[start]
  def __iter__(self):
    return iter(self.children)
  def __str__(self):
    statements = []
    for statement in self:
      statements.append(str(statement))
    return '\n'.join(statements)
  def __repr__(self):
    return f'Node({self.lineno}) {self.children}'

class Declare:
  def __init__(self, name, var_type):
    self.name = name
    self.var_type = var_type
  def eval(self):
    declare_var(self.name, self.var_type)
  def __repr__(self):
    return f'Variable {self.name} en {self.var_type}'

class DeclareArray:
  def __init__(self, name, var_type, *max_indexes):
    self.name = name
    self.var_type = var_type
    self.max_indexes = max_indexes
  def eval(self):
    declare_array(self.name, self.var_type, *self.max_indexes)
  def __repr__(self):
    indexes = [str(n) for n in self.max_indexes]
    idx = ', '.join(indexes)
    if idx == '-1':
      idx = ''
    return f'Tableau {self.name}[{idx}] en {self.var_type}'

class ArrayGetItem:
  def __init__(self, var, *indexes):
    self.var = var
    self.indexes = indexes
  def eval(self):
    var = self.var.eval()
    return var.get_item(*self.indexes)
  def __repr__(self):
    indexes = [str(index.eval()) for index in self.indexes]
    return f'{self.var.name}[{", ".join(indexes)}]'

class ArraySetItem:
  def __init__(self, var, value, *indexes):
    self.var = var
    self.value = value
    self.indexes = indexes
  def eval(self):
    var = self.var.eval()
    var.set_value(self.indexes, self.value)
  def __repr__(self):
    indexes = (str(index) for index in self.indexes)
    return f'{self.var.name}[{", ".join(indexes)}] ← {self.value}'

class ArrayResize:
  def __init__(self, var, *indexes):
    self.var = var
    self.indexes = indexes
  def eval(self):
    var = self.var.eval()
    var.resize(*self.indexes)
  def __repr__(self):
    indexes = (str(index) for index in self.indexes)
    return f'Redim {self.var.name}[{", ".join(indexes)}]'

class Assign:
  def __init__(self, var, value):
    self.var = var
    self.value = value
  def eval(self):
    assign_value(self.var, self.value.eval())
  def __repr__(self):
    return f'{self.var} ← {self.value}'

class Variable:
  def __init__(self, name):
    self.name = name
  def eval(self):
    var = get_variable(self.name)
    if isinstance(var, (Boolean, Number, String)):
      return var.eval()
    return var
  def __repr__(self):
    try:
      value = get_variable(self.name)
      return f'{self.name} → {value}'
    except VarUndeclared:
      return f'{self.name} → ?'

class Print:
  '''Print statement. Display one or several elements'''
  def __init__(self, data, newline=True):
    self.data = data
    self.newline = newline
  def eval(self):
    '''Print data'''
    result = []
    for element in self.data:
      if isinstance(element, (BinOp, Variable)):
        if isinstance(element.eval(), bool):
          # special treatment for bool type...
          # we want to print VRAI or FAUX
          # instead of True or False
          result.append(str(map_type(element.eval())))
          continue
      # here we want to use the str method of the evaluated class.
      result.append(str(element.eval()))
    if self.newline:
      print(' '.join(result))
    else:
      print(' '.join(result), end='')
  def __repr__(self):
    return f'Ecrire {self.data}'

class Read:
  '''
  Read user input and assign value to a variable...
  '''
  def __init__(self, var, *args):
    self.var = var
    self.args = args
  def eval(self):
    '''... on evaluation'''
    try:
      user_input = input()
    except (KeyboardInterrupt, EOFError):
      print()
      raise InterruptedByUser('Interrompu par l\'utilisateur')
    try:
      var = get_variable(self.var)
      if isinstance(var, Boolean):
        var.set_value(Boolean(user_input).eval())
      if isinstance(var, Integer):
        var.set_value(int(user_input))
      elif isinstance(var, Float):
        var.set_value(float(user_input))
      elif isinstance(var, String):
        var.set_value(user_input)
      elif isinstance(var, Array):
        match var.datatype:
          case 'Booléen':
            var.set_value(self.args, Boolean(user_input))
          case 'Chaîne':
            var.set_value(self.args, String(user_input))
          case 'Entier':
            var.set_value(self.args, Integer(int(user_input)))
          case 'Numérique':
            var.set_value(self.args, Float(float(user_input)))
    except ValueError:
      raise BadType(f'Type {var.data_type} attendu')
  def __repr__(self):
    return f'Lire {self.var}'

class BinOp:
  __op = {
      '+'   : operator.add,
      '-'   : operator.sub,
      '*'   : operator.mul,
      '/'   : 'dummy',
      '%'   : operator.mod,
      'dp'  : 'dummy',
      '^'   : operator.pow,
      '&'   : 'dummy',
      '='   : operator.eq,
      '>'   : operator.gt,
      '<'   : operator.lt,
      '>='  : operator.ge,
      '<='  : operator.le,
      '<>'  : operator.ne,
      'ET'  : operator.and_,
      'OU'  : operator.or_,
      'XOR' : operator.xor,
      'NON' : operator.not_,
  }
  def __init__(self, op, a, b):
    self.a = a
    self.b = b
    self.op = op
  def eval(self):
    a = self.a
    b = self.b
    op = self.__op.get(self.op, None)
    types = (ArrayGetItem, BinOp, Boolean, Neg, Number, String, Variable, Mid, Len, Trim)
    while isinstance(a, types):
      a = a.eval()
    while isinstance(b, types):
      b = b.eval()
    if self.op == '/':
      if not isinstance(a, (int, float)) and not isinstance(b, (int, float)):
        raise BadType('E|N/E|N : Type Entier ou Numérique attendu')
      if isinstance(a, int) and isinstance(b, int):
        if b == 0:
          raise ZeroDivide('Division par zéro')
        op = operator.floordiv
      elif isinstance(a, float) or isinstance(b, float):
        if b == 0:
          raise ZeroDivide('Division par zéro')
        op = operator.truediv
    if self.op == 'dp':
      return map_type(a % b == 0)
    if self.op == '&':
      # evaluate expressions until we get a str.
      if isinstance(a, str) and isinstance(b, str):
        return a + b
      raise BadType('C & C : Type Chaîne attendu')
    if self.b is None:
      return op(a)
    return op(a, b)
  def __repr__(self):
    if self.b is None:
      return f'{self.op} {self.a}'
    return f'{self.a} {self.op} {self.b}'

class Neg:
  def __init__(self, value):
    self.value = value
  def eval(self):
    value = self.value.eval()
    if not isinstance(value, (int, float)):
      raise BadType('-E|N : Type Entier ou Numérique attendu')
    return -value
  def __repr__(self):
    return f'-{self.value}'

class If:
  def __init__(self, condition, dothis, dothat):
    self.condition = condition
    self.dothis = dothis
    self.dothat = dothat
  def eval(self):
    if self.condition.eval():
      for statement in self.dothis:
        statement.eval()
    elif self.dothat is not None:
      self.dothat.eval()
  def __repr__(self):
    if self.dothat is not None:
      return f'Si {self.condition} Alors {self.dothis} Sinon {self.dothat}'
    return f'Si {self.condition} Alors {self.dothis}'

class While:
  def __init__(self, condition, dothis):
    self.condition = condition
    self.dothis = dothis
  def eval(self):
    while self.condition.eval():
      try:
        for statement in self.dothis:
          statement.eval()
      except KeyboardInterrupt:
        raise InterruptedByUser('Interrompu par l\'utilisateur')
      except FralgoException as e:
        raise e
  def __repr__(self):
    return f'TantQue {self.condition} → {self.dothis}'

class For:
  def __init__(self, v, b, e, dt, nv, s=Integer(1)):
    self.var = v.name
    self.start = b
    self.end = e
    self.step = s
    self.dothis = dt
    self.var_next = nv.name
  def eval(self):
    if self.var != self.var_next:
      raise FralgoException(f'Pour >>{self.var}<< ... >>{self.var_next}<< Suivant')
    i = self.start.eval()
    end = self.end.eval()
    step = self.step.eval()
    assign_value(self.var, i)
    while i <= end if step > 0 else i >= end:
      try:
        for statement in self.dothis:
          statement.eval()
      except FralgoException as e:
        raise e
      except KeyboardInterrupt:
        raise InterruptedByUser('Interrompu par l\'utilisateur')
      i += step
      assign_value(self.var, i)
  def __repr__(self):
    return f'Pour {self.var} ← {self.start} à {self.end} → {self.dothis}'

class Len:
  def __init__(self, value):
    self.value = value
  def eval(self):
    try:
      return len(self.value.eval())
    except TypeError:
      raise BadType('Longueur(>C<) : Type Chaîne attendu')
  def __repr__(self):
    return f'Longueur({self.value})'

class Mid:
  def __init__(self, exp, start, length):
    self.exp = exp
    self.start = start
    self.length = length
  def eval(self):
    exp = self.exp.eval()
    start = self.start.eval()
    length = self.length.eval()
    if not isinstance(exp, str):
      raise BadType('Extraire(>C<, E, E) : Type Chaîne attendu')
    if not isinstance(start, int):
      raise BadType('Extraire(C, >E<, E) : Type Entier attendu')
    if not isinstance(length, int):
      raise BadType('Extraire(C, E, >E<) : Type Entier attendu')
    return exp[start-1:start-1+length]
  def __repr__(self):
    return f'Extraire({self.exp, self.start, self.length})'

class Trim:
  def __init__(self, exp, length, right=False):
    self.exp = exp
    self.length = length
    self.right = right
    if right:
      self.cmd = 'Gauche'
    else:
      self.cmd = 'Droite'
  def eval(self):
    exp = self.exp.eval()
    length = self.length.eval()
    if not isinstance(exp, str):
      raise BadType(f'{self.cmd}(>C<, E) : Type Chaîne attendu')
    if not isinstance(length, int):
      raise BadType(f'{self.cmd}(C, >E<) : Type Entier attendu')
    if not self.right:
      return exp[:length]
    return exp[len(exp) - length:]
  def __repr__(self):
    return f'{self.cmd}({self.exp}, {self.length})'
