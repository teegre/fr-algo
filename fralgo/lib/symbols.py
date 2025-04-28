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

class Context:
  def __init__(self, context_name:str):
    self.name = context_name
    self.dereference = False
    self.has_reference = False
  def __repr__(self):
    return f'{self.name} [{"+" if self.dereference else "-"}]'
  def __str__(self):
    return f'{self.name} [{"+" if self.dereference else "-"}]'

class StructuresRegistry:
  __structures = {}

  @classmethod
  def register_structure(cls, namespace, name, structure):
    cls.__structures[name] = structure

  @classmethod
  def get_structure(cls, namespace,name):
    return cls.__structures.get(name)

  @classmethod
  def del_structure(cls, namespace, name):
    cls.__structures.pop(name)

  @classmethod
  def clear_structures(cls):
    cls.__structures.clear()

class Symbol:
  def __init__(self, namespace=None, datatype=None, name=None):
    self.namespace = namespace
    self.datatype = datatype
    self.name = name
  def eval(self):
    try:
      return self.name.eval()
    except AttributeError:
      return self.name
  def __repr__(self):
    ns = 'main' if self.namespace is None else self.namespace
    return f'{ns}:{self.name} ({self.datatype})'

class Symbols:
  __func         = 'functions'
  __vars         = 'variables'
  __structs      = 'structures'
  __local        = 'local'
  __localfunc    = 'localfunctions'
  __localstructs = 'localstructs'
  __context      = 'context'

  __superglobal  = {}
  __main_global  = {}
  __localrefs    = []

