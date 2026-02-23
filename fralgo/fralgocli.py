''' File interpreter '''
#  _______ ______        _______ _____   _______ _______
# |    ___|   __ \______|   _   |     |_|     __|       |
# |    ___|      <______|       |       |    |  |   -   |
# |___|   |___|__|      |___|___|_______|_______|_______|
#
# Copyright © 2024-2026 Stéphane MEYER (teegre)
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
from time import sleep

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fralgo import __version__
from fralgo.lib.datatypes import map_type
from fralgo.fralgoparse import parser
from fralgo.lib.ast import libs, namespaces, FreeFormArray
from fralgo.lib.exceptions import FatalError, print_err

sym = namespaces.get_namespace('main')

def main():
  try:
    algofile = sys.argv[1]
    with open(algofile, 'r', encoding='utf-8') as f:
      prog = f.read()
      prog = prog[:-1]
  except FileNotFoundError:
    print_err(f'{algofile} : fichier non trouvé')
    sys.exit(1)
  except IndexError:
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
    print('(c) 2024-2026 Stéphane MEYER (Teegre)', flush=True)
    sleep(0.0625)
    print()
    sleep(0.0625)
    print()
    print('Donnez-moi un fichier ALGO en paramètre et je ferai de mon')
    print("mieux pour lire et exécuter les instructions qu'il contient.")
    print()
    print('Exemple : fralgo monfichier.algo')
    print()
    sys.exit(1)

  # Commandline arguments
  args = [map_type(sys.argv[1])]
  args += [map_type(arg) for arg in sys.argv[2:]]
  sym.declare_const('_ARGS', FreeFormArray(args), superglobal=True)

  # Current working directory
  rep = os.path.dirname(os.path.abspath(algofile))
  sym.declare_const('_REP', map_type(rep), superglobal=True)

  try:
    libs.set_main(algofile)
    statements = parser.parse(prog)
    statements.eval()
  except FatalError as e:
    print_err(f'Oh oh : {e.message}')
    print('\033[?25h\033[0m', end='')
    print('\033[?1049l')
    sys.exit(666)

if __name__ == "__main__":
  main()
