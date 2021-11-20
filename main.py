from signal import signal, SIGINT
from auth.auth import login
from session.session import init_session
from monitor.report import init_analyzer
from utils.directory_manager import check_disk
from utils.logout import logout
from utils.inactivity_logout import on_exit_delayed
import keyboard

def main():
  check_disk()
  keyboard.on_press(on_exit_delayed)
  signal(SIGINT, logout)
  init_analyzer()
  user = login()
  init_session(user) if user is not None else logout()

if __name__ == "__main__":
  main() 
