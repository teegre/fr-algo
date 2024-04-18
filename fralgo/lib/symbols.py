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

import fralgo.lib.exceptions as ex
from fralgo.lib.datatypes import Array, Char
from fralgo.lib.datatypes import StructureData
from fralgo.lib.datatypes import __structures
from fralgo.lib.datatypes import get_structure, is_structure, get_type

__variables = {}
__functions = {}
__localvars = []

class Symbols:
  __func      = 'functions'
  __vars      = 'variables'
  __local     = 'local'
  __localfunc = 'localfunctions'

  table = {
    __func      : {},
    __vars      : {},
    __local     : {},
    __localfunc : [],
  }

  def is_variable(self, name):
    return name in self.table[self.__vars].keys()
  def is_local(self):
    return len(self.table[self.__local]) > 0
  def is_local_function(self):
    return len(self.table[self.__localfunc]) > 0
  def get_local_table(self):
    table = self.table[self.__local]
    return table[-1]
  def get_localfunc_table(self):
    table = self.table[self.__localfunc]
    return table[-1]

def declare_var(name, data_type):
  if is_local():
    variables = __localvars[-1]
  else:
    variables = __variables
  if variables.get(name, None) is not None:
    raise ex.VarRedeclared(f'Redéclaration de la variable >{name}<')
  datatype = get_type(data_type)
  if is_structure(data_type):
    structure = get_structure(data_type)
    variables[name] = StructureData(structure)
  else:
    variables[name] = datatype(None)

def declare_array(name, data_type, *max_indexes):
  if is_local():
    variables = __localvars[-1]
  else:
    variables = __variables
  if variables.get(name, None) is not None:
    raise ex.VarRedeclared((f'Redéclaration de la variable >{name}<'))
  variables[name] = Array(data_type, *max_indexes)

def declare_sized_char(name, size):
  if is_local():
    variables = __localvars[-1]
  else:
    variables = __variables
  if variables.get(name, None) is not None:
    raise ex.VarRedeclared(f'Redéclaration de la variable >{name}<')
  variables[name] = Char(None, size)

def declare_structure(structure):
  if __structures.get(structure.name, None) is not None:
    raise ex.VarRedeclared(f'Redéclaration de la structure >{structure.name}<')
  __structures[structure.name] = structure

def assign_value(name, value):
  # print('assign', name, value, 'local:', is_local())
  var = get_variable(name)
  var.set_value(value)

def get_variable(name, is_global=False):
  if is_local() and not is_global:
    variables = __localvars[-1]
  else:
    variables = __variables
  var = variables.get(name, None)
  if var is None:
    # print(__variables)
    # print(__localvars)
    raise ex.VarUndeclared(f'Variable >{name}< non déclarée')
  return var

def is_variable(name):
  if is_local():
    variables = __localvars[-1]
  else:
    variables = __variables
  return variables.get(name, False) is not False

def is_variable_structure(name):
  var = get_variable(name)
  return is_structure(var.data_type)

def declare_function(function):
  __functions[function.name] = function

def get_function(name):
  function = __functions.get(name, None)
  if function is None:
    raise ex.VarUndeclared(f'Fonction {name} non déclarée')
  return function

def set_local():
  # print('local')
  __localvars.append({})

def is_local():
  return len(__localvars) > 0

def reset_local():
  # print('reset', __localvars)
  if is_local():
    __localvars.pop()

def delete_variable(name):
  __variables.pop(name)

def reset_variables():
  __variables.clear()
  reset_local()
