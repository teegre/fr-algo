'''Abstract syntax tree'''
#  _______ ______        _______ _____   _______ _______
# |    ___|   __ \______|   _   |     |_|     __|       |
# |    ___|      <______|       |       |    |  |   -   |
# |___|   |___|__|      |___|___|_______|_______|_______|
#
# This file is part of FR-ALGO
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
from sys import stdout, stderr
import operator
from time import sleep
from random import random
from datetime import datetime

from fralgo.lib.libman import LibMan
from fralgo.lib.datatypes import map_type
from fralgo.lib.datatypes import Array, Boolean, Char, Number, Float, Integer, String, Table
from fralgo.lib.datatypes import Nothing, Structure, StructureData, _get_type
from fralgo.lib.symbols import Namespaces
from fralgo.lib.file import new_file_descriptor, get_file_descriptor, clear_file_descriptor
from fralgo.lib.exceptions import print_err
from fralgo.lib.exceptions import FralgoException, BadType, InterruptedByUser, VarUndeclared, PanicException
from fralgo.lib.exceptions import ReadOnlyValue, VarUndefined, ZeroDivide
from fralgo.lib.exceptions import FuncInvalidParameterCount, FralgoInterruption, FatalError

namespaces = Namespaces(_get_type)
libs = LibMan()
libs.set_namespaces(namespaces)

class Node:
  def __init__(self, stmt=None, lineno=0):
    self.statement = stmt
    self.children = []
    self.lineno = lineno
  def append(self, stmt=None, lineno=0):
    if stmt is not None:
      if not isinstance(stmt, Node):
        child = Node(stmt, self.lineno if lineno == 0 else lineno)
      else:
        child = stmt
      self.children.append(child)
  def eval(self):
    result = None
    try:
      if self.statement:
        node = self.statement
        result = self.statement.eval()
        if result is not None:
          return result
      if self.children:
        for statement in self.children:
          node = statement
          result = statement.eval()
          if result is not None:
            return result
      return result
    except RecursionError:
      self.handle_err('STOP : excès de récursivité !')
    except FatalError as e:
      self.handle_err(e.message)
    except FralgoException as e:
      self.handle_err(e.message)
  def handle_err(self, message):
    if namespaces.current_namespace != 'main':
      print_err(f'Espace `{namespaces.current_namespace}`')
    if message:
      print_err(message)
    if 'FRALGOREPL' not in os.environ:
      print_err(f'Ligne {self.lineno}')
      print('\033[?25h\033[0m', end='')
      sys.exit(666)
    raise FralgoInterruption('')
  def __getitem__(self, index):
    return self.children[index]
  def __iter__(self):
    return iter(self.children)
  def __str__(self):
    return '\n'.join(str(child) for child in self.children)
  def __repr__(self):
    return f'Node({self.lineno}) {self.statement}'

class Declare:
  def __init__(self, name, var_type):
    self.name = name
    self.var_type = var_type
  def eval(self):
    sym = namespaces.get_namespace(name=None)
    if isinstance(self.var_type, tuple): # sized char
      sym.declare_sized_char(self.name, self.var_type[1])
    else:
      sym.declare_var(self.name, self.var_type)
  def __repr__(self):
    return f'Variable {self.name} en {self.var_type}'

class DeclareConst:
  def __init__(self, name, value):
    self.name = name
    self.value = map_type(value)
  def eval(self):
    sym = namespaces.get_namespace(name=None)
    sym.declare_const(self.name, self.value)
  def __repr__(self):
    return f'Constante {self.name} {self.value}'

class DeclareArray:
  def __init__(self, name, var_type, *max_indexes):
    self.name = name
    self.var_type = var_type
    self.max_indexes = max_indexes
  def eval(self):
    sym = namespaces.get_namespace(name=None)
    sym.declare_array(self.name, self.var_type, *self.max_indexes)
  def __repr__(self):
    indexes = [str(n) for n in self.max_indexes]
    idx = ','.join(indexes)
    if idx == '-1':
      idx = ''
    return f'Tableau {self.name}[{idx}] en {self.var_type}'

class DeclareSizedChar:
  def __init__(self, name, size):
    self.name = name
    self.size = size
  def eval(self):
    sym = namespaces.get_namespace(name=None)
    sym.declare_sized_char(self.name, self.size)
  def __repr__(self):
    return f'Variable {self.name}*{self.size}'

class DeclareTable:
  def __init__(self, name, key_type, value_type):
    self.name = name
    self.key_type = key_type
    self.value_type = value_type
  def eval(self):
    sym = namespaces.get_namespace(name=None)
    sym.declare_table(self.name, self.key_type, self.value_type)
  def __repr__(self):
    return f'Table {self.name}'

