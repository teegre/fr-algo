#   __           _
#  / _|_ __ __ _| | __ _  ___
# | |_| '__/ _` | |/ _` |/ _ \
# |  _| | | (_| | | (_| | (_) |
# |_| |_|  \__,_|_|\__, |\___/
#                  |___/
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

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fralgo.fralgoparse import parser
from fralgo.lib.exceptions import FatalError

def main():
  try:
    with open(sys.argv[1], 'r') as f:
      prog = f.read()
      prog = prog[:-1]
  except FileNotFoundError:
    print('*** fichier non trouvé')
    sys.exit(1)
  except IndexError:
    print('fralgo <chemin/fichier.algo>')
    sys.exit(1)
  try:
    statements = parser.parse(prog)
    statements.eval()
  except FatalError:
    sys.exit(666)

if __name__ == "__main__":
  main()
