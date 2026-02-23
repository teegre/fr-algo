'''File'''
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

from fralgo.lib.exceptions import FatalError

__file_descriptors = [None,None,None,None,None,None,None,None,None,None]

def get_file_descriptor(fd_number):
  try:
    fd = __file_descriptors[fd_number-1]
  except IndexError:
    raise FatalError(f'Numéro de canal invalide : {fd_number}')
  return fd

def new_file_descriptor(fd_number):
  fd = __file_descriptors[fd_number-1]
  if fd is not None:
    if fd.state != -1:
      raise FatalError(f'Canal {fd_number} déjà utilisé')
  new_fd = FileDescriptor(fd_number-1)
  __file_descriptors[fd_number-1] = new_fd
  return new_fd

def clear_file_descriptor(fd_number):
  fd = __file_descriptors[fd_number-1]
  if fd is not None:
    if fd.state == -1:
      __file_descriptors[fd_number-1] = None
    else:
      raise FatalError(f'Fichier ouvert sur le canal {fd_number}')
  else:
    raise FatalError(f'Canal {fd_number} non utilisé')

class FileDescriptor:
  def __init__(self, fd):
    self.fd = fd
    self.filename = None
    self.__file = None
  def open_file(self, filename, access_mode):
    if self.__file is not None:
      raise FatalError(f'Un fichier est déjà affecté au canal {self.fd}')
    self.filename = filename
    self.__file = File()
    try:
      self.__file.open(self.filename, access_mode)
    except FatalError as e:
      del self.__file
      self.__file = None
      raise e
  def close_file(self):
    if self.__file is None:
      raise FatalError(f'Aucun fichier affecté au canal {self.fd}')
    self.__file.close()
    del self.__file
    self.__file = None
  def read(self):
    return self.__file.read()
  def write(self, buffer):
    self.__file.write(buffer)
  def __repr__(self):
    return f'Canal {self.fd}'
  @property
  def eof(self):
    return self.__file.eof
  @property
  def state(self):
    if self.__file is not None:
      return self.__file.state
    return -1

class File:
  __mode = [None, 'r', 'w', 'a']
  def __init__(self):
    self.__file = None
    self.__state = 0
    self.__access_mode = 0
    self.__buffer = []
  def open(self, filename, access_mode):
    try:
      self.__file = open(filename, self.__mode[access_mode], encoding='utf-8')
    except FileNotFoundError:
      raise FatalError(f'Fichier non trouvé : {filename}')
    self.__access_mode = access_mode
    self.__state = 1
    if access_mode == 1:
      try:
        self.__buffer = self.__file.read().splitlines()
      except UnicodeDecodeError:
        raise FatalError(f'Pas un fichier texte : {filename}')
  def close(self):
    if self.__state == 1:
      try:
        self.__file.close()
        self.__state = 0
      except AttributeError:
        raise FatalError('Le fichier n\'a pas pu être fermé.')
    else:
      raise FatalError('Le fichier n\'est pas ouvert')
  def read(self):
    if self.__access_mode in (2, 3):
      raise FatalError('Le fichier n\'est pas en mode Lecture')
    try:
      return self.__buffer.pop(0)
    except IndexError:
      raise FatalError('La fin du fichier a été atteinte')
  def write(self, buffer):
    if self.__access_mode == 1:
      raise FatalError('Impossible d\'écrire dans un fichier en mode Lecture')
    bytes_written = self.__file.write(buffer + '\n')
    self.__file.flush()
    return bytes_written
  @property
  def state(self):
    return self.__state
  @property
  def eof(self):
    return len(self.__buffer) == 0