class DeclareStruct:
  __types = ('Booléen', 'Caractère', 'Chaîne', 'Entier', 'Numérique')
  def __init__(self, name, fields):
    self.name = name
    self.fields = fields
  def eval(self):
    sym = namespaces.get_namespace(name=None)
    for field, datatype in self.fields:
      if datatype not in self.__types:
        if datatype == self.name: # recursive structure.
          continue
        elif isinstance(datatype, tuple) or sym.is_structure(datatype):
          continue
        raise BadType(f'Type invalide : `{self.name}.{field} en >{datatype}`')
    sym.declare_structure(Structure(self.name, self.fields))
  def __repr__(self):
    return f'Structure {self.name} {self.fields}'

class ArrayGetItem:
  def __init__(self, var, *indexes, namespace=None):
    self.var = var
    self.indexes = indexes
    self.namespace = namespace
  def eval(self):
    try:
      var = self.var.eval()
    except AttributeError:
      var = namespaces.get_variable(self.var, self.namespace)
    return var.get_item(*self.indexes)
  @property
  def data_type(self):
    value = map_type(self.eval())
    return value.data_type
  def __repr__(self):
    indexes = [str(index.eval()) for index in self.indexes]
    return f'{self.var.name}[{",".join(indexes)}]'

class ArraySetItem:
  def __init__(self, var, value, *indexes):
    self.var = var
    self.value = value
    self.indexes = indexes
  def eval(self):
    var = namespaces.get_variable(self.var.name, None)
    if isinstance(var, tuple):
      raise ReadOnlyValue(f'Constante `{self.var.name}` : valeur en lecture seule')
    var = self.var.eval()
    var.set_value(self.indexes, self.value)
  def __repr__(self):
    indexes = (str(index) for index in self.indexes)
    return f'{self.var.name}[{",".join(indexes)}] ← {self.value}'

class ArrayResize:
  def __init__(self, var, *indexes):
    self.var = var
    self.indexes = indexes
  def eval(self):
    if isinstance(self.var, Variable):
      if self.var.is_constant:
        raise ReadOnlyValue(f'Constante `{self.var.name}` : en lecture seule')
    var = self.var.eval()
    var.resize(*self.indexes)
  def __repr__(self):
    indexes = (str(index) for index in self.indexes)
    return f'Redim {self.var.name}[{",".join(indexes)}]'

class FreeFormArray(Array):
  def __init__(self, value):
    super().__init__(map_type(value[0]).data_type, len(value) - 1)
    self.value = [v.eval() if isinstance(v, (Variable, BinOp)) else v for v in value]
  def check(self):
    datatype = Array.get_datatype(self.value)
    Array.check_types(self.value, datatype)
  def eval(self):
    if self.value:
      return self.value
    # there should always be a value
    raise VarUndefined('Valeur indéfinie')
  def __iter__(self):
    return iter(self.value)
  def __getitem__(self, index):
    return self.value[index]
  def __len__(self):
    return len(self.value)
  # def __repr__(self):
  #   return f'{[v.eval() for v in self.value]}'
  # def __str__(self):
  #   return f'{[v.eval() for v in self.value]}'

class SizeOf:
  def __init__(self, var):
    self.var = var
  def eval(self):
    if issubclass(type(self.var), Array):
      var = self.var
    else:
      var = self.var.eval()
    if isinstance(var, Array):
      return var.size
    if isinstance(var, Table):
      return len(var)
    raise BadType('Taille(T) : type `Tableau` attendu')
  @property
  def data_type(self):
    if isinstance(self.var, Array) or issubclass(type(self.var), Array):
      if len(self.var.sizes) == 1:
        return 'Entier'
      indexes = ",".join([str(v) for v in self.var.indexes])
      return f'Tableau[{len(self.var.indexes) - 1}] en Entier'
    var = self.var.eval()
    if isinstance(var, Table):
      return 'Entier'
    if isinstance(var, Array) or issubclass(type(var), Array):
      if len(var.sizes) == 1:
        return 'Entier'
      return f'Tableau[{len(var.indexes) - 1}] en Entier'
    return var.data_type
  def __repr__(self):
    return f'Taille({self.var})'

class TableKeyExists:
  def __init__(self, var, key):
    self.var = var
    self.key = key
  def eval(self):
    var = self.var.eval()
    if not isinstance(var, Table):
      raise BadType(f'Existe({self.var.name, ...}) : type `Table` attendu')
    return var.value.get(self.key.eval()) is not None
  def __repr__(self):
    return f'Existe({self.var.name}, {self.key})'

class TableGetKeys:
  def __init__(self, var):
    self.var = var
  def eval(self):
    var = self.var.eval()
    keys = var.get_keys()
    return keys
  @property
  def data_type(self):
    var = self.var.eval()
    keys = var.get_keys()
    return repr_datatype(keys.data_type)
  def __repr__(self):
    return f'Clefs({self.var})'

