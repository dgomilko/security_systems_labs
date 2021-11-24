from signal import signal, SIGINT
from auth.auth import login
from session.session import init_session
from monitor.report import init_analyzer
from utils.directory_manager import check_disk
from utils.logout import logout
import keyboard
from threading import Timer
from system_stats import SESSION_TIMEOUT_SEC
from utils.logout import logout
from monitor.journal_manager import add_level_one_threat

def main():
  logged_user = '[unsigned user]'

  def on_inactivity():
    add_level_one_threat(logged_user)
    logout()

  t = Timer(SESSION_TIMEOUT_SEC, on_inactivity)
  t.start()

  def on_exit_delayed(_):
    nonlocal t
    t.cancel()
    t = Timer(SESSION_TIMEOUT_SEC, on_inactivity)
    t.start()

  check_disk()
  keyboard.on_press(on_exit_delayed)
  signal(SIGINT, logout)
  init_analyzer()
  user = login()
  logged_user = user.login
  init_session(user) if user is not None else logout()

if __name__ == "__main__":
  main() 
