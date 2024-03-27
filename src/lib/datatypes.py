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

from lib.exceptions import BadType, VarUndefined, IndexOutOfRange, ArrayResizeFailed

class Base():
  _type = 'Base'
  value = None
  def eval(self):
    raise NotImplementedError
  def set_value(self, value):
    raise NotImplementedError
  def __repr__(self):
    if self.value is None:
      return f'{self.data_type}'
    return f'{self.data_type} → {self.value}'
  @property
  def data_type(self):
    return self._type

class Number(Base):
  def set_value(self, value):
    raise NotImplementedError
  def eval(self):
    if self.value is None:
      raise VarUndefined('valeur indéfinie')
    return self.value
  def __str__(self):
    if self.value is None:
      raise VarUndefined('valeur indéfinie')
    return f'{self.value}'
  def __repr__(self):
    if self.value is None:
      return f'{self.data_type} → ?'
    return str(f'{self.data_type} → {self.value}')

class Integer(Number):
  _type = 'Entier'
  def __init__(self, value):
    self.value = value
  def set_value(self, value):
    if isinstance(value, int):
      self.value = value
    elif isinstance(value, Integer):
      self.value = value.eval()
    else:
      raise BadType(f'type {self.data_type} attendu [{self.value}]')

class Float(Number):
  _type = 'Numérique'
  def __init__(self, value):
    self.value = value
  def set_value(self, value):
    if isinstance(value, float):
      self.value = value
    elif isinstance(value, Float):
      self.value = value.eval()
    else:
      raise BadType(f'type {self.data_type} attendu [{self.value}]')

class String(Base):
  _type = 'Chaîne'
  def __init__(self, value):
    self.value = value
  def set_value(self, value):
    if isinstance(value, str):
      self.value = value
    else:
      raise BadType(f'type {self.data_type} attendu [{self.value}]')
  def eval(self):
    if self.value is None:
      raise VarUndefined('valeur indéfinie')
    return self.value
  def __repr__(self):
    if self.value is None:
      return f'{self.data_type} → ?'
    return f'{self.data_type} → "{self.value}"'

class Array(Base):
  _type = 'Tableau'
  def __init__(self, datatype, *indexes):
    # http://cours.pise.info/algo/tableaux.htm
    # http://cours.pise.info/algo/tableauxmulti.htm
    self.datatype = datatype # array content type
    self.indexes = indexes # max index(es)
    self.sizes = tuple(idx + 1 for idx in indexes) # size(s)
    self.value = self._new_array(*self.sizes)
  def _new_array(self, *sizes):
    if len(sizes) == 0:
      return []
    if len(sizes) == 1:
      return [None] * sizes[0]
    else:
      return [self._new_array(*sizes[1:]) for _ in range(sizes[0])]
  def _validate_index(self, index):
    if len(index) != len(self.sizes):
      raise VarUndefined('tableau non dimensionné')
    for i, size in enumerate(self.indexes):
      if size < 0 or size >= self.indexes[i] + 1:
        raise IndexOutOfRange('index hors limite')
  def eval(self):
    if self.value:
      return self.value
    raise VarUndefined('valeur indéfinie')
  def get_item(self, index):
    if isinstance(index, int):
      self._validate_index((index,))
      return self.value[index]
    elif isinstance(index, tuple):
      self._validate_index(index)
      array = self.value
      for i in index:
        array = array[i]
      return array
    else:
      raise BadType('type de données de l\'index invalide')
  def set_value(self, index, value):
    if self.value == []:
      raise VarUndefined('tableau non dimensionné')
    typed_value = map_type(value)
    if typed_value.data_type != self.datatype:
      raise BadType(f'type {self.datatype} attendu')
    self._validate_index(index)
    array = self.value
    for i in index[:-1]:
      array = array[i]
    array[index[-1]] = map_type(value)
  def redim(self, *indexes):
    self.indexes = indexes
    self.sizes = tuple(idx + 1 for idx in indexes)
    self.value = self._new_array(*self.sizes)
  def __repr__(self):
    def recursive_repr(array):
      if isinstance(array, list):
        return '[' + ', '.join(recursive_repr(item) for item in array) + ']'
      else:
        return '?' if array is None else str(array)
    return recursive_repr(self.value)
  def __str__(self):
    return self.__repr__()

# class Array(Base):
#   _type = 'Tableau'
#   def __init__(self, datatype, *max_indexes):
#     self.size = len(max_indexes) if list(max_indexes) != [-1] else 0
#     self.max_indexes = list(max_indexes)
#     self.datatype = datatype
#     if self.size == 0:
#       self.value = []
#     else:
#       self.value = []
#       for idx in max_indexes:
#         value = [None for _ in range(idx + 1)]
#         self.value += [value] if self.size > 1 else value
#   def eval(self):
#     if self.value:
#       return self.value
#     raise VarUndefined('valeur indéfinie')
#   def redim(self, size, *indexes):
#     array = self.get_item(*indexes)
#     if not isinstance(array, list):
#       raise BadType('type Tableau attendu')
#     if len(array) == 0:
#       raise VarUndefined('tableau non dimensionné')
#     if size < self.size or size < 0:
#       raise ArrayResizeFailed(f'{size} < {self.size} redimensionnement impossible')
#     value = [None for _ in range(len(array), size + 1)]
#     self.max_indexes[indexes[-1]] = Integer(size)
#     array += value
#   def get_item(self, *indexes):
#     item = self.value
#     if len(indexes) > 0:
#       for index in indexes:
#         try:
#           item = item[index.eval()]
#         except IndexError as e:
#           raise IndexOutOfRange(f'{index}, indice hors limite') from e
#         if item is None:
#           raise VarUndefined('valeur indéfinie')
#     return item
#   def set_value(self, value, *args, **kwargs):
#     '''set_value(value, list_index1, list_index2, ..., item_index)'''
#     if self.size == 0:
#       raise VarUndefined('tableau non dimensionné')
#     array = self.get_item(*args[:-1])
#     typed_value = map_type(value)
#     if typed_value.data_type != self.datatype:
#       raise BadType(f'type {self.datatype} attendu')
#     try:
#       array[args[-1].eval()] = typed_value
#     except IndexError as e:
#       raise IndexOutOfRange(f'{args[0]}, indice hors limite') from e
#   def __str__(self):
#     array = [item.eval() for item in self.value if item is not None]
#     return f'{array}'
#   def __repr__(self):
#     value = ['?' if v is None else v.eval() for v in self.value]
#     return f'{self.data_type}{self.max_indexes} en {self.datatype} {value}'

class Boolean(Base):
  _type = 'Booléen'
  def __init__(self, value):
    self.value = value
  def set_value(self, value):
    if value not in (True, False):
      raise BadType(f'type {self.data_type} attendu [{self.value}]')
    self.value = value
  def eval(self):
    if self.value is None:
      raise VarUndefined('valeur indéfinie')
    return self.value
  def __str__(self):
    if self.value is not None:
      return 'VRAI' if self.value is True else 'FAUX'
    return f'{self.data_type}'
  def __repr__(self):
    if self.value is None:
      return f'{self.data_type} → ?'
    return f'{self.data_type} → VRAI' if self.value else f'{self.data_type} → FAUX'

def map_type(value):
  '''Convert Python type to an Algo type'''
  if isinstance(value, int) and not isinstance(value, bool):
    return Integer(value)
  if isinstance(value, float):
    return Float(value)
  if isinstance(value, bool):
    return Boolean(value)
  if isinstance(value, str):
    return String(value)
  return value