class TableGetValues:
  def __init__(self, var):
    self.var = var
  def eval(self):
    var = self.var.eval()
    values = var.get_values()
    return values
  @property
  def data_type(self):
    var = self.var.eval()
    values = var.get_values()
    return repr_datatype(values.data_type)
  def __repr__(self):
    return f'Valeurs({self.var})'

class TableEraseKey:
  def __init__(self, var, key):
    self.var = var
    self.key = key
  def eval(self):
    var = self.var.eval()
    var.delete_key(self.key.eval())

class StructureGetItem:
  def __init__(self, name, field, namespace=None):
    self.name = name
    self.field = field
    self.namespace = namespace
  def eval(self):
    if isinstance(self.name, tuple):
      if len(self.name) > 1:
        structure = namespaces.get_variable(self.name[0], self.namespace)
        for field in self.name[1:]:
          structure = structure.get_item(field)
        return structure.get_item(self.field)
    if isinstance(self.name, (ArrayGetItem, StructureGetItem)):
      var = self.name.eval()
    else:
      var = namespaces.get_variable(self.name, self.namespace)
    try:
      return var.get_item(self.field)
    except AttributeError:
      raise BadType(f'`{self.var}` : Erreur inattendue')
  @property
  def data_type(self):
    value = map_type(self.eval())
    return value.data_type
  def __repr__(self):
    return f'{self.name}.{self.field}'

class StructureSetItem:
  def __init__(self, var, field, value, namespace=None):
    self.var = var
    self.field = field
    self.value = value
    self.namespace = namespace
  def eval(self):
    if isinstance(self.var, tuple):
      if len(self.var) > 1:
        structure = namespaces.get_variable(self.var[0], self.namespace)
        for field in self.var[1:]:
          structure = structure.get_item(field)
        var = structure
    elif isinstance(self.var, (StructureGetItem, ArrayGetItem)):
      var = self.var.eval()
    else:
      var = namespaces.get_variable(self.var, self.namespace)

    if isinstance(self.field, tuple): # Array!
      var.set_value(
          self.value if isinstance(self.value, list) else self.value.eval(),
          (self.field[0], (self.field[1],)))
    elif isinstance (self.value, list):
      if isinstance(var, StructureData):
        var.set_value(self.value, self.field)
      else:
        var.set_value(None, self.value)
    else:
      if self.field is None:
        var.set_value(self.value.eval())
      else:
        var.set_value(self.value.eval(), self.field)
  def __repr__(self):
    return f'{self.var}.{self.field} ← {self.value}'

class Function:
  '''A function definition'''
  def __init__(self, name, params, body, return_type=None):
    self.name = name # str
    self.params = params # [(name, datatype)]
    self.body = body # Node
    self.return_type = return_type # str
    self.namespace = namespaces.current_namespace
    if return_type is None:
      self.ftype = 'Procédure'
    else:
      self.ftype = 'Fonction'
  def eval(self):
    sym = namespaces.get_namespace(self.namespace)
    sym.declare_function(self)
  def __repr__(self):
    if self.params:
      params = [f'{param[0]}{repr_datatype(param[1:], shortform=True)}' for param in self.params]
    else:
      params = ''
    if self.return_type is not None:
      return f'Fonction {self.name}({",".join(params)}) en {self.return_type}'
    return f'Procédure {self.name}({",".join(params)})'

