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

import lib.exceptions as ex
from lib.datatypes import Boolean, Float, Integer, String

__variables = {}

def declare_var(name, data_type):
  if __variables.get(name, None) is not None:
    raise ex.VarRedeclared(f'redéclaration de la variable {name}')
  if data_type == 'Booléen':
    __variables[name] = Boolean(None)
  elif data_type == 'Chaîne':
    __variables[name] = String(None)
  elif data_type == 'Numérique':
    __variables[name] = Float(None)
  elif data_type == 'Entier':
    __variables[name] = Integer(None)

def assign_value(name, value):
  var = get_variable(name)
  var.set_value(value)

def get_variable(name):
  var = __variables.get(name, None)
  if var is None:
    raise ex.VarUndeclared(f'variable {name} non déclarée')
  return var

def is_variable(name):
  return __variables.get(name, False) is not False

def get_type(name):
  var = get_variable(name)
  return  var.data_type

def delete_variable(name):
  __variables.pop(name)

def reset_variables():
  __variables.clear()
