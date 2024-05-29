'''Symbols'''
#  _______ ______        _______ _____   _______ _______
# |    ___|   __ \______|   _   |     |_|     __|       |
# |    ___|      <______|       |       |    |  |   -   |
# |___|   |___|__|      |___|___|_______|_______|_______|
#
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
from fralgo.lib.datatypes import Array, Char, StructureData, Table

class Symbols:
  __func         = 'functions'
  __vars         = 'variables'
  __structs      = 'structures'
  __local        = 'local'
  __localfunc    = 'localfunctions'
  __localstructs = 'localstructs'

  __superglobal  = {}
  __localrefs    = []

# TODO: ORDER METHODS

  def __init__(self, get_type_func, namespace=None):
    self.table = {
      self.__func         : {},
      self.__vars         : {},
      self.__structs      : {},
      # self.__localrefs    : [],
      self.__local        : [],
      self.__localfunc    : [],
      self.__localstructs : [],
    }
    self.get_type = get_type_func
    self.namespace = namespace
  def is_structure(self, name):
    if self.is_local_structure():
      table = self.table[self.__localstructs]
      for structs in reversed(table):
        if structs.get(name, None) is not None:
          return True
      return False
    struct = self.table[self.__structs].get(name, None)
    return struct is not None
  def is_local(self):
    return bool(self.table[self.__local])
  def is_local_function(self):
    return bool(self.table[self.__localfunc])
  def is_local_structure(self):
    return bool(self.table[self.__localstructs])
  def get_local_table(self):
    table = self.table[self.__local]
    return table[-1]
  def get_localrefs_table(self):
    table = self.__localrefs
    return table[-1]
  def get_localfunc_table(self):
    table = self.table[self.__localfunc]
    return table[-1]
  def get_localstructs_table(self):
    table = self.table[self.__localstructs]
    return table[-1]
  def get_variables(self):
    if self.is_local():
      return self.get_local_table()
    return self.table[self.__vars]
  def get_structures(self):
    if self.is_local_structure():
      return self.get_localstructs_table()
    return self.table[self.__structs]
  def declare_var(self, name, data_type, superglobal=False):
    if superglobal:
      variables = self.__superglobal
    else:
      variables = self.get_variables()
    if variables.get(name, None) is not None:
      raise ex.VarRedeclared(f'Redéclaration de la variable >{name}<')
    datatype = self.get_type(data_type, self.get_structure)
    if self.is_structure(data_type):
      structure = self.get_structure(data_type)
      data = StructureData(structure)
      data.set_get_structure(self.get_structure)
      data.data = data.new_structure_data()
      variables[name] = data
    else:
      variables[name] = datatype(None)
  def declare_ref(self, name, var):
    refs = self.get_localrefs_table()
    if refs.get(name, None) is not None:
      raise ex.VarRedeclared(f'Redéclaration de la référence >{name}<')
    refs[name] = var
  def declare_array(self, name, data_type, *max_indexes, superglobal=False):
    if superglobal:
      variables = self.__superglobal
    elif self.is_local():
      variables = self.get_local_table()
    else:
      variables = self.table[self.__vars]
    if variables.get(name, None) is not None:
      raise ex.VarRedeclared((f'Redéclaration de la variable >{name}<'))
    array = Array(data_type, *max_indexes)
    array.set_get_structure(self.get_structure)
    array.value = array.new_array(*array.sizes)
    variables[name] = array
  def declare_table(self, name, key_type, value_type):
    if self.is_local():
      variables = self.get_local_table()
    else:
      variables = self.table[self.__vars]
    if variables.get(name, None) is not None:
      raise ex.VarRedeclared(f'Redéclaration de la variable {name}')
    variables[name] = Table(key_type, value_type)
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
  def get_variable(self, name, visited=None):
    if self.is_local():
      if visited is None:
        visited = set()
      elif name in visited:
        return None
      for references in reversed(self.__localrefs):
        if name in references:
          visited.add(name)
          var = references[name]
          if var.namespace != self.namespace and self.namespace is not None:
            return var.eval()
          resolved = self.get_variable(var.name, visited)
          if resolved is not None:
            return resolved
      for variables in reversed(self.table[self.__local]):
        if name in variables:
          return variables[name]
    var = self.table[self.__vars].get(name, None)
    if var is None:
      var = self.__superglobal.get(name, None)
      if var is not None:
        return var
      raise ex.VarUndeclared(f'Variable >{name}< non déclarée')
    return var
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
  def declare_structure(self, structure):
    structs = self.get_structures()
    if structs.get(structure.name, None) is not None:
      raise ex.VarRedeclared(f'Redéclaration de la structure >{structure.name}<')
    structs[structure.name] = structure
  def get_structure(self, name):
    if self.is_local_structure():
      for structs in reversed(self.table[self.__localstructs]):
        if name in structs:
          return structs[name]
    struct = self.table[self.__structs].get(name, None)
    if struct is None:
      raise ex.VarRedeclared(f'Structure >{name}< non déclarée')
    return struct
  def set_local(self):
    self.table[self.__local].append({})
    self.__localrefs.append({})
    self.table[self.__localfunc].append({})
    self.table[self.__localstructs].append({})
  def del_local(self):
    if self.table[self.__local]:
      self.table[self.__local].pop()
    if self.__localrefs:
      self.__localrefs.pop()
    if self.table[self.__localfunc]:
      self.table[self.__localfunc].pop()
    if self.table[self.__localstructs]:
      self.table[self.__localstructs].pop()
  def del_variable(self, name):
    try:
      self.table[self.__vars].pop(name)
    except KeyError:
      raise ex.VarUndeclared(f'Variable >{name}< non déclarée')
  def reset(self):
    self.table[self.__func].clear()
    self.table[self.__local].clear()
    self.table[self.__vars].clear()
    self.table[self.__structs].clear()
    self.__localrefs.clear()
    self.table[self.__localfunc].clear()
    self.table[self.__localstructs].clear()
  def dump(self):
    print('*** global variables')
    for k in self.table[self.__vars].keys():
      print(k)
    print('---')
    print('*** functions')
    for k in self.table[self.__func].keys():
      print(k)
    print('---')
    print('*** refs')
    for refs in self.__localrefs:
      for k in refs:
        print(k)
    print('---')
  def __repr__(self):
    return f'Espace-nom {self.namespace}'