class FunctionCall:
  '''Function call'''
  def __init__(self, name, params, namespace=None):
    self.name = name
    self.params = params
    self.namespace = namespace if namespace else namespaces.current_namespace
    self.cnamespace = namespaces.current_namespace
  def _check_param_count(self, params):
    if self.params is None and params is not None:
      x = len(params) # expected
      raise FuncInvalidParameterCount(f'`{self.name}` nombre de paramètres invalide : 0, attendu {x} ')
    if self.params is not None:
      if len(self.params) != len(params):
        a = len(self.params) # actual
        x = len(params) # expected
        raise FuncInvalidParameterCount(f'`{self.name}` nombre de paramètres invalide : {a}, attendu {x} ')
  def _check_datatypes(self, params):
    for i, p in enumerate(self.params):
      if isinstance(params[i][0], Reference):
        # enable dereferencing
        sym = namespaces.get_namespace(self.namespace)
        sym.set_local_ref_context(dereference=True)
      p1 = params[i][1][0] if isinstance(params[i][1][0], tuple) else params[i][1:]
      try:
        if isinstance(p, (BinOp, Node, ArrayGetItem, StructureGetItem)):
          p2 = map_type(p.eval())
          p2 = p2.data_type
        elif p.data_type == 'Quelconque':
          p2 = map_type(p).data_type
        else:
          p2 = p.data_type
      except AttributeError:
        raise BadType(f'`{self.name}` : paramètre {i+1} invalide.')
      p2 = (p2,) if not isinstance(p2, tuple) else p2
      if p1 == p2:
        continue
      for n, q in enumerate(zip(p1, p2)):
        match n:
          case 0:
            t1, t2 = q
          case 1:
            t3, t4 = q
          case 2:
            t5, t6 = q
      ok = True
      if isinstance(t1, tuple):
        if t1[0] == t2 == 'Caractère':
          continue
      if t1 == 'Chaîne' and t2 == 'Caractère':
        continue
      if t1 == 'Quelconque':
        continue
      if t1 == t2 == 'Tableau':
        if t3 == 'Chaîne' and t4[0] == 'Caractère':
          ok &= True
        elif t3 == 'Quelconque':
          ok &= True
        elif t3 != t4:
          ok &= False
        if t5 == -1 and not isinstance(t6, tuple):
          ok &= True
      else:
        ok &= False
      if not ok:
        raise BadType(f'`{self.name}` : type {repr_datatype(p1)} attendu [paramètre {i + 1}]')
  def _check_returned_type(self, rt, value):
    mv = map_type(value)
    if isinstance(rt, tuple): # Sized char.
      clen = map_type(rt[1]).eval()
      if mv.data_type == 'Chaîne' and len(mv) == clen:
        return
      rt = rt[0] + '*' + str(rt[1])
    if isinstance(mv.data_type, tuple):
      mvdt = mv[0] + '*' + str(mv[1])
    else:
      mvdt = mv.data_type
    if rt == 'Quelconque':
      return
    if rt != mvdt:
      raise BadType(f'Type `{rt}` attendu [{mv.data_type}]')
  def eval(self):
    func = namespaces.get_function(self.name, self.namespace)
    params = func.params
    namespaces.set_local(self.namespace, context_name=self.name)
    sym = namespaces.get_namespace(self.namespace)
    if params is not None:
      # check parameter count
      self._check_param_count(params)
      # check data types
      self._check_datatypes(params)
      # False if param is a Reference, True otherwise.
      types = [not isinstance(param[0], Reference) for param in params]
      # Evaluate everything but References and FreeFormArray (Array subclass)
      values = [
          param.eval()
          if types[i] and not issubclass(type(param), Array)
          else param
          for i, param in enumerate(self.params)]
      # set variables
      for i, param in enumerate(params):
        if isinstance(self.params[i], (Variable, StructureGetItem, ArrayGetItem)):
          if self.params[i].namespace is None:
            self.params[i].namespace = self.cnamespace
        if isinstance(param[0], Reference):
          sym.declare_ref(param[0].name, self.params[i])
          continue
        if len(param) == 4: # Array
          n, _, t, s = param
          if t == 'Quelconque':
            t = self.params[i].data_type[1]
          if s == -1:
            if isinstance(self.params[i], (ArrayGetItem, StructureGetItem, Variable)):
              array = self.params[i].eval()
            else:
              try:
                array = namespaces.get_variable(self.params[i].name, self.params[i].namespace)
              except AttributeError:
                array = self.params[i]
            if array is None:
              array = self.params[i].eval()
            if isinstance(array, tuple): # Constant!
              array = array[1]
            sym.declare_array(n, t, *array.indexes)
          else:
            sym.declare_array(n, t, *s)
        elif isinstance(param[1], tuple): # Sized char
          n, dt = param
          _, s = dt
          sym.declare_sized_char(n, s)
        else:
          n, t = param
          if t == 'Quelconque':
            t = self.params[i].data_type
          sym.declare_var(n, t)

        sym.assign_value(n, values[i])

    # function body
    body = func.body

    namespaces.set_current_namespace(self.namespace)

    try:
      result = body.eval()
      if not isinstance(result, ProcTerminate) and result is not None:
        if func.ftype == 'Procédure':
          raise FralgoException(f'`{self.name}` : instruction `Retourne` inattendue')
        self._check_returned_type(func.return_type, result)
        return result if not isinstance(result, bool) else map_type(result)
      if func.ftype == 'Fonction':
        raise FralgoException(f'`{self.name}` : instruction `Retourne` absente')
    except FralgoException as e:
      raise e
    finally:
      namespaces.del_local(self.namespace)
      namespaces.set_current_namespace(self.cnamespace)
    return None
  def __repr__(self):
    try:
      func = namespaces.get_function(self.name, self.namespace)
    except VarUndeclared:
      func = None
    params = [str(param) for param in self.params]
    if func:
      if func.return_type is not None:
        return f'{self.name}({",".join(params)}) → {func.return_type}'
    else:
      return f'{self.name}({",".join(params)})'

