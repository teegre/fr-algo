import platform
from fralgo import __version__

def get_version():
  return (f'fralgo {__version__}',
          f'python {platform.python_version()}')
