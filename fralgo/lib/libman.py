'''Library Manager'''

import os

from fralgo.lib.exceptions import FatalError

class LibMan:
  def __init__(self, parser=None, mainfile=None):
    self.parser = None
    self.mainfile = None
  def set_main(self, mainfile=None):
    self.mainfile = mainfile
    if mainfile is not None:
      self.__path = os.path.abspath(mainfile)
    else:
      self.__path = os.getcwd()
  def set_parser(self, parser):
    self.parser = parser
  def import_lib(self, libfile):
    libpath = os.path.join(self.path, libfile + '.algo')
    try:
      with open(libpath, 'r') as f:
        lib = f.readlines()
    except FileNotFoundError:
      name = os.path.basename(libpath)
      raise FatalError(f'Importer : fichier {name} non trouvé')
    try:
      self.checklib(lib)
    except FatalError as e:
      print(f'*** Importer : fichier {libfile}')
      raise e
    statements = self.parser.parse(''.join(lib))
    statements.eval()
  def checklib(self, algocontent):
    for line in algocontent:
      if 'Début' in line:
        raise FatalError('Importer : ceci n\' est pas une librairie.')
  @property
  def path(self):
    return self.__path
