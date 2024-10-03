'''Algo data types'''
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
from copy import deepcopy

from fralgo.lib.exceptions import BadType, VarUndefined, VarUndeclared, IndexOutOfRange
from fralgo.lib.exceptions import ArrayResizeFailed, InvalidCharacterSize
from fralgo.lib.exceptions import InvalidStructureValueCount, UnknownStructureField

class Base():
  _type = 'Base'
  value = None
  def eval(self):
    raise NotImplementedError
  def __repr__(self):
    if self.value is None:
      return f'{self.data_type} → ?'
    return f'{self.data_type} → {self.value}'
  @property
  def is_empty(self):
    return self.value is None
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
      return '?'
      # raise VarUndefined('Valeur indéfinie')
    return f'{self.value}'
  def __eq__(self, other):
    if isinstance(other, Number):
      return self.value == other.value
    return False
  def __ne__(self, other):
    if isinstance(other, Number):
      return self.value != other.value
    return False
  def __gt__(self, other):
    if isinstance(other, Number):
      return self.value > other.value
    return False
  def __ge__(self, other):
    if isinstance(other, Number):
      return self.value >= other.value
    return False
  def __lt__(self, other):
    if isinstance(other, Number):
      return self.value < other.value
    return False
  def __le__(self, other):
    if isinstance(other, Number):
      return self.value <= other.value
    return False
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
    elif isinstance(value, String):
      self.value = value.eval()
    else:
      raise BadType(f'Type {self.data_type} attendu [{value}]')
  def eval(self):
    if self.value is None:
      raise VarUndefined('Valeur indéfinie')
    return self.value
  def __len__(self):
    return len(self.value)
  def __eq__(self, other):
    if isinstance(other, String):
      return self.value == other.value
    return False
  def __ne__(self, other):
    if isinstance(other, String):
      return self.value != other.value
    return False
  def __gt__(self, other):
    if isinstance(other, String):
      return self.value > other.value
    return False
  def __ge__(self, other):
    if isinstance(other, String):
      return self.value >= other.value
    return False
  def __lt__(self, other):
    if isinstance(other, String):
      return self.value < other.value
    return False
  def __le__(self, other):
    if isinstance(other, String):
      return self.value <= other.value
    return False
  def __str__(self):
    if self.value is None:
      return '?'
    return self.value
  def __repr__(self):
    if self.value is None:
      return '?'
    return f'"{self.value}"'

class Char(String):
  _type = 'Caractère'
  def __init__(self, value, size=Integer(1)):
    super().__init__(value)
    self.size = map_type(size)
    sz = self.size.eval()
    if sz > 255 or sz < 1:
      raise InvalidCharacterSize(f'Taille invalide : {sz}')
    if self.value is not None:
      self.set_value(value)
  def set_value(self, value):
    size = self.size.eval()
    val = value
    if not isinstance(val, (str, int, float, bool, list, tuple, Char, String)):
      val = value.eval()
    if isinstance(value, (Char, String)):
      val = value.eval()
    try:
      if len(val) < size:
        self.value = val.ljust(size, ' ')
      else:
        self.value = val[:size]
    except TypeError:
      raise BadType('Type Caractère attendu')
  def eval(self):
    if self.value is None:
      raise VarUndefined('Valeur indéfinie')
    return self.value
  def __repr__(self):
    if self.value is None:
      return '?'
    return f'"{self.value}"'
  @property
  def data_type(self):
    return (self._type, self.size.eval())


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
  def __eq__(self, other):
    if isinstance(other, Boolean):
      return self.value == other.value
    return False
  def __ne__(self, other):
    if isinstance(other, Boolean):
      return self.value != other.value
    return False
  def __gt__(self, other):
    if isinstance(other, Boolean):
      return self.value > other.value
    return False
  def __ge__(self, other):
    if isinstance(other, Boolean):
      return self.value >= other.value
    return False
  def __lt__(self, other):
    if isinstance(other, Boolean):
      return self.value < other.value
    return False
  def __le__(self, other):
    if isinstance(other, Boolean):
      return self.value <= other.value
    return False
  def __str__(self):
    if self.value is not None:
      return 'VRAI' if self.value is True else 'FAUX'
    return f'{self.data_type}'
  def __repr__(self):
    if self.value is None:
      return f'{self.data_type} → ?'
    return f'{self.data_type} → VRAI' if self.value else f'{self.data_type} → FAUX'

