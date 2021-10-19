from signal import signal, SIGINT
from disk_access_utils.directory_manager import check_disk
from auth.auth import login
from session.session import init_session, logout
from disk_access_utils.user_manager import *
from inactivity_logout import on_exit_delayed
import keyboard

def main():
  check_disk()
  keyboard.on_press(on_exit_delayed)
  signal(SIGINT, logout)
  user = login()
  init_session(user) if user is not None else logout()

if __name__ == "__main__":
  main() 
