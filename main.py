from signal import signal, SIGINT
from disk_access_utils.directory_manager import check_disk
from auth.auth import login
from session.session import init_session, logout
from disk_access_utils.user_manager import *

def main():
  check_disk()
  signal(SIGINT, logout)
  user = login()
  init_session(user)

if __name__ == "__main__":
  main() 
