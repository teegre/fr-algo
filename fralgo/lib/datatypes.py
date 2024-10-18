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
from fralgo.lib.exceptions import ArrayInvalidSize, ArrayResizeFailed, InvalidCharacterSize
from fralgo.lib.exceptions import InvalidStructureValueCount, UnknownStructureField

class Base:
  _type = 'Base'
  value = None
  def eval(self):
    raise NotImplementedError
  def set_value(self, value):
    self.value = value
  def __repr__(self):
    if self.value is None:
      return f'{self.data_type} → ?'
    return f'{self.data_type} → {self.value}'
  @property
  def is_empty(self):
    return self.value is None or isinstance(self.value, Nothing)
  @property
  def data_type(self):
    return self._type

class Nothing:
  _type = 'Rien'
  value = None
  def eval(self):
    raise VarUndefined('Valeur indéfinie.')
  def __str__(self):
    return '?'
  def __repr__(self):
    return '?'
  def __bool__(self):
    return False
  def __eq__(self, other):
    isinstance(other, Nothing) or other is None
  def __lt__(self, other):
    return False
  def __le__(self, other):
    return False
  def __gt__(self, other):
    return False
  def __ge__(self, other):
    return False
  @property
  def data_type(self):
    return self._type

class Number(Base):
  def set_value(self, value):
    raise NotImplementedError
  def eval(self):
    return self.value.eval() if isinstance(self.value, Nothing) else self.value
  def __str__(self):
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
  def __bool__(self):
    if self.value is None or isinstance(self.value, Nothing) or self.value <= 0:
      return False
    return True
  def __repr__(self):
    if self.value is None:
      return '?'
    return str(self.value)

class Integer(Number):
  _type = 'Entier'
  def __init__(self, value):
    self.value = value if value is not None else Nothing()
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
    self.value = value if value is not None else Nothing()
  def set_value(self, value):
    if isinstance(value, float):
      self.value = value
    elif isinstance(value, int):
      self.value = float(value)
    elif isinstance(value, Number):
      self.value = float(value.eval())
    else:
      raise BadType(f'Type {self.data_type} attendu [{value}]')

class String(Base):
  _type = 'Chaîne'
  def __init__(self, value):
    self.value = value if value is not None else Nothing()
  def set_value(self, value):
    if isinstance(value, str):
      self.value = value
    elif isinstance(value, String):
      self.value = value.eval()
    else:
      raise BadType(f'Type {self.data_type} attendu [{value}]')
  def eval(self):
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
  def __bool__(self):
    if self.value is None or isinstance(self.value, Nothing) or self.value == '':
      return False
    return True
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
    if self.value is not None and not isinstance(self.value, Nothing):
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
    elif isinstance(value, bool):
      self.value = value
    else:
      self.value = Nothing()
  def set_value(self, value):
    if value not in (True, False):
      raise BadType(f'Type {self.data_type} attendu [{value}]')
    self.value = value
  def eval(self):
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
  def __bool__(self):
    if self.value is None or isinstance(self.value, Nothing):
      return False
    return self.value
  def __str__(self):
    if self.value is not None or not isinstance(self.value, Nothing):
      return 'VRAI' if self.value is True else 'FAUX'
    return '?'
  def __repr__(self):
    if self.value is None or isinstance(self.value, Nothing):
      return '?'
    return 'VRAI' if self.value else 'FAUX'

