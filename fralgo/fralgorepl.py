'''REPL'''
#  _______ ______        _______ _____   _______ _______
# |    ___|   __ \______|   _   |     |_|     __|       |
# |    ___|      <______|       |       |    |  |   -   |
# |___|   |___|__|      |___|___|_______|_______|_______|
#
# Copyright © 2024 Stéphane MEYER (teegre)
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
import sys
import readline
from time import sleep
from pathlib import Path
import traceback

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fralgo import __version__
from fralgo.fralgoparse import parser
from fralgo.lib.datatypes import map_type
from fralgo.lib.ast import namespaces, libs
from fralgo.lib.exceptions import FralgoException, print_err

os.environ['FRALGOREPL'] = '1'
user_path = os.path.expanduser('~')
history_file = os.path.join(user_path, '.fralgohistory')

class Interpreter:
  start_hook = ('Fonction', 'Table', 'Procédure', 'TantQue', 'Pour', 'Si', 'Sinon', 'SinonSi', 'Structure')
  loop_hook = ('Fonction', 'Table', 'Procédure', 'TantQue', 'Pour', 'Si', 'Structure')
  while_end_hook = 'Suivant'
  end_hook = ('FinTantQue', 'FinSi', 'FinTable', 'FinStructure', 'FinFonction', 'FinProcédure')
  def __init__(self):
    self.loop = False
    self.cancel = False
    self.traceback = False
    self.instructions = []
    self.level = 0
    try:
      readline.read_history_file(history_file)
    except FileNotFoundError:
      Path(history_file).touch(mode=0o600)
  def input_loop(self):
    while True:
      try:
        print('\033[?25h\033[0m', end='')
        instruction = input(self.set_prompt())
      except KeyboardInterrupt:
        print()
        self.cancel = self.loop
        self.loop = False
        self.level = 0
        self.instructions.clear()
        continue
      except EOFError:
        print()
        print('*** Au revoir,', os.getenv('USER').capitalize(), '!')
        readline.write_history_file(history_file)
        sys.exit(0)
      match instruction:
        case 'TRACE':
          self.traceback = not self.traceback
          print('*** TRACE est', map_type(self.traceback))
          continue
        case 'REINIT':
          namespaces.reset()
          print('*** Reinitialisation effectuée')
          continue
      if instruction in ('Début', 'Fin', 'Librairie', 'Initialise'):
        print('*** Instruction non admise en mode interpréteur.')
        continue

      result = self.proceed(instruction)
      if result is None:
        continue
      self.parse(result)
  def proceed(self, instruction):
    if instruction:
      inst = instruction.split()
      if inst[0] in self.start_hook:
        self.loop = True
      if inst[0] in self.loop_hook:
        self.level += 1
      if inst[-1] == self.while_end_hook or inst[0] in self.end_hook:
        self.level -= 1
        if self.level == 0:
          self.loop = False
          self.instructions.append(instruction)
          instruction = '\n'.join(self.instructions)
          self.instructions.clear()
          return instruction
      if self.loop:
        self.instructions.append(instruction)
        return None
      return instruction
    self.cancel = self.loop
    self.loop = False
    self.level = 0
    self.instructions.clear()
    return None
  def parse(self, instruction):
    try:
      result = parser.parse(instruction + '\n')
    except FralgoException as e:
      if e.message:
        print_err(e.message)
      return
    except Exception as e:
      if self.traceback:
        traceback.print_exc()
      parser.restart()
      print_err(e)
      return
    if result is None:
      return
    try:
      result = result.eval()
    except FralgoException as e:
      if e.message:
        print_err(e.message)
      return
    except Exception as e:
      if self.traceback:
        traceback.print_exc()
      parser.restart()
      print_err(e)
    if isinstance(result, bool):
      print('---', map_type(result))
    elif result is not None:
      try:
        print('---', result)
      except Exception as e:
        if self.traceback:
          traceback.print_exc()
        print_err(e)
    return
  def set_prompt(self):
    if self.loop:
      return '... '
    if self.cancel:
      self.cancel = False
      return ':x: '
    return '::: '

def main():
  readline.parse_and_bind(r'"[" "\C-v[]\e[D"')
  readline.parse_and_bind(r'"(" "\C-v()\e[D"')
  print(r' _______ ______        _______ _____   _______ _______',  flush=True)
  sleep(0.0625)
  print(r'|    ___|   __ \______|   _   |     |_|     __|       |', flush=True)
  sleep(0.0625)
  print(r'|    ___|      <______|       |       |    |  |   -   |', flush=True)
  sleep(0.0625)
  print(r'|___|   |___|__|      |___|___|_______|_______|_______|', flush=True)
  sleep(0.0625)
  version = f'fr-v100 {__version__}mg'
  print('|A|L|G|O|R|I|T|H|M|E|S|'.ljust(55-len(version)) + version)
  print()
  sleep(0.0625)
  print()
  print('(c) 2024 Stéphane MEYER (Teegre)', flush=True)
  sleep(0.0625)
  print()
  print('Bonjour,', os.getenv('USER').capitalize(), '!')
  print('En attente de vos instructions.')
  print()
  libs.set_main()
  repl = Interpreter()
  repl.input_loop()

if __name__ == '__main__':
  main()
