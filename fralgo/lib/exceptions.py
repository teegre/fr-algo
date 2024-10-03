'''Exceptions'''
#  _______ ______        _______ _____   _______ _______
# |    ___|   __ \______|   _   |     |_|     __|       |
# |    ___|      <______|       |       |    |  |   -   |
# |___|   |___|__|      |___|___|_______|_______|_______|
#
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

from sys import stderr

class FralgoException(Exception):
  def __init__(self, message):
    self.message = message
  def __str__(self):
    return str(self.message)

def print_err(message):
  stderr.write(f'*** {message}\n')
  stderr.flush()

class VarUndeclared(FralgoException):
  '''Variable non déclarée.'''
class BadType(FralgoException):
  '''Le type de données n\'est pas conforme à celui attendu.'''
class VarRedeclared(FralgoException):
  '''La variable a déjà été déclarée.'''
class VarUndefined(FralgoException):
  '''Attention, ne jamais toucher à une variable vide...'''
  # ... même tombée à terre !
class InterruptedByUser(FralgoException):
  '''Le programme a été interrompu par l\'utilisateur. '''
class IndexOutOfRange(FralgoException):
  '''L\'indice du tableau n\'existe pas.'''
class ArrayResizeFailed(FralgoException):
  '''La taille d\'un tableau ne peut pas être inférieure à sa taille initiale.'''
class InvalidCharacterSize(FralgoException):
  '''Taille invalide.'''
class UnknownStructureField(FralgoException):
  '''Le champ n\'appartient pas à la structure.'''
class InvalidStructureValueCount(FralgoException):
  '''Le nombre de valeurs ne correspond pas au nombre de champs de la structure'''
class FatalError(FralgoException):
  ''' ERREUR FATALE '''
class ZeroDivide(FralgoException):
  ''' Division par 0 ! '''
class FuncInvalidParameterCount(FralgoException):
  '''Nombre de paramètres invalide'''
class FralgoInterruption(FralgoException):
  '''Exécution interrompue '''

