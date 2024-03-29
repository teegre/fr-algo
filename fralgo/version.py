import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import platform
from fralgo import __version__

def get_version():
  return (f'fralgo {__version__}',
          f'python {platform.python_version()}')
