import os
from sys import stdin
from termios import tcflush, TCIFLUSH
from utils.directory_manager import check_disk

def logout(signum=None, frame=None):
  print('\nFinishing current session...\n')
  check_disk()
  tcflush(stdin, TCIFLUSH)
  os._exit(0)
