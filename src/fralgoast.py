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

import fralgoexception as ex

__variables = {}

types = ('Booléen', 'Chaîne', 'Entier', 'Numérique')

class Variable():
  def __init__(self, name, var_type):
    self.name = name
    self.type = var_type
    self.value = None
  def eval(self):
    return self.value
  def __repr__(self):
    if self.value:
      return f'{self.name} = {self.value}'
    return f'{self.name} en {self.type}'

def declare_var(name, var_type):
  if name in __variables.keys():
    raise ex.VarRedeclared(f'redéclaration de la variable {name}')
  var = Variable(name, var_type)
  __variables[name] = var

def get_var_type(name):
  return __variables[name].type

def assign_value(name, value):
  if name not in __variables.keys():
    raise ex.VarUndeclared(f'variable {name} non déclarée')

  var_type = get_var_type(name)
  if isinstance(value, bool) and var_type != 'Booléen':
    raise ex.BadType(f'type {var_type} attendu pour la variable {name}')
  if isinstance(value, int) and not isinstance(value, bool) and var_type != 'Entier':
    raise ex.BadType(f'type {var_type} attendu pour la variable {name}')
  if isinstance(value, float) and var_type != 'Numérique':
    raise ex.BadType(f'type {var_type} attendu pour la variable {name}')
  if isinstance(value, str) and var_type != 'Chaîne':
    raise ex.BadType(f'type {var_type} attendu pour la variable {name}')

  __variables[name].value = value

def get_variable(name):
  return __variables.get(name, None)

def show_variables():
  for k, v in __variables:
    print(f'{k}: {v.type}')
