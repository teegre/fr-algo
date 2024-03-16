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

import exceptions as ex

class Base():
  _type = 'Base'
  def eval(self):
    raise NotImplementedError
  def set_value(self, value):
    raise NotImplementedError
  @property
  def data_type(self):
    return self._type

class Number(Base):
  def __init__(self, value):
    self.value = value
  def set_value(self, value):
    raise NotImplementedError
  def eval(self):
    if self.value is None:
      raise ex.VarUndefined('valeur indéfinie')
    return self.value
  def __repr__(self):
    return str(f'{self.data_type} → {self.value}')

class Integer(Number):
  _type = 'Entier'
  def set_value(self, value):
    if isinstance(value, int):
      self.value = value
    else:
      raise ex.BadType(f'type {self.data_type} attendu')

class Float(Number):
  _type = 'Numérique'
  def set_value(self, value):
    if isinstance(value, float):
      self.value = value
    else:
      raise ex.BadType(f'type {self.data_type} attendu')

class String(Base):
  _type = 'Chaîne'
  def __init__(self, value):
    self.value = value
  def set_value(self, value):
    if isinstance(value, str):
      self.value = value
    else:
      raise ex.BadType(f'type {self.data_type} attendu')
  def eval(self):
    if self.value is None:
      raise ex.VarUndefined('valeur indéfinie')
    return self.value
  def __repr__(self):
    return str(f'{self.data_type} → {self.value}')

class Boolean(Base):
  _type = 'Booléen'
  def __init__(self, value):
    self.value = value
  def set_value(self, value):
    if isinstance(value, bool):
      self.value = value
    else:
      raise ex.BadType(f'type {self.data_type} attendu')
  def eval(self):
    if self.value is None:
      raise ex.VarUndefined('valeur indéfinie')
    return self.value
  def __str__(self):
    if self.value is True:
      return 'VRAI'
    return 'FAUX'
  def __repr__(self):
    return f'{self.data_type} → {self.__str__()}'

def map_type(value):
  if isinstance(value, int) and not isinstance(value, bool):
    return Integer(value)
  if isinstance(value, float):
    return Float(value)
  if isinstance(value, bool):
    return Boolean(value)
  if isinstance(value, str):
    return String(value)
  raise ex.VarTypeUnknown(f'valeur de type inconnu {value} ???')

def init_variable_data_type(data_type):
  if data_type == 'Booléen':
    return Boolean(None)
  if data_type == 'Chaîne':
    return String(None)
  if data_type == 'Numérique':
    return Float(None)
  if data_type == 'Entier':
    return Integer(None)
  # ça n'arrivera jamais car l'utilisation d'un type inconnu
  # entraîne une erreur de syntaxe.
  raise ex.VarTypeUnknown(f'type inconnu {data_type} ???')
