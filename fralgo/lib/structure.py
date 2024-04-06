'''Structure type'''
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

from fralgo.lib.datatypes import Boolean, Char, Float, Integer, String

class Structure:
  '''Structure skeleton'''
  _type = 'Structure'
  def __init__(self, name, fields):
    self.name =  name
    self.fields = fields # list of names and types
    self._type = name
  def __iter__(self):
    return iter(self.fields)
  def __repr__(self):
    return f'{self.name} {", ".join(str(field) for field in self.fields)}'
  @property
  def data_type(self):
    return self.name

class StructureData:
  _type = 'Structure'
  def __init__(self, structure):
    self.structure = structure
    self.name = structure.name
    self.data = self._new_structure_data()
  def eval(self):
    return self
  def set_value(self, value, fieldname=None):
    if fieldname is not None:
      self.data[fieldname].set_value(value)
    else:
      for i, name in enumerate(self.data):
        self.data[name].set_value(value[i])
  def get_item(self, name):
    return self.data[name]
  def _new_structure_data(self):
    data = {}
    for name, datatype in self.structure:
      if datatype == 'Booléen':
        data[name] = Boolean(None)
      elif isinstance(datatype, (list, tuple)):
        if datatype[0] == 'Caractère':
          data[name] = Char(None, datatype[1])
      elif datatype == 'Chaîne':
        data[name] = String(None)
      elif datatype == 'Entier':
        data[name] = Integer(None)
      elif datatype == 'Numérique':
        data[name] = Float(None)
    return data
  def __repr__(self):
    return f'{self.name} {", ".join(k+" "+str(v) for k,v in self.data.items())}'
