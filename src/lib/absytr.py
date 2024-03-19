'''Abstract syntax tree kinda'''
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
from lib.datatypes import Boolean, Float, Integer, String
from lib.symbols import get_variable, is_variable
from lib.exceptions import BadType, InterruptedByUser

class Statements:
  '''
  Program statements.
  Statements are added to a list and can be evaluated once
  the program has been parsed.
  '''
  def __init__(self, value):
    if value is None:
      self.children = []
    else:
      self.children = [value]
  def eval(self):
    '''Evaluate all statements in the list.'''
    for statement in self:
      statement.eval()
  def append(self, value):
    '''Add a statement to the list.'''
    if value is not None:
      self.children.append(value)
  def __getitem__(self, index):
    return self.children[index]
  def __iter__(self):
    return iter(self.children)
  def __len__(self):
    return len(self.children)
  def __repr__(self):
    return f'{self.children}'

class Print:
  '''Print statement. Display one or several elements'''
  def __init__(self, data):
    self.data = data
  def eval(self):
    '''Print data'''
    result = []
    for element in self.data:
      if isinstance(element, Boolean):
        result.append(str(element))
      else:
        result.append(str(map_type(element).eval()))
    print(''.join(result))
  def __repr__(self):
    return f'Ecrire {self.data}'

class Read:
  '''Read user input and assign value to a variable...'''
  def __init__(self, var):
    self.var = var
  def eval(self):
    '''... on evaluation'''
    try:
      user_input = input()
      var = get_variable(self.var)
    except KeyboardInterrupt as e:
      raise InterruptedByUser("interrompu par l'utilisateur") from e
    try:
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

class Negative:
  def __init__(self, value):
    if isinstance(value, (Integer, Float)):
      self.value = map_type(-value.eval())
    elif is_variable(value):
      print('variable', value)
      var = get_variable(value)
      self.value = map_type(-var.eval())
      print(self.value)
    else:
      raise BadType(f'{self.value} ne peut pas être négatif.')
  def eval(self):
    return self.value
  def __repr__(self):
    return self.value.__repr__()

class Binop:
  __op = {
      '+'  : operator.add,
      '-'  : operator.sub,
      '*'  : operator.mul,
      '/'  : operator.truediv,
      '//' : operator.floordiv,
      'dp' : 'dummy',
      '^'  : operator.pow,
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
      return a.eval() % b.eval() == 0
    return op(a.eval(), b.eval())
  def __repr__(self):
    return f'{self.a} {self.op} {self.b}'