class Array(Base):
  _type = 'Tableau'
  def __init__(self, datatype, *indexes):
    # http://cours.pise.info/algo/tableaux.htm
    # http://cours.pise.info/algo/tableauxmulti.htm
    self.datatype = datatype # array content type
    self.indexes = indexes # max index(es)
    self.sizes = tuple(idx + 1 for idx in indexes) # size(s)
    self.value = None
    self.get_structure = None
  def set_get_structure(self, get_structure_func):
    self.get_structure = get_structure_func
  def new_array(self, *sizes):
    if len(sizes) == 0:
      return []
    if len(sizes) == 1:
      datatype = _get_type(self.datatype, self.get_structure)
      if isinstance(datatype, (list, tuple)):
        if issubclass(datatype[0], StructureData):
          data = [datatype[0](datatype[1]) for _ in range(sizes[0])]
          for struct in data:
            struct.set_get_structure(self.get_structure)
            struct.data = struct.new_structure_data()
          return data
        # sized Char
        return [datatype[0](None, datatype[1])] * sizes[0]
      # Basic type / structure
      return [datatype(None)] * sizes[0]
    return [self.new_array(*sizes[1:]) for _ in range(sizes[0])]
  def _validate_index(self, index):
    if len(index) != len(self.sizes):
      raise VarUndefined('Index invalide')
    for i, size in enumerate(index):
      if size < 0 or size >= self.indexes[i] + 1:
        raise IndexOutOfRange(f'Index hors limite : {size}')
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
        try:
          idx = idx.eval()
        except AttributeError:
          raise BadType('Index manquant')
      idxs.append(idx)
    return tuple(idxs)
  def get_item(self, *indexes):
    idxs = self._eval_indexes(*indexes)
    self._validate_index(idxs)
    array = self.value
    for i in idxs:
      array = array[i]
    return array
  def set_array(self, array, ref=False):
    '''
    self ← array
    self ← &array
    '''
    if self.sizes != array.sizes:
      raise BadType('Tableaux de taille differentes')
    if self.datatype != array.datatype:
      raise BadType(f'Type {self.datatype} attendu [{array.datatype}]')
    # /!\ Not implemented in grammar.
    # References are only available in procedure.
    if ref:
      self.indexes = array.indexes
      self.sizes = array.sizes
      self.value = array.value
    else:
      self.indexes = deepcopy(array.indexes)
      self.sizes = deepcopy(array.sizes)
      self.value = deepcopy(array.value)
  def set_value(self, indexes, value):
    datatype = self.datatype
    if isinstance(datatype, tuple): # sized char
      typed_value = Char(value.eval(), datatype[1])
      datatype = self.datatype
    if isinstance(value, list) and (
        indexes == [] or indexes == (None,) or indexes == ()): # sequence to array
      if len(self.sizes) > 1:
        raise BadType('Interdit : Affectation directe de valeurs à un tableau multidimensionnel')
      if len(self.indexes) == 1 and self.indexes[0] == -1:
        raise BadType('Tableau non dimensionné')
      if self.sizes[0] != len(value):
        raise BadType('Nombre de valeurs invalide')
      array = self.new_array(len(value))
      for i, n in enumerate(value):
        try:
          if n.data_type != datatype:
            raise BadType(f'Type {datatype} attendu')
        except AttributeError:
          nn = map_type(n.eval())
          if nn.data_type != datatype:
            raise BadType(f'Type {datatype} attendu')
        array[i] = n.eval()
      self.value = array
      return
    if value is None:
      raise BadType('Erreur de syntaxe : [] manquants')
    typed_value = map_type(value.eval())
    if typed_value.data_type != datatype:
      raise BadType(f'Type {datatype} attendu ({typed_value.data_type})')
    idxs = self._eval_indexes(*indexes)
    self._validate_index(idxs)
    array = self.value
    for i in idxs[:-1]:
      array = array[i]
    # /!\ deepcopy StructureData
    if isinstance(typed_value, StructureData):
      array[idxs[-1]] = deepcopy(typed_value)
    else:
      array[idxs[-1]] = typed_value.eval()
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
    sizes = tuple(idx + 1 for idx in idxs)
    array = Array(self.datatype, *idxs)
    array.set_get_structure(self.get_structure)
    array.value = array.new_array(*array.sizes)
    if self.is_empty():
      self.indexes = idxs
      self.sizes = sizes
      self.value = array.value
      return
    for i, idx in enumerate(self.indexes):
      try:
        if idxs[i] < 0:
          raise ArrayResizeFailed('Redimensionnement impossible')
      except IndexError:
        raise ArrayResizeFailed('Redimensionnement impossible')
    for idx in self._indexes_to_copy(self.sizes, sizes):
      value = self.get_item(*idx)
      if value is None:
        continue
      if isinstance(value, StructureData):
        value = deepcopy(value)
      array.set_value(idx, map_type(value))
    self.indexes = idxs
    self.sizes = sizes
    self.value = array.value
  def is_empty(self, array=None):
    if array is not None:
      for item in array:
        if isinstance(item, list):
          return self.is_empty(item)
        if not map_type(item).is_empty:
          return False
    else:
      for item in self.value:
        if isinstance(item, list):
          return self.is_empty(item)
        if not map_type(item).is_empty:
          return False
    return True
  def __eq__(self,  other):
    if isinstance(other, Array):
      return self.value == other.value
    return False
  def __ne__(self, other):
    if isinstance(other, Array):
      return self.value != other.value
    return False
  def __gt__(self, other):
    if isinstance(other, Array):
      return self.value > other.value
    return False
  def __ge__(self, other):
    if isinstance(other, Array):
      return self.value >= other.value
    return False
  def __lt__(self, other):
    if isinstance(other, Array):
      return self.value < other.value
    return False
  def __le__(self, other):
    if isinstance(other, Array):
      return self.value <= other.value
    return False
  def __repr__(self):
    def recursive_repr(array):
      if isinstance(array, list):
        return '[' + ', '.join(recursive_repr(item) for item in array) + ']'
      return '?' if array is None else str(map_type(array))
    return recursive_repr(self.value)
  def __str__(self):
    return str(self.value)
  @property
  def size(self):
    if len(self.sizes) == 1:
      if self.indexes[0] == -1:
        return map_type(0)
      return map_type(self.sizes[0])
    array = Array('Entier', len(self.sizes) - 1)
    array.set_get_structure(self.get_structure)
    array.new_array(*array.sizes)
    for idx, value in enumerate(self.sizes):
      array.set_value((idx,), Integer(value))
    return array
  @property
  def data_type(self):
    if len(self.indexes) == 1:
      indexes = self.indexes[0]
    else:
      indexes = self.indexes
    return (self._type, self.datatype, indexes)