class Array(Base):
  _type = 'Tableau'

  @classmethod
  def get_datatype(cls, value):
    if isinstance(value, list) or issubclass(type(value), Array):
      return cls.get_datatype(value[0])
    return map_type(value).data_type
  @classmethod
  def check_types(cls, value, expected, datatype=None, index=None):
    if isinstance(value, list):
      for i, e in enumerate(value):
        if isinstance(e, list) or issubclass(type(e), Array):
          if index is None:
            cls.check_types(e, expected, datatype, (i,))
          else:
            cls.check_types(e, expected, datatype, index + (i,))
        else:
          if datatype is None:
            datatype = type(e)
          elif type(e) != datatype:
            indexes = ','.join(str(idx) for idx in index + (i,)) if index is not None else i
            badtype = map_type(e).data_type
            raise BadType(f'Type `{badtype}` invalide à l\'index [{indexes}] : attendu `{expected}`')
  @classmethod
  def get_indexes(cls, value):
    if (isinstance(value, list) or issubclass(type(value), Array)) and len(value) > 0:
      if isinstance(value[0], list) or issubclass(type(value[0]), Array):
        size = len(value[0]) - 1
        for idx, e in enumerate(value):
          if (isinstance(e, list) or issubclass(type(e), Array)) and size != len(e) - 1:
            raise ArrayInvalidSize(f'Taille invalide à l\'index {idx} : {len(e)} ({size+1})')
      return (len(value) - 1,) + cls.get_indexes(value[0])
    return ()

  @classmethod
  def multi_len(cls, value):
    count = 0
    if isinstance(value, list) or issubclass(type(value), Array):
      for e in value:
        count += cls.multi_len(e)
    else:
      if not isinstance(value.value, Nothing):
        count += 1
    return count

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
    return self
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
    if issubclass(type(array), Array):
      indexes = Array.get_indexes(array.value)
      datatype = Array.get_datatype(array.value)
      if datatype != self.datatype:
        raise BadType(f'Type `{self.datatype}` attendu [`{datatype}`]')
      Array.check_types(array.value, datatype)
      temparray = Array(datatype, *indexes)
      if self.sizes == temparray.sizes:
        self.indexes = indexes
        self.sizes = temparray.sizes
        self.value = deepcopy(array.value)
        return
      else:
        raise BadType(f'Nombre de valeurs invalide : {len(array.value)} ({len(self.value)})')
    try:
      if self.sizes != array.sizes:
        raise BadType(f'Nombre de valeurs invalide : {len(array)} ({len(self.value)}) ')
    except AttributeError:
      array = array.eval()
      if self.sizes != array.sizes:
        raise BadType(f'Nombre de valeurs invalide : {len(array)} ({len(self.value)}) ')
    if self.datatype != array.datatype and array.datatype != 'Quelconque':
      raise BadType(f'Type {self.datatype} attendu [{array.datatype}]')
    if ref:
      # /!\ Not implemented in grammar.
      # References are only available in procedure.
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
    if (isinstance(value, list) or issubclass(type(value), Array)) and indexes is None:
      if len(self.sizes) > 1:
        raise BadType('Interdit : Affectation directe de valeurs à un tableau multidimensionnel')
      if len(self.indexes) == 1 and self.indexes[0] == -1:
        raise BadType('Tableau non dimensionné')
      if self.sizes[0] != len(value):
        # check if elements are lists and check their lengths
        length = sum([len(ar.eval()) for ar in value if isinstance(ar.eval(), (Array, list))])
        if length != self.sizes[0]:
          raise BadType(f'Nombre de valeurs invalide : {len(value)} ({len(self.value)})')
        else:
          array = []
          for e in value:
            v = map_type(e)
            array += v.value if not isinstance(v, list) else v
          self.value = array
          return
        self.set_array(array)
        return
      array = self.new_array(len(value))
      for i, n in enumerate(value):
        try:
          if isinstance(n, Number) and datatype == 'Numérique':
            n = Float(float(n.eval()))
          elif isinstance(n, (int, float, bool, str)):
            n = map_type(n)
          if n.data_type != datatype:
            raise BadType(f'Type {datatype} attendu ({n.data_type})')
        except AttributeError:
          nn = map_type(n.eval())
          if nn.data_type != datatype:
            raise BadType(f'Type {datatype} attendu ({nn.data_type})')
        array[i] = map_type(n)
      self.value = array
      return
    if isinstance(value, Number) and datatype == 'Numérique':
      value = Float(float(value.eval()))
    if not issubclass(type(value), Array):
      typed_value = map_type(value.eval())
    else:
      typed_value = value
    if typed_value.data_type != datatype and datatype != 'Quelconque':
      raise BadType(f'Type {datatype} attendu [{repr_datatype(typed_value.data_type, shortform=False)}]')
    idxs = self._eval_indexes(*indexes)
    self._validate_index(idxs)
    array = self.value
    for i in idxs[:-1]:
      array = array[i]
    # /!\ deepcopy StructureData
    if isinstance(typed_value, StructureData):
      array[idxs[-1]] = deepcopy(typed_value)
    else:
      array[idxs[-1]] = typed_value
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
  def __len__(self):
    if len(self.sizes) == 1:
      return sum([1 if not isinstance(map_type(e).value, Nothing) else 0 for e in self.value])
    return Array.multi_len(self.value)

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
  def __bool__(self):
    return not self.is_empty()
  def __repr__(self):
    def recursive_repr(array):
      if isinstance(array, list):
        return '[' + ','.join(recursive_repr(item) for item in array) + ']'
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
    array.value = array.new_array(*array.sizes)
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
    data = [f'{n}{repr_datatype(t)}' for n, t in self.fields]
    return f'{self.name} → {",".join(data)}'
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
  def is_recursive(self):
    for field, datatype in self.structure.fields:
      if datatype == self.name:
        return True
    return False
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
          if isinstance(self.data[fieldname], Array):
            if isinstance(value, (list, Array)):
              self.data[fieldname].set_value(None, value)
          elif self.data[fieldname] is None: # recursive structure
            self.data[fieldname] = value
          else:
            self.data[fieldname].set_value(value)
        except KeyError:
          raise UnknownStructureField(f'`{fieldname}` ne fait pas partie de `{self.name}`')
    else:
      if isinstance(value, StructureData):
        if value.name == self.name:
          if self.is_recursive():
            self.data = value.data
          else:
            self.data = deepcopy(value.data)
        else:
          raise BadType(f'{value.name} n\'est pas {self.name}')
      else:
        try:
          if len(value) != len(self.data):
            raise InvalidStructureValueCount(f'{self.name} nombre de valeurs invalide')
        except TypeError as e:
          # Dealing with a mono-field structure here
          if len(self.data) > 1 and isinstance(self.data, (list, tuple)):
            raise InvalidStructureValueCount(f'{self.name} nombre de valeurs invalide')
        for i, name in enumerate(self.data):
          try:
            if isinstance(self.data[name], StructureData):
              self.data[name].set_value(value, None)
            elif self.data[name] is None:
              if value[i].data_type != self.name:
                raise BadType(f'Type {self.name} attendu [{value[i].data_type}]')
              self.data[name] = value[i].eval()
            elif isinstance(self.data[name], Array):
              self.data[name].set_array(value[i])
            else:
              self.data[name].set_value(
                value[i].eval() if isinstance(value, (list, tuple)) else map_type(value))
          except TypeError as e:
            # Mono-field structure
            self.data[name].set_value(map_type(value).eval())
  def get_item(self, name):
    try:
      if isinstance(name, tuple): # Array!
        if name[0] in self.data.keys():
          return self.data[name[0]].get_item(name[1])
        raise VarUndefined(f'{name[0]} ne fait pas partie de {self.name}')
      if name in self.data.keys():
        return self.data[name]
      raise UnknownStructureField(f'{name} ne fait pas partie de {self.name}')
    except TypeError:
      raise BadType(f'{self.name} : Type d\'accès invalide')
  def new_structure_data(self):
    data = {}
    for name, datatype in self.structure:
      data_type = _get_type(datatype, self.get_structure)
      if datatype == self.name:
        data[name] = None
      elif isinstance(data_type, (list, tuple)):
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
    data = [str(v) if v is not None else '?' for v in self.data.values()]
    return ','.join(data)
  def __repr__(self):
    data = [k+": " + str(v) if v else '?' for k,v in self.data.items()]
    return f'{self.name} → {",".join(data)}'
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
    return value
  def get_keys(self):
    return self.value.keys()
  def get_values(self):
    return self.value.values()
  def __len__(self):
    return len(self.value)
  def __repr__(self):
    return f'({(",".join(str(k) + ": " + str(v) for k, v in self.value.items()))})'