class Namespaces:
  def __init__(self, get_type):
    self.ns = {}
    self.get_type = get_type
    # init main namespace
    self.ns['main'] = Symbols(get_type_func=get_type)
    self.current_namespace = 'main'
  def set_current_namespace(self, name):
    self.current_namespace = name
  def declare_namespace(self, name):
    if name in self.ns:
      raise ex.VarRedeclared(f"Redéclaration de l'espace-nom '{name}'")
    self.ns[name] = Symbols(self.get_type, name)
    self.current_namespace = name
  def get_namespace(self, name):
    if not name:
      nm = self.current_namespace
    else:
      nm = name
    if nm in self.ns:
      return self.ns[nm]
    raise ex.VarUndeclared(f'Espace-nom \'{nm}\' non déclaré')
  def declare_ref(self, name, var, namespace):
    sym = self.get_namespace(namespace)
    sym.declare_ref(name, var)
  def get_variable(self, name, namespace):
    sym = self.get_namespace(namespace)
    return sym.get_variable(name)
  def get_function(self, name, namespace):
    sym = self.get_namespace(namespace)
    return sym.get_function(name)
  def get_structure(self, name, namespace):
    sym = self.get_namespace(namespace)
    return sym.get_structure(name)
  def set_local(self, namespace):
    sym = self.get_namespace(namespace)
    return sym.set_local()
  def del_local(self, namespace):
    sym = self.get_namespace(namespace)
    return sym.del_local()
  def reset(self):
    for _, symbols in self.ns.items():
      symbols.reset()
    self.ns.clear()
    self.ns['main'] = Symbols(self.get_type, 'main')
    self.current_namespace = 'main'
