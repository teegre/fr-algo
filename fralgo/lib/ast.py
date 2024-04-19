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
from time import sleep
from random import random

from fralgo.lib.datatypes import map_type
from fralgo.lib.datatypes import Array, Boolean, Char, Number, Float, Integer, String
from fralgo.lib.datatypes import Structure, is_structure
from fralgo.lib.symbols import Symbols, declare_structure
from fralgo.lib.file import new_file_descriptor, get_file_descriptor, clear_file_descriptor
from fralgo.lib.exceptions import FralgoException, BadType, InterruptedByUser, VarUndeclared
from fralgo.lib.exceptions import VarUndefined, FatalError, ZeroDivide
from fralgo.lib.exceptions import FuncInvalidParameterCount

sym = Symbols()

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
        if isinstance(statement, FunctionReturn):
          return statement.eval()
        result = statement.eval()
      except FatalError as e:
        print(f'*** {e.message}')
        if 'FRALGOREPL' not in os.environ:
          print(f'-v- Ligne {self.lineno}')
          sys.exit(666)
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
  # def __add__(self, other):
  #   self.append(other)

class Declare:
  def __init__(self, name, var_type):
    self.name = name
    self.var_type = var_type
  def eval(self):
    if isinstance(self.var_type, tuple): # sized char
      sym.declare_sized_char(self.name, self.var_type[1])
    else:
      sym.declare_var(self.name, self.var_type)
  def __repr__(self):
    return f'Variable {self.name} en {self.var_type}'

class DeclareArray:
  def __init__(self, name, var_type, *max_indexes):
    self.name = name
    self.var_type = var_type
    self.max_indexes = max_indexes
  def eval(self):
    sym.declare_array(self.name, self.var_type, *self.max_indexes)
  def __repr__(self):
    indexes = [str(n) for n in self.max_indexes]
    idx = ', '.join(indexes)
    if idx == '-1':
      idx = ''
    return f'Tableau {self.name}[{idx}] en {self.var_type}'

class DeclareSizedChar:
  def __init__(self, name, size):
    self.name = name
    self.size = size
  def eval(self):
    sym.declare_sized_char(self.name, self.size)
  def __repr__(self):
    return f'Variable {self.name}*{self.size}'

class DeclareStruct:
  __types = ('Booléen', 'Caractère', 'Chaîne', 'Entier', 'Numérique')
  def __init__(self, name, fields):
    self.name = name
    self.fields = fields
  def eval(self):
    for field, datatype in self.fields:
      if datatype not in self.__types:
        if isinstance(datatype, tuple) or is_structure(datatype):
          continue
        raise BadType(f'Type invalide : {self.name}.{field} en >{datatype}<')
    declare_structure(Structure(self.name, self.fields))
  def __repr__(self):
    return f'Structure {self.name} {self.fields}'

class ArrayGetItem:
  def __init__(self, var, *indexes):
    self.var = var
    self.indexes = indexes
  def eval(self):
    try:
      var = self.var.eval()
    except AttributeError:
      var = sym.get_variable(self.var)
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

class StructureGetItem:
  def __init__(self, var, field):
    self.var = var
    self.field = field
  def eval(self):
    if isinstance(self.var, tuple):
      if len(self.var) > 1:
        structure = sym.get_variable(self.var[0])
        for f, field in enumerate(self.var):
          if f == 0:
            continue
          structure = structure.get_item(field)
        return structure.get_item(self.field)
    if isinstance(self.var, (ArrayGetItem, StructureGetItem)):
      var = self.var.eval()
    else:
      var = sym.get_variable(self.var)
    return var.get_item(self.field)
  def __repr__(self):
    return f'{self.var}.{self.field}'

class StructureSetItem:
  def __init__(self, var, field, value):
    self.var = var
    self.field = field
    self.value = value
  def eval(self):
    if isinstance(self.var, tuple):
      if len(self.var) > 1:
        structure = sym.get_variable(self.var[0])
        for f, field in enumerate(self.var):
          if f == 0:
            continue
          structure = structure.get_item(field)
        var = structure
    elif isinstance(self.var, (StructureGetItem, ArrayGetItem)):
      var = self.var.eval()
    else:
      var = sym.get_variable(self.var)
    if isinstance (self.value, list):
      var.set_value(self.value, None)
    else:
      var.set_value(self.value.eval(), self.field)
  def __repr__(self):
    return f'{self.var}.{self.field} ← {self.value}'

class Function:
  '''A function definition'''
  ftype = 'Fonction'
  def __init__(self, name, params, body, return_type):
    self.name = name # str
    self.params = params # [(name, datatype)]
    self.body = body # Node
    self.return_type = return_type # str
    if return_type is None:
      self.ftype = 'Procédure'
  def eval(self):
    sym.declare_function(self)
  def __repr__(self):
    params = [f'{param} en {datatype}' for param, datatype in self.params]
    return f'{self.ftype} {self.name}({", ".join(params)}) en {self.return_type}'

class FunctionCall:
  '''Function call'''
  def __init__(self, name, params):
    self.name = name
    self.params = params
  def eval(self):
    func = sym.get_function(self.name)
    params = func.params
    # check parameter count
    if self.params is not None:
      if len(self.params) != len(params):
        a = len(self.params) # actual
        x = len(params) # expected
        raise FuncInvalidParameterCount(f'Nombre de paramètres invalide : {a}, attendu {x} ')
      # check data types
      for i, p in enumerate(self.params):
        if isinstance(p, (BinOp, Node)):
          p = map_type(p.eval())
        if p.data_type != params[i][1]:
          raise BadType(f'Type invalide : >{params[i][0]}< type {params[i][1]} attendu')
      values = [param.eval() for param in self.params]
      # set variables
      sym.set_local()
      for i, p in enumerate(params):
        n, t = p
        sym.declare_var(n, t)
        sym.assign_value(n, values[i])
    # function body
    body = func.body
    try:
      result = body.eval()
      if result is not None:
        return map_type(result).eval()
    except FralgoException as e:
      raise e
    finally:
      if self.params is not None:
        sym.del_local()
    return result
  def __repr__(self):
    params = [str(param) for param in self.params]
    return f'{self.name}({", ".join(params)})'