class FunctionReturn:
  def __init__(self, expression):
    self.expression = expression
    self.namespace = namespaces.current_namespace
  def eval(self):
    sym = namespaces.get_namespace(self.namespace)
    if sym.is_local_function():
      return self.expression.eval()
    raise FralgoException('Erreur de syntaxe : `Retourne` en dehors d\'une fonction')
  def __repr__(self):
    return f'Retourne {self.expression}'

class ProcTerminate:
  def eval(self):
    return self
  def __repr__(self):
    return 'Terminer'

class Assign:
  def __init__(self, var, value):
    self.var = var
    self.value = value
  def eval(self):
    if isinstance(self.var, list):
      namespace, name = self.var
    else:
      namespace, name = namespaces.current_namespace, self.var
    sym = namespaces.get_namespace(namespace)
    value = self.value
    if issubclass(type(value), Array):
      sym.assign_value(name, value, namespace)
    else:
      sym.assign_value(name, value.eval(), namespace)
  def __repr__(self):
    return f'{self.var} ← {self.value}'

class Variable:
  def __init__(self, name, namespace=None):
    self.name = name
    self.namespace = namespace if namespace is not None else namespaces.current_namespace
  def eval(self):
    var = namespaces.get_variable(self.name, self.namespace)
    # sym = namespaces.get_namespace(self.namespace)
    # var = sym.get_variable(self.name)
    if isinstance(var, tuple): # constant!
      var = var[1]
    if isinstance(var, (Boolean, Number, String, Variable)):
      return var.eval()
    return var
  def __repr__(self):
    try:
      value = namespaces.get_variable(self.name, self.namespace)
      return f'{self.name} → {value}'
    except (VarUndeclared, VarUndefined):
      return f'{self.name} → ?'
  @property
  def is_constant(self):
    value = namespaces.get_variable(self.name, self.namespace)
    if isinstance(value, tuple):
      return value[0] == 'CONST'
    return False
  @property
  def data_type(self):
    var = namespaces.get_variable(self.name, self.namespace)
    if isinstance(var, tuple): # constant!
      var = var[1]
    return var.data_type
  @property
  def key_type(self):
    if self.data_type == 'Table':
      var = namespaces.get_variable(self.name, self.namespace)
      return var.key_type
    raise BadType(f'La variable `{self.name}` n\'est pas de type Table')
  @property
  def value_type(self):
    if self.data_type == 'Table':
      var = namespaces.get_variable(self.name, self.namespace)
      return var.value_type
    raise BadType(f'La variable `{self.name}` n\'est pas de type Table')

class Reference(Variable):
  def __repr__(self):
    return f'&{self.name}'

class Print:
  '''Print statement. Display one or several elements'''
  def __init__(self, data, newline=True, err=False):
    self.data = data
    self.newline = newline
    self.err = err # write on stderr
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
    std = stdout if not self.err else stderr
    if self.newline:
      std.write(' '.join(result) + '\n')
    else:
      std.write(' '.join(result))
    stdout.flush()
  def __repr__(self):
    return f'Ecrire {self.data}'

class PrintErr(Print):
  def __init__(self, data, newline=True, err=True):
    super().__init__(data, newline, err)
def __repr__(self):
  return f'EcrireErr {self.data}'

class Read:
  '''
  Read user input and assign value to a variable...
  '''
  def __init__(self, var, *args):
    self.var = var
    self.args = args
  def eval(self):
    '''... on evaluation'''
    # sym = namespaces.get_namespace(name=None)
    try:
      user_input = input()
    except (KeyboardInterrupt, EOFError):
      print()
      raise InterruptedByUser('Interrompu par l\'utilisateur')
    try:
      var = namespaces.get_variable(self.var, None)
      # var = sym.get_variable(self.var)
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
      raise BadType(f'Type `{var.data_type}` attendu')
  def __repr__(self):
    return f'Lire {self.var}'

