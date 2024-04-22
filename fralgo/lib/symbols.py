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

class Symbols:
  __func      = 'functions'
  __vars      = 'variables'
  __local     = 'local'
  __refs      =  'refs'
  __localrefs = 'localrefs'
  __localfunc = 'localfunctions'

  table = {
    __func      : {},
    __vars      : {},
    __localrefs : [],
    __local     : [],
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
  def get_localrefs_table(self):
    table = self.table[self.__localrefs]
    return table[-1]
  def get_localfunc_table(self):
    table = self.table[self.__localfunc]
    return table[-1]
  def get_variables(self):
    if self.is_local():
      return self.get_local_table()
    return self.table[self.__vars]
  def declare_var(self, name, data_type):
    variables = self.get_variables()
    if variables.get(name, None) is not None:
      raise ex.VarRedeclared(f'Redéclaration de la variable >{name}<')
    datatype = get_type(data_type)
    if is_structure(data_type):
      structure = get_structure(data_type)
      variables[name] = StructureData(structure)
    else:
      variables[name] = datatype(None)
  def declare_ref(self, name, var):
    refs = self.get_localrefs_table()
    if refs.get(name, None) is not None:
      raise ex.VarRedeclared(f'Redéclaration de la référence >{name}<')
    refs[name] = var
  def declare_array(self, name, data_type, *max_indexes):
    if self.is_local():
      variables = self.get_local_table()
    else:
      variables = self.table[self.__vars]
    if variables.get(name, None) is not None:
      raise ex.VarRedeclared((f'Redéclaration de la variable >{name}<'))
    variables[name] = Array(data_type, *max_indexes)
  def declare_sized_char(self, name, size):
    if self.is_local():
      variables = self.get_local_table()
    else:
      variables = self.table[self.__vars]
    if variables.get(name, None) is not None:
      raise ex.VarRedeclared(f'Redéclaration de la variable >{name}<')
    variables[name] = Char(None, size)
  def assign_value(self, name, value):
    var = self.get_variable(name)
    if isinstance(value, Array):
      var.set_array(value)
    else:
      var.set_value(value)
  def get_variable(self, name):
    if self.is_local():
      for variables in reversed(self.table[self.__local]):
        if name in variables:
          return variables[name]
      for references in reversed(self.table[self.__localrefs]):
        if name in references:
          var = references[name]
          return self.get_variable(var.name)
    var = self.table[self.__vars].get(name, None)
    if var is None:
      raise ex.VarUndeclared(f'Variable >{name}< non déclarée')
    return var

  # def is_variable_structure(self, name):
    # var = self.get_variable(name)
    # return is_structure(var.data_type)
  def declare_function(self, function):
    if self.is_local_function():
      self.get_localfunc_table()[function.name] = function
    else:
      self.table[self.__func][function.name] = function
  def get_function(self, name):
    if self.is_local_function():
      for functions in reversed(self.table[self.__localfunc]):
        if name in functions:
          return functions[name]
    function = self.table[self.__func].get(name, None)
    if function is None:
      raise ex.VarUndeclared(f'Fonction >{name}< non déclarée')
    return function
  def set_local(self):
    self.table[self.__local].append({})
    self.table[self.__localrefs].append({})
    self.table[self.__localfunc].append({})
  def del_local(self):
    if self.table[self.__local]:
      self.table[self.__local].pop()
    if self.table[self.__localrefs]:
      self.table[self.__localrefs].pop()
    if self.table[self.__localfunc]:
      self.table[self.__localfunc].pop()
  def del_variable(self, name):
    try:
      self.table[self.__vars].pop(name)
    except KeyError:
      raise ex.VarUndeclared(f'Variable >{name}< non déclarée')
  def reset(self):
    self.table[self.__func].clear()
    self.table[self.__local].clear()
    self.table[self.__vars].clear()
    self.table[self.__localrefs].clear()
    self.table[self.__localfunc].clear()

def declare_structure(structure):
  if __structures.get(structure.name, None) is not None:
    raise ex.VarRedeclared(f'Redéclaration de la structure >{structure.name}<')
  __structures[structure.name] = structure
