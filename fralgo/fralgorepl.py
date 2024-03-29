#! /usr/bin/env python
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import readline
from fralgo.fralgoparse import parser, reset
from fralgo.lib.datatypes import map_type
from fralgo.lib.exceptions import FralgoException

def repl():
  loop = False
  cancel = False
  instructions = []
  level = 0

  while True:
    try:
      if loop:
        prompt = '... '
      elif cancel:
        prompt = 'xx> '
        cancel = False
      else:
        prompt = '::> '
      instruction = input(prompt)
      if instruction:
        inst = instruction.split()
        if inst[0] in ('Début', 'TantQue', 'Pour', 'Si', 'Sinon', 'SinonSi'):
          loop = True
        if  inst[0] in ('TantQue', 'Pour', 'Si'):
          level += 1
        if inst[-1] == 'Suivant' or inst[0] in ('FinTantQue', 'FinSi', 'Fin'):
          level -= 1
          if level == 0:
            loop = False
            instructions.append(instruction)
            instruction = '\n'.join(instructions)
            instructions = []
        if loop:
          instructions.append(instruction)
          continue
        try:
          result = parser.parse(instruction + '\n').eval()
          if isinstance(result, bool):
            print(map_type(result))
          elif result is not None:
            print(result)
        except FralgoException as e:
          print(e.message)
      else:
        cancel = loop
        loop = False
        level = 0
        instructions = []
        continue
    except EOFError:
      print()
      print('*** Au revoir !')
      sys.exit(0)
    except KeyboardInterrupt:
      print()
    except Exception as e:
      print(e)

def main():
  readline.parse_and_bind('"[" "\C-v[]\e[D"')
  readline.parse_and_bind('"(" "\C-v()\e[D"')
  print("  __           _             ")
  print(" / _|_ __ __ _| | __ _  ___  ")
  print("| |_| '__/ _` | |/ _` |/ _ \ ")
  print("|  _| | | (_| | | (_| | (_) |")
  print("|_| |_|  \__,_|_|\__, |\___/ ")
  print("ALGORITHMES      |___/ 500mg ")
  print()
  print('CTRL+d pour quitter.')
  repl()

if __name__ == '__main__':
  main()
