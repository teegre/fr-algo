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

from datatypes import init_variable_data_type, map_type, Boolean

class Statements:
  def __init__(self):
    self.children = []
  def eval(self):
    for statement in self:
      statement.eval()
  def append(self, value):
    if value is not None:
      self.children.append(value)
  def __getitem__(self, index):
    return self.children[index]
  def __iter__(self):
    return iter(self.children)
  def __len__(self):
    return len(self.children)
  def __repr__(self):
    return f'{self.children}'

class Variable:
  def __init__(self, name, data_type):
    self.name = name
    self.data = init_variable_data_type(data_type)
  def eval(self):
    if isinstance(self.data, Boolean):
      return self.data
    return self.data.eval()
  def set_value(self, value):
    self.data.set_value(value)
  def __repr__(self):
    if self.data.value is not None:
      return f'{self.name} = {str(self.data)}'
    return f'{self.name} en {self.data.data_type}'

class Print:
  def __init__(self, data):
    self.data = data
  def eval(self):
    result = []
    for element in self.data:
      if isinstance(element, Boolean):
        result.append(str(element))
      else:
        result.append(str(map_type(element).eval()))
    print(''.join(result))
  def __repr__(self):
    return f'Ecrire {self.data}'