# TODO: ORDER METHODS

  def __init__(self, get_type_func, namespace=None):
    self.table = {
      self.__func         : {},
      self.__vars         : {},
      self.__structs      : {},
      self.__local        : [],
      self.__localfunc    : [],
      self.__localstructs : [],
      self.__context      : [],
    }
    self.get_type = get_type_func
    self.namespace = namespace

  def is_structure(self, name):
    if isinstance(name, list):
      namespace, name = name[0], name[1]
    else:
      namespace = self.namespace
    if self.is_local():
      table = self.get_localstructs_table()
      for structs in reversed(table):
        if structs.get(name, None) is not None:
          return True
    if namespace != self.namespace:
      return StructuresRegistry.get_structure(namespace, name) is not None
    struct = self.table[self.__structs].get(name, None)
    return struct is not None
  def is_local(self):
    return bool(self.table[self.__local])
  def is_local_function(self):
    return bool(self.table[self.__localfunc])
  def get_local_table(self):
    table = self.table[self.__local]
    return table[-1]
  def get_local_ref_context(self):
    table = self.table[self.__context]
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
    if self.namespace == 'main':
      return self.__main_global
    return self.table[self.__vars]
  def get_structures(self):
    if self.is_local():
      return self.get_localstructs_table()
    return self.table[self.__structs]
  def set_local_ref_context(self, dereference:bool):
    context = self.get_local_ref_context()
    context.dereference = dereference
  def set_local_ref_context_has_reference(self, has_reference:bool):
    context = self.get_local_ref_context()
    context.has_reference = has_reference
  def declare_var(self, name, data_type, superglobal=False):
    if superglobal:
      variables = self.__superglobal
    else:
      variables = self.get_variables()
    if variables.get(name, None) is not None:
      raise ex.VarRedeclared(f'Redéclaration de la variable `{name}`')
    # Beware of global variables!
    # if self.namespace == 'main' and self.__main_global.get(name, None) is not None:
    #   raise ex.VarRedeclared(f'Redéclaration de la variable `{name}`')
    datatype = self.get_type(data_type, self.get_structure)
    if isinstance(datatype, tuple): # structure!
      data = datatype[0](datatype[1])
      data.set_get_structure(self.get_structure)
      data.data = data.new_structure_data()
      variables[name] = data
    else:
      variables[name] = datatype(None)
  def declare_const(self, name, value, superglobal=False):
    if superglobal:
      variables = self.__superglobal
    else:
      variables = self.get_variables()
    if variables.get(name, None) is not None:
      raise ex.VarRedeclared(f'Redéclaration de la constante `{name}`')
    if issubclass(type(value), Array):
      indexes = Array.get_indexes(value.value)
      datatype = Array.get_datatype(value.value)
      Array.check_types(value.value, datatype)
      array = Array(datatype, *indexes)
      array.set_get_structure(self.get_structure)
      array.value = array.new_array(*array.sizes)
      array.set_array(value)
      variables[name] = ('CONST', array)
    else:
      variables[name] = ('CONST', value)
  def declare_ref(self, name, var):
    refs = self.get_localrefs_table()
    if refs.get(name, None) is not None:
      raise ex.VarRedeclared(f'Redéclaration de la référence `{name}`')
    refs[name] = var
  def declare_array(self, name, data_type, *max_indexes, superglobal=False):
    if superglobal:
      variables = self.__superglobal
    elif self.is_local():
      variables = self.get_local_table()
    else:
      variables = self.get_variables()
    if variables.get(name, None) is not None:
      raise ex.VarRedeclared((f'Redéclaration de la variable `{name}`'))
    array = Array(data_type, *max_indexes)
    array.set_get_structure(self.get_structure)
    array.value = array.new_array(*array.sizes)
    variables[name] = array
  def declare_table(self, name, key_type, value_type):
    variables = self.get_variables()
    if variables.get(name, None) is not None:
      raise ex.VarRedeclared(f'Redéclaration de la variable `{name}`')
    variables[name] = Table(key_type, value_type)
  def declare_sized_char(self, name, size):
    variables = self.get_variables()
    if variables.get(name, None) is not None:
      raise ex.VarRedeclared(f'Redéclaration de la variable `{name}`')
    variables[name] = Char(None, size)
  def assign_value(self, name, value, namespace=None):
    if name.startswith('@') and self.namespace != namespace:
      raise ex.FralgoException('Affectation d\'une valeur à un symbole privé.')
    var = self.get_variable(name)
    if isinstance(var, tuple): # constant!
      raise ex.ReadOnlyValue(f'Constante `{name}` : en lecture seule')
    elif issubclass(type(value), Array):
      var.set_array(value)
    else:
      try:
        var.set_value(value)
      except TypeError:
        raise ex.FralgoException(f'{name} ← {value} : affectation impossible')
  def get_variable(self, name, visited=None):
    if self.is_local():
      context = self.get_local_ref_context()
      if not context.has_reference:
        for variables in reversed(self.table[self.__local]):
          if name in variables:
            return variables[name]
      if context.dereference:
        if visited is None:
          visited = set()
        elif name in visited:
          return None
        visited.add(name)
        for references in reversed(self.__localrefs):
          if name in references:
            var = references[name]
            try:
              if var.namespace != self.namespace and self.namespace is not None:
                return var.eval()
            except AttributeError:
              raise ex.BadReference(f'Référence `{name}` invalide !')
            resolved = self.get_variable(var.name, visited)
            if resolved is not None:
              return resolved
      for variables in reversed(self.table[self.__local]):
        if name in variables:
          return variables[name]
    var = self.table[self.__vars].get(name, None)
    if var is None:
      var = self.__main_global.get(name, None)
      if var is not None:
        return var
      var = self.__superglobal.get(name, None)
      if var is not None:
        return var
      raise ex.VarUndeclared(f'Variable `{name}` non déclarée')
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
      raise ex.VarUndeclared(f'Fonction `{name}` non déclarée')
    return function
  def declare_structure(self, structure):
    structs = self.get_structures()
    if structs.get(structure.name, None) is not None:
      raise ex.VarRedeclared(f'Redéclaration de la structure `{structure.name}`')
    if not self.is_local():
      StructuresRegistry.register_structure(self.namespace, structure.name, structure)
    structs[structure.name] = structure
  def get_structure(self, name):
    if isinstance(name, list):
      namespace, name = name[0], name[1]
    else:
      namespace = self.namespace
    if self.is_local():
      for structs in reversed(self.table[self.__localstructs]):
        if name in structs:
          return structs[name]
    if self.namespace == namespace:
      struct = self.table[self.__structs].get(name, None)
      if struct is not None:
        return struct
    struct = StructuresRegistry.get_structure(namespace, name)
    if struct is not None:
      return struct
    raise ex.VarUndeclared(f'Structure `{name}` non déclarée')
  def set_local(self, context_name: str):
    self.table[self.__local].append({})
    self.table[self.__context].append(Context(context_name))
    self.__localrefs.append({})
    self.table[self.__localfunc].append({})
    self.table[self.__localstructs].append({})
  def del_local(self):
    if self.table[self.__local]:
      self.table[self.__local].pop()
    if self.table[self.__context]:
      self.table[self.__context].pop()
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
      raise ex.VarUndeclared(f'Variable `{name}` non déclarée')
  def reset(self):
    self.__superglobal.clear()
    self.__main_global.clear()
    self.table[self.__func].clear()
    self.table[self.__local].clear()
    self.table[self.__context].clear()
    self.table[self.__vars].clear()
    self.table[self.__structs].clear()
    self.__localrefs.clear()
    self.table[self.__localfunc].clear()
    self.table[self.__localstructs].clear()
  def dump(self):
    if self.__superglobal:
      print('%%% Super globales')
      for k, v in sorted(self.__superglobal.items()):
        if isinstance(v, tuple):
          if k.startswith('@'):
            continue
          print('... Constante', k, '=', repr(v[1]))
        else:
          print('... Variable', k, '=', repr(v))
      print('---')
    if self.__main_global:
      print('+++ Variables globales')
      for k, v in sorted(self.__main_global.items()):
        if k.startswith('@'):
          continue
        if isinstance(v, tuple):
          print('... Constante', k, '=', repr(v[1]))
        else:
          print('... Variable', k, '=', repr(v))
      print('---')
    if self.table[self.__vars]:
      print('+++ Variables locales', self.namespace)
      for k, v in sorted(self.table[self.__vars].items()):
        if k.startswith('@'):
          continue
        if isinstance(v, tuple):
          print('... Constante', k, '=', repr(v[1]))
        else:
          print('... Variable', k, '=', repr(v))
      print('---')
    if self.table[self.__structs]:
      print('+++ Structures')
      for v in self.table[self.__structs].values():
        print('...', v)
      print('---')
    if self.is_local():
      if self.table[self.__local]:
        print('@@@ Variables locales')
        for i, locs in enumerate(self.table[self.__local]):
          context = self.table[self.__context][i]
          print('### Contexte', context.name, '+' if context.dereference else '-')
          for k, v in locs.items():
            print('...', k, '=', repr(v))
          print('---')
        if self.table[self.__localstructs][-1]:
          print('+++ Structures locales')
          for v in sorted(self.table[self.__localstructs].values()):
            print('...', v)
        if not self.table[self.__localfunc]:
          print('+++ Fonctions et Procédures')
          for k, v in sorted(self.table[self.__localfunc].items()):
            if k.startswith('@'):
              continue
            print(f'... {k} :', v)
          print('---')
        if self.__localrefs:
          print('&&& Références locales')
          for refs in self.__localrefs:
            for k, v in sorted(refs.items()):
              print('...', k, '=', repr(v))
          print('---')
    if self.table[self.__func]:
      print('+++ Fonctions et Procédures')
      for k, v in sorted(self.table[self.__func].items()):
        if k.startswith('@'):
          continue
        print(f'... {k} :', v)
      print('---')
  def __repr__(self):
    return f'Espace {self.namespace}'

