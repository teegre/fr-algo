''' Algo data types '''
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

from fralgo.lib.exceptions import BadType, VarUndefined, IndexOutOfRange, ArrayResizeFailed

class Base():
  _type = 'Base'
  value = None
  def eval(self):
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
      raise VarUndefined('Valeur indéfinie')
    return self.value
  def __str__(self):
    if self.value is None:
      raise VarUndefined('Valeur indéfinie')
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
      raise BadType(f'Type {self.data_type} attendu [{value}]')

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
      raise BadType(f'Type {self.data_type} attendu [{value}]')

class String(Base):
  _type = 'Chaîne'
  def __init__(self, value):
    self.value = value
  def set_value(self, value):
    if isinstance(value, str):
      self.value = value
    else:
      raise BadType(f'Type {self.data_type} attendu [{value}]')
  def eval(self):
    if self.value is None:
      raise VarUndefined('Valeur indéfinie')
    return self.value
  def __repr__(self):
    if self.value is None:
      return '?'
    return f'"{self.value}"'

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
    return [self._new_array(*sizes[1:]) for _ in range(sizes[0])]
  def _validate_index(self, index):
    if len(index) != len(self.sizes):
      raise VarUndefined('Tableau non dimensionné')
    for i, size in enumerate(index):
      if size < 0 or size >= self.indexes[i] + 1:
        raise IndexOutOfRange('Index hors limite')
  def eval(self):
    if self.value:
      return self.value
    raise VarUndefined('Valeur indéfinie')
  def _eval_indexes(self, *indexes):
    '''Evaluate indexes until we get integers (int)'''
    idxs = []
    for index in indexes:
      idx = index
      while not isinstance(idx, int):
        idx = idx.eval()
      idxs.append(idx)
    return tuple(idxs)
  def get_item(self, *indexes):
    idxs = self._eval_indexes(*indexes)
    self._validate_index(idxs)
    array = self.value
    for i in idxs:
      array = array[i]
    return array
  def set_value(self, indexes, value):
    typed_value = map_type(value.eval())
    while not isinstance(typed_value, (Boolean, Number, String)):
      typed_value = map_type(typed_value)
    if typed_value.data_type != self.datatype:
      raise BadType(f'Type {self.datatype} attendu')
    idxs = self._eval_indexes(*indexes)
    self._validate_index(idxs)
    array = self.value
    for i in idxs[:-1]:
      array = array[i]
    array[idxs[-1]] = value.eval()
  def _indexes_to_copy(self, old, new):
    '''
    Generator yielding indexes for copying values
    into a resized Array.
    '''
    if len(old) == 1:
      for size in range(min(old[0], new[0])):
        yield (size,)
    else:
      for size in range(min(old[0], new[0])):
        for sizes in self._indexes_to_copy(old[1:], new[1:]):
          yield (size,) + sizes
  def resize(self, *indexes):
    ''' Resize an Array '''
    idxs = self._eval_indexes(*indexes)
    for i, idx in enumerate(self.indexes):
      if idxs[i] < 0:
        raise ArrayResizeFailed('Redimensionnement impossible')
    sizes = tuple(idx + 1 for idx in idxs)
    new_array = Array(self.datatype, *idxs)
    for idx in self._indexes_to_copy(self.sizes, sizes):
      value = self.get_item(*idx)
      if value is None:
        continue
      new_array.set_value(idx, map_type(value))
    self.indexes = idxs
    self.sizes = sizes
    self.indexes = idxs
    self.value = new_array.value
  def __repr__(self):
    def recursive_repr(array):
      if isinstance(array, list):
        return '[' + ', '.join(recursive_repr(item) for item in array) + ']'
      return '?' if array is None else str(map_type(array))
    return recursive_repr(self.value)
  def __str__(self):
    return self.__repr__()
  @property
  def size(self):
    return self.sizes

class Boolean(Base):
  _type = 'Booléen'
  def __init__(self, value):
    if value in ('VRAI', 'FAUX'):
      self.value = value == 'VRAI'
    else:
      self.value = value
  def set_value(self, value):
    if value not in (True, False):
      raise BadType(f'Type {self.data_type} attendu [{value}]')
    self.value = value
  def eval(self):
    if self.value is None:
      raise VarUndefined('Valeur indéfinie')
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