class BinOp:
  __op = {
      '+'   : operator.add,
      '-'   : operator.sub,
      '*'   : operator.mul,
      '/'   : 'dummy',
      '%'   : operator.mod,
      'DP'  : 'dummy',
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
      'OUX' : operator.xor,
      'NON' : operator.not_,
  }
  def __init__(self, op, a, b):
    self.a = a
    self.b = b
    self.op = op
  def eval(self):
    a = algo_to_python(self.a)
    b = algo_to_python(self.b)
    op = self.__op.get(self.op, None)
    comp = ('=', '<>', '<', '>', '<=', '>=')
    if self.op == '/':
      if not isinstance(a, (int, float)) and not isinstance(b, (int, float)):
        raise BadType('E|N / E|N : Type Entier ou Numérique attendu')
      if isinstance(a, int) and isinstance(b, int):
        if b == 0:
          raise ZeroDivide('Division par zéro')
        op = operator.floordiv
      elif isinstance(a, float) or isinstance(b, float):
        if b == 0:
          raise ZeroDivide('Division par zéro')
        op = operator.truediv
    elif self.op == '*':
      if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise BadType('E|N * E|N : Type Entier ou Numérique attendu')
    elif self.op == 'DP':
      return map_type(a % b == 0)
    elif self.op == '&':
      if isinstance(a, str) and isinstance(b, str):
        return a + b
      raise BadType('C & C : Type Chaîne attendu')
    elif self.b is None:
      return op(a)
    elif isinstance(a, str) and isinstance(b, str) and self.op not in comp:
      raise BadType(f'E|N {self.op} E|N : Type Entier ou Numérique attendu')
    try:
      return op(a, b)
    except TypeError:
      raise BadType('Opération sur des types incompatibles')
  @property
  def data_type(self):
    value = map_type(self.eval())
    return value.data_type
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
  @property
  def data_type(self):
    return self.value.data_type

class If:
  def __init__(self, condition, dothis, dothat):
    self.condition = condition
    self.dothis = dothis
    self.dothat = dothat
  def eval(self):
    if self.condition.eval():
      result = self.dothis.eval()
      if result is not None:
        return result
    elif self.dothat is not None:
      result = self.dothat.eval()
      if result is not None:
        return result
    return None
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
        result = self.dothis.eval()
        if result is not None:
          return result
      except KeyboardInterrupt:
        print()
        raise InterruptedByUser('Interrompu par l\'utilisateur')
      except FralgoInterruption:
        return None
    return None
  def __repr__(self):
    return f'TantQue {self.condition} → {self.dothis}'

class For:
  def __init__(self, v, b, e, dt, nv, s=Integer(1), namespace=None):
    self.var = v.name
    self.start = b
    self.end = e
    self.step = s
    self.dothis = dt
    self.var_next = nv.name
    self.namespace = namespace
  def eval(self):
    sym = namespaces.get_namespace(self.namespace)
    if self.var != self.var_next:
      raise FralgoException(f'Pour `{self.var}` ... `{self.var_next}` Suivant')
    i = self.start.eval()
    end = self.end.eval()
    step = self.step.eval()
    sym.assign_value(self.var, i)
    while i <= end if step > 0 else i >= end:
      try:
        result = self.dothis.eval()
      except KeyboardInterrupt:
        print()
        raise InterruptedByUser('Interrompu par l\'utilisateur')
      except FralgoInterruption:
        return None
      if result is not None:
        return result
      i += step
      sym.assign_value(self.var, i)
    return None
  def __repr__(self):
    return f'Pour {self.var} ← {self.start} à {self.end} → {self.dothis}'

class Len:
  def __init__(self, value):
    self.value = value
  def eval(self):
    try:
      return len(self.value.eval())
    except TypeError:
      raise BadType('Longueur(C | T) : Type Chaîne ou Tableau attendu')
  def __repr__(self):
    return f'Longueur({self.value})'

class Mid:
  def __init__(self, exp, start, length):
    self.exp = exp
    self.start = start
    self.length = length
  def eval(self):
    exp = algo_to_python(self.exp)
    start = algo_to_python(self.start)
    length = algo_to_python(self.length)
    if not isinstance(exp, str):
      raise BadType('Extraire(`C`, E, E) : Type Chaîne attendu')
    if not isinstance(start, int):
      raise BadType('Extraire(C, `E`, E) : Type Entier attendu')
    if not isinstance(length, int):
      raise BadType('Extraire(C, E, `E`) : Type Entier attendu')
    return exp[start-1:start-1+length]
  def __repr__(self):
    return f'Extraire{self.exp, self.start, self.length}'
  @property
  def data_type(self):
    return 'Chaîne'

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
    exp = algo_to_python(self.exp)
    length = algo_to_python(self.length)
    if not isinstance(exp, str):
      raise BadType(f'{self.cmd}(`C`, E) : Type Chaîne attendu')
    if not isinstance(length, int):
      raise BadType(f'{self.cmd}(C, `E`) : Type Entier attendu')
    if not self.right:
      return exp[:length]
    return exp[len(exp) - length:]
  def __repr__(self):
    return f'{self.cmd}({self.exp}, {self.length})'
  @property
  def data_type(self):
    return 'Chaîne'

class Find:
  def __init__(self, str1, str2):
    self.str1 = str1
    self.str2 = str2
  def eval(self):
    try:
      str1 = algo_to_python(self.str1)
      str2 = algo_to_python(self.str2)
      result = str1.find(str2)
      return result + 1
    except AttributeError:
      raise BadType('Trouve(`C`, C) : Type Chaîne attendu')
    except TypeError:
      raise BadType('Trouve(C, `C`) : Type Chaîne attendu')
  def __repr__(self):
    return f'Trouve({self.str1}, {self.str2})'
  @property
  def data_type(self):
    return 'Entier'

