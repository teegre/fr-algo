#! /usr/bin/env python
import sys
from algoparser import parser, reset

if __name__ == '__main__':
  while True:
    try:
      instruction = input('ALGO> ')
      if instruction:
        parser.parse(instruction + '\n').eval()
      else:
        continue
    except EOFError:
      print()
      print('Au revoir !')
      sys.exit(0)
    except KeyboardInterrupt:
      reset()
      print()
      print('*** les variables ont été détruites.')
    except Exception as e:
      print(e)
