from fralgo.lib.exceptions import FatalError

__file_descriptors = [None,None,None,None,None,None,None,None,None,None,None]

def get_file_descriptor(fd_number):
  try:
    fd = __file_descriptors[fd_number]
  except IndexError:
    raise FatalError(f'Numéro de canal invalide : {fd_number}')
  return fd

def new_file_descriptor(fd_number):
  fd = __file_descriptors[fd_number]
  if fd is not None:
    # if 
    raise FatalError(f'Canal {fd} déjà utilisé')
  new_fd = FileDescriptor(fd)
  __file_descriptors[fd] = new_fd
  return new_fd

# def clear_file_descriptor(fd):


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
    try:
      self.__file.open(self.filename, access_mode)
    except FatalError as e:
      del self.__file
      self.__file = None
      __file_descriptors[self.fd] = None
      raise e
  def close_file(self):
    if self.__file is None:
      raise FatalError(f'Aucun fichier affecté au canal {self.fd}')
    self.__file.close()
    del self.__file
    self.__file = None
  def read(self):
    return self.__file.read()
  def __repr__(self):
    return f'Canal {self.fd}'
  @property
  def eof(self):
    return self.__file.eof
  @property
  def state(self):
    if self.__file is not None:
      return self.__file.state
    return -1

class File:
  __mode = [None, 'r', 'w', 'a']
  def __init__(self):
    self.__file = None
    self.__state = 0
    self.__access_mode = 0
    self.__buffer = []
  def open(self, filename, access_mode):
    try:
      self.__file = open(filename, self.__mode[access_mode], encoding='UTF-8')
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
    else:
      raise FatalError('Le fichier n\'est pas ouvert')
  def read(self):
    if self.__access_mode in (2, 3):
      raise FatalError('Le fichier n\'est pas en mode Lecture')
    try:
      return self.__buffer.pop(0)
    except IndexError:
      raise FatalError('La fin du fichier a été atteinte')
  @property
  def state(self):
    return self.__state
  @property
  def eof(self):
    return len(self.__buffer) == 0