class Structure(Base):
  '''Structure skeleton'''
  _type = 'Structure'
  def __init__(self, name, fields):
    self.name =  name
    self.fields = fields # list of names and types
    self._type = name
  def eval(self):
    return NotImplemented
  def __iter__(self):
    return iter(self.fields)
  def __repr__(self):
    return f'{self.name} {", ".join(str(field) for field in self.fields)}'
  @property
  def data_type(self):
    return self.name

class StructureData(Base):
  ''' A Structure instance '''
  _type = 'StructureData'
  def __init__(self, structure):
    self.structure = structure
    self.name = structure.name
    self.data = None
    self.get_structure = None
  def set_get_structure(self, get_structure_func):
    self.get_structure = get_structure_func
  def eval(self):
    return self
  def f_eval(self):
    data = [str(v.eval()) for v in self.data.values()]
    return ''.join(data)
  def set_value(self, value, fieldname=None):
    if fieldname is not None:
      if isinstance(fieldname, tuple): # Array!
        name, indexes = fieldname
        if indexes is None:
          if isinstance(value, list):
            self.data[name].set_value([], value)
          else:
            self.data[name].set_value(indexes, map_type(value))
        else:
          self.data[name].set_value(indexes, map_type(value))
      else:
        try:
          self.data[fieldname].set_value(value)
        except KeyError:
          raise UnknownStructureField(f'{fieldname} ne fait pas partie de {self.name}')
    else:
      if isinstance(value, StructureData):
        if value.name == self.name:
          self.data = deepcopy(value.data)
        else:
          raise BadType(f'{value.name} n\'est pas {self.name}')
      else:
        try:
          if len(value) != len(self.data):
            raise InvalidStructureValueCount(f'{self.name} nombre de valeurs invalide')
        except TypeError as e:
          print(e)
          # Dealing with a mono-field structure here
          if len(self.data) > 1 and isinstance(self.data, (list, tuple)):
            raise InvalidStructureValueCount(f'{self.name} nombre de valeurs invalide')
        for i, name in enumerate(self.data):
          try:
            if isinstance(self.data[name], StructureData):
              self.data[name].set_value(value, None)
            elif isinstance(self.data[name], Array):
              self.data[name].set_value(value, None)
            else:
              self.data[name].set_value(
                value[i].eval() if isinstance(value, (list, tuple)) else map_type(value))
          except TypeError as e:
            print(e)
            # Mono-field structure
            self.data[name].set_value(map_type(value).eval())
  def get_item(self, name):
    try:
      if isinstance(name, tuple): # Array!
        if name[0] in self.data.keys():
          return self.data[name[0]].get_item(name[1])
        raise VarUndefined(f'{name[0]} ne fait pas partie de {self.name}')
      if name in self.data.keys():
        if self.data[name] is None:
          raise VarUndefined(f'{self.name}.{name} : Valeur indéfinie')
        return self.data[name]
      raise UnknownStructureField(f'{name} ne fait pas partie de {self.name}')
    except TypeError:
      raise BadType(f'{self.name} : Type d\'accès invalide')
  def new_structure_data(self):
    data = {}
    for name, datatype in self.structure:
      data_type = _get_type(datatype, self.get_structure)
      if isinstance(data_type, (list, tuple)):
        if issubclass(data_type[0], StructureData):
          struct = StructureData(data_type[1])
          struct.set_get_structure(self.get_structure)
          struct.data = struct.new_structure_data()
          data[name] = struct
        elif issubclass(data_type[0], Array):
          array = Array(data_type[1], data_type[2])
          array.value = array.new_array(*array.sizes)
          array.set_get_structure(self.get_structure)
          data[name] = array
        else:
          data[name] = data_type[0](None, data_type[1])
      else:
        data[name] = data_type(None)
    return data
  def get_field_type(self, name):
    for field in self.structure.fields:
      if field[0] == name:
        return field[1]
    return None
  @property
  def is_empty(self):
    for element in self.data:
      if not map_type(element).is_empty:
        return False
    return True
  def __eq__(self, other):
    if isinstance(other, StructureData):
      return self.name == other.name and self.data == other.data
    return False
  def __str__(self):
    # if 'FRALGOREPL' in os.environ:
      # return self.__repr__()
    # else:
    data = [str(v.eval()) for v in self.data.values()]
    return ', '.join(data)
  def __repr__(self):
    data = [k+": " + str(v) for k,v in self.data.items()]
    return f'{self.name}: ({", ".join(data)})'
  @property
  def data_type(self):
    return self.name

