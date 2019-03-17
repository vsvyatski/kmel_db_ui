import sys
import os

_current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(_current_dir, '..', 'src')))

from info import APP_VERSION


if __name__ == '__main__':
    print(APP_VERSION)
