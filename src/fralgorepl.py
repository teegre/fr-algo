#! /usr/bin/env python
import sys
import readline
from algoparser import parser, reset

def repl():
  loop = False
  instructions = []

  while True:
    try:
      if loop:
        prompt = '... '
      else:
        prompt = '::> '
      instruction = input(prompt)
      if instruction:
        inst = instruction.split()
        if inst[0] in ('TantQue', 'Pour', 'Si', 'Sinon', 'SinonSi'):
          loop = True
        if inst[-1] == 'Suivant' or inst[0] in ('FinTantQue', 'FinSi'):
          loop = False
          instructions.append(instruction)
          instruction = '\n'.join(instructions)
          instructions = []
        if loop:
          instructions.append(instruction)
          continue
        else:
          result = parser.parse(instruction + '\n').eval()
          if result:
            print(result)
      else:
        loop = False
        instructions = []
        continue
    except EOFError:
      print()
      print('*** Au revoir !')
      sys.exit(0)
    except KeyboardInterrupt:
      try:
        reset()
      except:
        pass
      print()
      print('*** les variables ont été détruites.')
    except Exception as e:
      print(e)

if __name__ == '__main__':
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