class Any(Base):
  def __init__(self, value=None):
    if value is not None:
      self.set_value(value)
    else:
      self.value = value
  def set_value(self, value):
    if isinstance(value, (bool, Boolean)):
      self.__class__ = Boolean
    elif isinstance(value, (int, Integer)):
      self.__class__ = Integer
    elif isinstance(value, (float, Float)):
      self.__class__ = Float
    elif isinstance(value, (str, String)):
      self.__class__ = String
    self.value = map_type(value)
  def __repr__(self):
    if self.value is None:
      return '? → ?'
    return f'{self.data_type} → {self.value}'

def _get_type(datatype, get_structure):
  __datatypes = {
    'Booléen': Boolean,
    'Caractère': Char,
    'Chaîne': String,
    'Entier': Integer,
    'Numérique': Float,
    'Tableau': Array,
    'Table': Table,
    'Quelconque': Any,
  }
  if isinstance(datatype, (tuple, list)):
    if datatype[0] == 'Caractère':
      return (Char, datatype[1])
    if datatype[0] == 'Tableau':
      return (Array, datatype[1], datatype[2])
  elif isinstance(datatype, list):
    structure = get_structure(datatype)
    return (StructureData, structure)
  elif datatype in __datatypes.keys():
    return __datatypes[datatype]
  structure = get_structure(datatype)
  if structure:
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
  if value is None:
    return Nothing()
  return value

def repr_datatype(datatype, shortform=True):
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
