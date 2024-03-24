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

import operator
from lib.datatypes import map_type
from lib.datatypes import Array, Boolean, Number, Float, Integer, String
from lib.symbols import declare_array, declare_var, get_variable, get_type, assign_value
from lib.exceptions import FralgoException, BadType, InterruptedByUser, VarUndeclared

class Node:
  def __init__(self, statement=None, lineno=0):
    self.children = [statement] if statement else []
    self.lineno = lineno
  def append(self, statement):
    if statement is not None:
      self.children.append(statement)
  def eval(self):
    for statement in self.children:
      try:
        statement.eval()
      except FralgoException as e:
        print('***', e.message)
        print('-v-', f'ligne {self.lineno}')
        break
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
  def __init__(self, data):
    self.data = data
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
    print(' '.join(result))
  def __repr__(self):
    return f'Ecrire {self.data}'

class Read:
  '''Read user input and assign value to a variable...'''
  def __init__(self, var):
    self.var = var
  def eval(self):
    '''... on evaluation'''
    var_type = get_type(self.var)
    try:
      user_input = input(f'({self.var} ← {var_type[0]}) : ')
    except KeyboardInterrupt as e:
      raise InterruptedByUser("interrompu par l'utilisateur") from e
    try:
      var = get_variable(self.var)
      if isinstance(var, Integer):
        var.set_value(int(user_input))
      elif isinstance(var, Float):
        var.set_value(float(user_input))
      elif isinstance(var, String):
        var.set_value(user_input)
    except ValueError as e:
      raise BadType(f'type {var.data_type} attendu') from e
  def __repr__(self):
    return f'Lire {self.var}'

class BinOp:
  __op = {
      '+'   : operator.add,
      '-'   : operator.sub,
      '*'   : operator.mul,
      '/'   : operator.truediv,
      '//'  : operator.floordiv,
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
    if self.op == 'dp':
      return map_type(a.eval() % b.eval() == 0)
    if self.op == '&':
      # evaluate expressions until we get a str.
      while isinstance(a, (String, BinOp, Variable)):
        a = a.eval()
      while isinstance(b, (String, BinOp, Variable)):
        b = b.eval()
      if isinstance(a, str) and isinstance(b, str):
        return a + b
      raise BadType('type Chaîne attendu')
    if self.b is None:
      return op(a.eval())
    return op(a.eval(), b.eval())
    # return map_type(op(a.eval(), b.eval()))
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
      raise BadType('type Entier ou Numérique attendu')
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
      for statement in self.dothis:
        statement.eval()
  def __repr__(self):
    return f'TantQue {self.condition} → {self.dothis}'

class For:
  def __init__(self, v, b, e, dt, nv, s=Integer(1)):
    # if v != nv:
    #   raise ForLoopVariablesNotMatching(f'{v} ne correspond pas à {nv}')
    self.var = v.name
    self.start = b.eval()
    self.end = e.eval()
    self.step = s.eval()
    self.dothis = dt
  def eval(self):
    i = self.start
    end = self.end
    assign_value(self.var, i)
    while i <= end if self.step > 0 else i >= end:
      for statement in self.dothis:
        statement.eval()
      i += self.step
      assign_value(self.var, i)
  def __repr__(self):
    return f'Pour {self.var} ← {self.start} à {self.end}'
