import os
import sys
import readline
from pathlib import Path
import traceback

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fralgo import __version__
from fralgo.fralgoparse import parser
from fralgo.lib.datatypes import map_type
from fralgo.lib.ast import sym
from fralgo.lib.exceptions import FralgoException

os.environ['FRALGOREPL'] = '1'
user_path = os.path.expanduser('~')
history_file = os.path.join(user_path, '.fralgohistory')

class Interpreter:
  start_hook = ('Fonction', 'Procédure', 'TantQue', 'Pour', 'Si', 'Sinon', 'SinonSi', 'Structure')
  loop_hook = ('Fonction', 'Procédure', 'TantQue', 'Pour', 'Si', 'Structure')
  while_end_hook = 'Suivant'
  end_hook = ('FinTantQue', 'FinSi', 'FinStructure', 'FinFonction', 'FinProcédure')
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
          sym.reset()
          print('*** Reinitialisation effectuée')
          continue
        case 'Début':
          print('*** Instructions Début et Fin non admises en mode interpréteur')
          continue
        case 'Fin':
          print('*** Instructions Début et Fin non admises en mode interpréteur')
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
      print(e.message)
      return
    except Exception as e:
      if self.traceback:
        traceback.print_exc()
      parser.restart()
      print(e)
      return
    if result is None:
      return
    try:
      result = result.eval()
    except FralgoException as e:
      print(e.message)
      return
    except Exception as e:
      if self.traceback:
        traceback.print_exc()
      parser.restart()
      print(e)
    if isinstance(result, bool):
      print(map_type(result))
    elif result is not None:
      try:
        print(result)
      except Exception as e:
        if self.traceback:
          traceback.print_exc()
        print(e)
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
  print(r' _______ ______ _______ _____   _______ _______ ')
  print(r'|    ___|   __ \   _   |     |_|     __|       |')
  print(r'|    ___|      <       |       |    |  |   -   |')
  print(r'|___|   |___|__|___|___|_______|_______|_______|')
  print(f'A L G O R I T H M E S                   {__version__}mg')
  print()
  print('Bonjour,', os.getenv('USER').capitalize(), '!')
  print('En attente de vos instructions.')
  print()
  repl = Interpreter()
  repl.input_loop()

if __name__ == '__main__':
  main()