class Table(Base):
  _type = 'Table'
  def __init__(self, key_type, value_type, value=None):
    self.key_type = key_type
    self.value_type = value_type
    self.value = {} if value is None else value
  def eval(self):
    return self
  def set_value(self, key, value):
    key = key[0]
    if key.data_type != self.key_type:
      raise BadType(f'Clef : Type {self.key_type} attendu')
    if value.data_type != self.value_type:
      raise BadType(f'Valeur : Type {self.value_type} attendu')
    self.value[key.eval()] = value.eval()
  def get_item(self, key):
    value = self.value.get(key.eval())
    if value is not None:
      return value
    raise VarUndefined('Valeur indéfinie')
  def get_keys(self):
    return self.value.keys()
  def get_values(self):
    return self.value.values()
  def __len__(self):
    return len(self.value)
  def __repr__(self):
    return f'({(", ".join(str(k) + ": " + str(v) for k, v in self.value.items()))})'

def _get_type(datatype, get_structure):
  __datatypes = {
    'Booléen': Boolean,
    'Caractère': Char,
    'Chaîne': String,
    'Entier': Integer,
    'Numérique': Float,
    'Tableau': Array,
    'Table': Table,
  }
  if isinstance(datatype, (list, tuple)):
    if datatype[0] == 'Caractère':
      return (Char, datatype[1])
    if datatype[0] == 'Tableau':
      return (Array, datatype[1], datatype[2])
  elif datatype in __datatypes.keys():
    return __datatypes[datatype]
  else:
    structure = get_structure(datatype)
    return (StructureData, structure)
  raise BadType(f'{datatype} : type de données inconnu')

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
