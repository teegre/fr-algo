from exceptions import FatalError

__file_descriptors = [
    None,
    FileDescriptor(1),
    FileDescriptor(2),
    FileDescriptor(3),
    FileDescriptor(4),
    FileDescriptor(5),
    FileDescriptor(6),
    FileDescriptor(7),
    FileDescriptor(8),
    FileDescriptor(9),
    FileDescriptor(10),
]

def get_file_descriptor(fd):
  return __file_descriptors[fd]

class FileDescriptor:
  def __init__(self, fd):
    self.fd = fd
    self.filename = None
    self.__file = None
  def open_file(self, filename, access_mode):
    if self.__file is not None:
      raise FatalError(f'Un fichier est déjà affecté au canal {self.fd}')
    self.filename = filename
    self.__file = File()
    self.__file.open(self.filename, fd, access_mode)
  def close_file(self):
    if self.__file is None:
      raise FatalError(f'Aucun fichier affecté au canal {self.fd}')
    if self.__file.state == 0:
      raise FatalError(f'Fichier non ouvert')
    self.__file.close()
    delete(self.__file)
    self.__file = None
  def eof(self):
    return self.__file.eof

class File:
  __mode = [None, 'r', 'w', 'a']
  def __init__(self):
    self.__file = None
    self.__state = 0
    self.__access_mode = 0
    self.__eof = False
    self.__buffer = []
  def open(self, filename, fd, access_mode):
    try:
      self.__file = open(filename, self.__mode[access_mode])
    except FileNotFoundError:
      raise FatalError(f'Fichier non trouvé : {filename}')
    self.__access_mode = access_mode
    self.__state = 1
    self.__buffer = self.__file.read().splitlines()
  def close(self):
    if self.__state == 1:
      try:
        self.__file.close()
        self.__state = 0
      except AttributeError:
        raise FatalError('Le fichier n\'a pas pu être fermé.')
    raise FatalError('Le fichier n\'est pas ouvert')

  def read(self):
    if self.__access_mode in (2, 3):
      raise FatalError('Le fichier n\'est pas en mode Lecture')
    try:
      return self.__buffer.pop(0)
    except IndexError:
      self.__eof = True
  @property
  def state(self):
    return self.__state
  @property
  def eof(self):
    return self.__eof