class OpenFile:
  def __init__(self, filename, fd, access_mode):
    self.filename = filename
    self.fd_number = fd
    self.access_mode_str = access_mode
    match access_mode:
      case 'Lecture':
        self.access_mode = 1
      case 'Ecriture':
        self.access_mode = 2
      case 'Ajout':
        self.access_mode = 3
  def eval(self):
    fd = new_file_descriptor(self.fd_number.eval())
    if fd is None:
      raise FatalError(f'Pas de fichier affecté au canal {self.fd_number}')
    try:
      fd.open_file(self.filename.eval(), self.access_mode)
    except FatalError as e:
      raise e
  def __repr__(self):
    return f'Ouvrir {self.filename} sur {self.fd_number} en {self.access_mode_str}'

class ReadFile:
  def __init__(self, fd, var):
    self.fd_number = fd
    self.var = var
  def eval(self):
    fd = get_file_descriptor(self.fd_number.eval())
    if fd is None:
      raise FatalError(f'Pas de fichier affecté au canal {self.fd_number}')
    if isinstance(self.var, ArrayGetItem):
      var = self.var.eval()
    else:
      var = namespaces.get_variable(self.var, namespace=None)
    value = fd.read()
    var.set_value(value)
  def __repr__(self):
    return f'LireFichier {self.fd_number}, {self.var}'

class WriteFile:
  def __init__(self, fd, var):
    self.fd_number = fd
    self.var = var
  def eval(self):
    sym = namespaces.get_namespace(name=None)
    fd = get_file_descriptor(self.fd_number.eval())
    if fd is None:
      raise FatalError(f'Pas de fichier affecté au canal {self.fd_number}')
    elif isinstance(self.var, (Variable, BinOp, Boolean, Float, Integer, String, ArrayGetItem, StructureGetItem, Structure)):
      var = self.var.eval()
    else:
      var = self.var
    fd.write(str(var))
  def __repr__(self):
    return f'EcrireFichier {self.fd_number}, {self.var}'

class EOF:
  def __init__(self, fd):
    self.fd_number = fd
  def eval(self):
    fd = get_file_descriptor(self.fd_number.eval())
    if fd is None:
      raise FatalError(f'Pas de fichier affecté au canal {self.fd_number}')
    return map_type(fd.eof)
  def __repr__(self):
    return f'FDF({self.fd_number})'

class CloseFile:
  def __init__(self, fd):
    self.fd_number = fd
  def eval(self):
    fd = get_file_descriptor(self.fd_number.eval())
    if fd is None:
      raise FatalError(f'Pas de fichier affecté au canal {self.fd_number}')
    fd.close_file()
    clear_file_descriptor(self.fd_number.eval())
  def __repr__(self):
    return f'Fermer {self.fd_number}'

class Chr:
  def __init__(self, value):
    self.value = value
  def eval(self):
    value = self.value.eval()
    if not isinstance(value, int):
      raise BadType('Car(`E`) : Type Entier attendu')
    return chr(value)
  def __repr__(self):
    return f'Car({self.value})'
  @property
  def data_type(self):
    return 'Chaîne'

class Ord:
  def __init__(self, value):
    self.value = value
  def eval(self):
    value = self.value.eval()
    if not isinstance(value, str):
      raise BadType('CodeCar(`C`) : Type Chaîne attendu')
    if len(value) != 1:
      raise BadType('CodeCar(`C`) : Chaîne de longueur 1 attendue')
    return ord(value)
  def __repr__(self):
    return f'CodeCar({self.value})'
  @property
  def data_type(self):
    return 'Entier'

class Type:
  def __init__(self, var):
    self.var = var
  def eval(self):
    if isinstance(self.var, str):
      var = namespaces.get_variable(self.var)
      return repr_datatype(map_type(var.data_type))
    if isinstance(self.var, Node):
      try:
        return repr_datatype(map_type(self.var.eval()).data_type)
      except AttributeError:
        raise BadType(f'Pas de type.')
    return repr_datatype(self.var.data_type)
  def __repr__(self):
    return f'Type({self.var})'

class Panic:
  def __init__(self, data):
    self.data = data
  def eval(self):
    data = []
    for e in self.data:
      if isinstance(e, (BinOp, Variable)):
        if isinstance(e.eval(), bool):
          data.append(str(map_type(e.eval())))
          continue
      data.append(str(e.eval()))
      raise PanicException(' '.join(data))
  def __repr__(self):
    return f'Panique {self.data}'

