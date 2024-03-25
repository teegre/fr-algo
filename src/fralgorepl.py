#! /usr/bin/env python
import sys
import readline
from algoparser import parser, reset

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

  while True:
    try:
      instruction = input('::> ')
      if instruction:
        parser.parse(instruction + '\n').eval()
      else:
        continue
    except EOFError:
      print()
      print('*** Au revoir !')
      sys.exit(0)
    except KeyboardInterrupt:
      reset()
      print()
      print('*** les variables ont été détruites.')
    except Exception as e:
      print(e)
