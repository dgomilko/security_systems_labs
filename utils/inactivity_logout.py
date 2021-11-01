from threading import Timer
from system_stats import SESSION_TIMEOUT_SEC
from utils.logout import logout

t = Timer(SESSION_TIMEOUT_SEC, logout)
t.start()
def on_exit_delayed(_):
  global t
  t.cancel()
  t = Timer(SESSION_TIMEOUT_SEC, logout)
  t.start()