class ToInteger:
  def __init__(self, value):
    self.value = value
  def eval(self):
    value = algo_to_python(self.value)
    tvalue = map_type(self.value)
    try:
      return int(value)
    except (ValueError, TypeError):
      raise BadType(f'Entier(N ou C) : conversion du type `{repr_datatype(tvalue.data_type)}` impossible')
  def __repr__(self):
    return f'Entier({self.value})'
  @property
  def data_type(self):
    return 'Entier'

class ToFloat:
  def __init__(self, value):
    self.value = value
  def eval(self):
    value = algo_to_python(self.value)
    tvalue = map_type(self.value)
    try:
      return float(value)
    except (ValueError, TypeError):
      raise BadType(f'Entier(E ou C) : Conversion du type `{repr_datatype(tvalue.data_type)}` impossible')
  def __repr__(self):
    return f'Numérique({self.value})'
  @property
  def data_type(self):
    return 'Numérique'

class ToString:
  def __init__(self, value):
    self.value = value
  def eval(self):
    value = algo_to_python(self.value)
    tvalue = map_type(self.value)
    try:
      return str(value)
    except (ValueError, TypeError):
      raise BadType(f'Chaîne(E ou N) : Conversion du type `{repr_datatype(tvalue.data_type)}` impossible')
  def __repr__(self):
    return f'Chaîne({self.value})'
  @property
  def data_type(self):
    return 'Chaîne'

class ToBoolean:
  def __init__(self, value):
    self.value = value
  def eval(self):
    value = algo_to_python(self.value)
    tvalue = map_type(self.value)
    try:
      return map_type(bool(value))
    except (ValueError, TypeError):
      raise BadType(f'Booléen(C ou E ou N) : Conversion du type `{repr_datatype(tvalue.data_type)}` impossible')
  def __repr__(self):
    return f'Booléen({self.value})'
  @property
  def data_type(self):
    return 'Booléen'

class Random:
  def eval(self):
    return map_type(random())
  def __repr__(self):
    return 'Aléa()'
  @property
  def data_type(self):
    return 'Numérique'

class Sleep:
  def __init__(self, duration):
    self.duration = duration
  def eval(self):
    duration = algo_to_python(self.duration)
    try:
      sleep(duration)
    except TypeError:
      raise BadType('Dormir(E ou N) : Type Entier ou Numérique attendu')
  def __repr__(self):
    return f'Dormir({self.duration})'

class UnixTimestamp:
  def eval(self):
    return datetime.now().timestamp()
  def __repr__(self):
    return 'TempsUnix()'
  @property
  def data_type(self):
    return 'Numérique'

class Import:
  def __init__(self, filename, Lexer, lex, parser, alias=None):
    self.filename = filename
    self.lexer = lex(object=Lexer())
    self.parser = parser
    self.alias = alias
  def eval(self):
    libs.set_lexer(self.lexer)
    libs.set_parser(self.parser)
    libs.import_lib(self.filename, self.alias)
  def __str__(self):
    return repr(self)
  def __repr__(self):
    if self.alias:
      return f'Importer "{self.filename}" Alias {self.alias}'
    return f'Importer "{self.filename}"'

def algo_to_python(expression):
  '''
  Evaluate an Algo expression/type to a Python type
  '''
  types = (
      ArrayGetItem,
      BinOp, Boolean,
      Char, Chr,
      EOF,
      Find,
      Len,
      Neg, Number,
      Ord,
      Mid,
      Node,
      Nothing,
      Random,
      SizeOf,
      String,
      StructureGetItem,
      TableKeyExists,
      ToBoolean, ToFloat, ToInteger, ToString,
      Trim,
      Type,
      UnixTimestamp,
      Variable,
  )
  exp = expression
  while isinstance(exp, types):
    exp = exp.eval()
  return exp

def get_type(expr):
  return Type(expr).eval()

def repr_datatype(datatype, shortform=False):
  if isinstance(datatype, (ArrayGetItem, StructureGetItem)):
    datatype = datatype.data_type
  datatype = algo_to_python(datatype)
  if isinstance(datatype[0], tuple):
    datatype = datatype[0]
  match datatype[0]:
    case 'Caractère':
      if shortform:
        return f' en {datatype[0]}*{datatype[1]}'
      return f'{datatype[0]}*{datatype[1]}'
    case 'Tableau':
      if isinstance(datatype[2], tuple):
        indexes = ','.join(str(idx) for idx in datatype[2])
      else:
        indexes = datatype[2] if datatype[2] != -1 else ''
      if shortform:
        return f'[{indexes}] en {repr_datatype(datatype[1])}'
      return f'{datatype[0]}[{indexes}] en {repr_datatype(datatype[1])}'
  if shortform:
    return f' en {datatype}' if not isinstance(datatype, tuple) else f' en {datatype[0]}'
  return datatype if not isinstance(datatype, tuple) else datatype[0]
