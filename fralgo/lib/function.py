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

from fralgo.lib.exceptions import FralgoException, BadType, VarUndeclared, FuncInvalidParameterCount

__functions = {}

class Function:
  '''A function definition'''
  _type = 'Fonction'
  def __init__(self, name, params, body, return_type):
    self.name = name # str
    self.params = params # [(name, datatype)]
    self.body = body # Node
    self.return_type = return_type # str
    if return_type is None:
      self._type = 'Procédure'
  def eval(self):
    declare_function(self.name, self.params, self.body, self.return_type)
  def __repr__(self):
    params = [f'{param} en {datatype}' for param, datatype in self.params]
    return f'{self.data_type} {self.name}({", ".join(params)}) en {self.return_type}'
  @property
  def data_type(self):
    return self._type

class FunctionCall:
  '''Function call'''
  _type = 'Fonction'
  __localvars = {}

  def __init__(self, name, params):
    self.name = name
    self.params = params
  def eval(self):
    function = get_function(self.name)
    params = function.params
    # Check parameter count
    if len(self.params) != len(params):
      raise FuncInvalidParameterCount('Nombre de paramètres invalide')
    # Type check
    for index, param in enumerate(self.params):
      if param.data_type != params[index][1]:
        raise BadType(f'{param.name},')
    sparams = [param.eval() for param in self.params]
    for index, param in enumerate(params):
      self.set_variable(param, sparams[index])
    body = function.body
    try:
      result = body.eval()
    except FralgoException as e:
      raise e
    finally:
      self.__localvars.clear()
    return result
  def set_variable(self, param, value):
    self.__localvars[param] = value
  def get_variable(self, name):
    return self.__localvars[name]
  def __repr__(self):
    params = [str(param) for param in self.params]
    return f'{self.name}({", ".join(params)})'

def declare_function(name, params, body, return_type):
  __functions[name] = Function(name, params, body, return_type)

def get_function(name):
  function = __functions.get(name, None)
  if function is None:
    raise VarUndeclared(f'Fonction {name} non déclarée')
  return function