class Namespaces:
  def __init__(self, get_type):
    self.__namespaces = {}
    self.get_type = get_type
    # init main namespace
    self.__namespaces['main'] = Symbols(get_type_func=get_type, namespace='main')
    self.current_namespace = 'main'
  def set_current_namespace(self, name):
    self.current_namespace = name
  def declare_namespace(self, name):
    if name in self.__namespaces:
      raise ex.VarRedeclared(f'Redéclaration de l\'espace `{name}`')
    self.__namespaces[name] = Symbols(self.get_type, name)
    self.current_namespace = name
  def get_namespace(self, name=None):
    if not name:
      namespace = self.current_namespace
    else:
      namespace = name
    if namespace in self.__namespaces:
      return self.__namespaces[namespace]
    raise ex.VarUndeclared(f'Espace `{name}` non déclaré')
  def declare_ref(self, name, var, namespace):
    sym = self.get_namespace(namespace)
    sym.declare_ref(name, var)
  def get_current_context(self):
    sym = self.get_namespace(self.current_namespace)
    if sym.is_local():
      return sym.get_local_ref_context()
    return None
  def get_variable(self, name, namespace=None):
    if name.startswith('@'):
      if self.current_namespace != namespace:
        raise ex.FralgoException('Accès à un symbole privé')
    sym = self.get_namespace(namespace)
    return sym.get_variable(name)
  def get_function(self, name, namespace):
    if name.startswith('@'):
      if self.current_namespace != namespace:
        raise ex.FralgoException('Accès à un symbole privé')
    sym = self.get_namespace(namespace)
    return sym.get_function(name)
  def get_structure(self, name, namespace):
    sym = self.get_namespace(namespace)
    return sym.get_structure(name)
  def set_local(self, namespace:str, context_name:str):
    sym = self.get_namespace(namespace)
    sym.set_local(context_name)
  def del_local(self, namespace):
    sym = self.get_namespace(namespace)
    sym.del_local()
  def del_namespace(self, name):
    namespace = self.__namespaces.get(name, None)
    if namespace is not None:
      self.__namespaces.pop(name)
    else:
      raise ex.VarUndeclared(f'Espace `{name}` non défini.')
  def reset(self):
    for symbols in self.__namespaces.values():
      symbols.reset()
    StructuresRegistry.clear_structures()
    self.__namespaces.clear()
    self.__namespaces['main'] = Symbols(self.get_type, 'main')
    self.current_namespace = 'main'
  def dump(self, namespace='main', current=False):
    self.get_namespace(namespace)
    print('=== Espace :', end=' ')
    if current:
      print(self.current_namespace)
      context = self.__namespaces[self.current_namespace]
      context.dump()
    elif self.__namespaces.get(namespace, None) is not None:
      print(namespace)
      self.__namespaces[namespace].dump()
  def namespaces(self):
    print(f'{", ".join(k for k in self.__namespaces.keys())}')
