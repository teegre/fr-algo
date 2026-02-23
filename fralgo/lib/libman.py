'''Library Manager'''
#  _______ ______        _______ _____   _______ _______
# |    ___|   __ \______|   _   |     |_|     __|       |
# |    ___|      <______|       |       |    |  |   -   |
# |___|   |___|__|      |___|___|_______|_______|_______|
#
# This file is part of FRALGO
# Copyright © 2024-2026 Stéphane MEYER (Teegre)
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

from fralgo.lib.exceptions import FralgoException, FatalError, print_err

class LibMan:
  def __init__(self):
    self.parser = None
    self.mainfile = None
    self.__path = None
    self.__local_lib_path = os.path.join(os.getenv("HOME"), '.local/lib/fralgo')
    self.namespaces = None
    self.imports = ['main']
  def set_main(self, mainfile=None):
    self.mainfile = mainfile
    if mainfile is not None:
      self.__path = os.path.dirname(os.path.abspath(mainfile))
    else:
      self.__path = os.getcwd()
  def set_lexer(self, lexer):
    self.lexer = lexer
  def set_parser(self, parser):
    self.parser = parser
  def set_namespaces(self, ns):
    self.namespaces = ns
  def import_lib(self, libfile, alias=None):
    libpath = os.path.join(self.path, libfile + '.algo')
    if not os.path.isfile(libpath):
      libpath = os.path.join(self.__local_lib_path, libfile + '.algo')
    try:
      with open(libpath, 'r', encoding='utf-8') as f:
        lib = f.readlines()
    except FileNotFoundError:
      name = os.path.basename(libpath)
      raise FatalError(f'Importer : fichier `{name}` non trouvé')
    try:
      self.checklib(lib, libfile)
    except FatalError as e:
      print_err(f'Librairie : {libfile}.algo')
      raise e
    if not alias:
      alias = os.path.basename(libfile)
    self.imports.append(alias)
    self.namespaces.declare_namespace(alias)
    try:
      statements = self.parser.parse(''.join(lib), lexer=self.lexer)
      statements.eval()
    except FralgoException as e:
      print_err(f'Librairie : {libfile}.algo')
      print_err(f'Ligne {self.lexer.lineno}')
      self.namespaces.del_namespace(alias)
      raise e
    finally:
      self.imports.pop()
      self.namespaces.set_current_namespace(self.imports[-1])
  def checklib(self, algocontent, libfile):
    start = False
    for line in algocontent:
      if 'Librairie\n' in line:
        start = True
        break
    if not start:
      raise FatalError(f'`{libfile}` n\'est pas une librairie.')
  @property
  def path(self):
    return self.__path