class FunctionReturn:
  def __init__(self, expression):
    self.expression = expression
  def eval(self):
    return self.expression.eval()
  def __repr__(self):
    return f'Retourne {self.expression}'

class Assign:
  def __init__(self, var, value):
    self.var = var
    self.value = value
  def eval(self):
    value = self.value
    sym.assign_value(self.var, value.eval())
  def __repr__(self):
    return f'{self.var} ← {self.value}'

class Variable:
  def __init__(self, name):
    self.name = name
  def eval(self):
    var = sym.get_variable(self.name)
    if isinstance(var, (Boolean, Number, String)):
      return var.eval()
    return var
  def __repr__(self):
    try:
      value = sym.get_variable(self.name)
      return f'{self.name} → {value}'
    except (VarUndeclared, VarUndefined):
      return f'{self.name} → ?'
  @property
  def data_type(self):
    var = sym.get_variable(self.name, is_global=not sym.is_local())
    return var.data_type

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
      var = sym.get_variable(self.var)
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
    if self.op == 'dp':
      return map_type(a % b == 0)
    if self.op == '&':
      if isinstance(a, str) and isinstance(b, str):
        return a + b
      raise BadType('C & C : Type Chaîne attendu')
    if self.b is None:
      return op(a)
    if isinstance(a, str) and isinstance(b, str) and self.op not in comp:
      raise BadType(f'E|N {self.op} E|N : Type Entier ou Numérique attendu')
    try:
      return op(a, b)
    except TypeError:
      raise BadType('Opération sur des types incompatibles')
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
      result = self.dothis.eval()
      if result is not None:
        return result
    elif self.dothat is not None:
      result = self.dothat.eval()
      if result is not None:
        return result
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
    sym.assign_value(self.var, i)
    while i <= end if step > 0 else i >= end:
      try:
        result = self.dothis.eval()
        if result is not None:
          return result
      except FralgoException as e:
        raise e
      except KeyboardInterrupt:
        raise InterruptedByUser('Interrompu par l\'utilisateur')
      i += step
      sym.assign_value(self.var, i)
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
    exp = algo_to_python(self.exp)
    start = algo_to_python(self.start)
    length = algo_to_python(self.length)
    if not isinstance(exp, str):
      raise BadType('Extraire(>C<, E, E) : Type Chaîne attendu')
    if not isinstance(start, int):
      raise BadType('Extraire(C, >E<, E) : Type Entier attendu')
    if not isinstance(length, int):
      raise BadType('Extraire(C, E, >E<) : Type Entier attendu')
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
      raise BadType(f'{self.cmd}(>C<, E) : Type Chaîne attendu')
    if not isinstance(length, int):
      raise BadType(f'{self.cmd}(C, >E<) : Type Entier attendu')
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
      raise BadType('Trouve(>C<, C) : Type Chaîne attendu')
    except TypeError:
      raise BadType('Trouve(C, >C<) : Type Chaîne attendu')
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
      var = sym.get_variable(self.var)
    value = fd.read()
    var.set_value(value)
  def __repr__(self):
    return f'LireFichier {self.fd_number}, {self.var}'

class WriteFile:
  def __init__(self, fd, var):
    self.fd_number = fd
    self.var = var
  def eval(self):
    fd = get_file_descriptor(self.fd_number.eval())
    if fd is None:
      raise FatalError(f'Pas de fichier affecté au canal {self.fd_number}')
    return fd.write(str(self.var.eval()))
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
      raise BadType('Car(>E<) : Type Entier attendu')
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
      raise BadType('CodeCar(>C<) : Type Chaîne attendu')
    if len(value) != 1:
      raise BadType('CodeCar(>C<) : Chaîne de longueur 1 attendue')
    return ord(value)
  def __repr__(self):
    return f'CodeCar({self.value})'
  @property
  def data_type(self):
    return 'Entier'

class ToInteger:
  def __init__(self, value):
    self.value = value
  def eval(self):
    value = self.value.eval()
    try:
      return int(value)
    except ValueError:
      raise BadType(f'Entier(>N|C<) : Conversion de >{value}< impossible')
  def __repr__(self):
    return f'Entier({self.value})'
  @property
  def data_type(self):
    return 'Entier'

class ToFloat:
  def __init__(self, value):
    self.value = value
  def eval(self):
    value = self.value.eval()
    try:
      return float(value)
    except ValueError:
      raise BadType(f'Entier(>E|C<) : Conversion de >{value}< impossible')
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
    try:
      return str(value)
    except ValueError:
      raise BadType(f'Chaîne(>E|N<) : Conversion de >{value}< impossible')
  def __repr__(self):
    return f'Chaîne({self.value})'
  @property
  def data_type(self):
    return 'Chaîne'

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
      raise BadType('Dormir(E|N) : Type Entier ou Numérique attendu')
  def __repr__(self):
    return f'Dormir({self.duration})'

def algo_to_python(expression):
  '''
  Evaluate an Algo expression to a Python type
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
      Random,
      String,
      StructureGetItem,
      ToFloat, ToInteger, ToString, Trim,
      Variable,
  )
  exp = expression
  while isinstance(exp, types):
    exp = exp.eval()
  return exp
