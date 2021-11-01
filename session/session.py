import os
import time
import threading
from session.command_execution.commands import handle_cmd
from session.stochastic_verification.verify import *
from utils.directory_manager import grant_access
from utils.logout import logout
from utils.wrapped_input import wrapped_input
from system_stats import DISK_NAME, QUESTIONS_INTERVAL_MIN

ASK = False
ANSWER = ''
NOT_ANSWERED = False

def question(user):
  global ASK, ANSWER, NOT_ANSWERED
  while True:
    time.sleep(QUESTIONS_INTERVAL_MIN * 60)
    if NOT_ANSWERED:
      handle_no_answer(user)
      logout()
    ASK = True
    ANSWER = ask(user)
    NOT_ANSWERED = True

def init_session(user):
  grant_access(user)
  cur_path = DISK_NAME
  intercepted_commands = {
    'whoami': lambda: print(user.login),
    'pwd': lambda: print(cur_path),
    'clear': lambda: os.system('clear'),
    'logout': logout
  }
  global ASK, ANSWER, NOT_ANSWERED
  t = threading.Thread(target=question, args=(user,))
  t.start()
  while True:
    inp = wrapped_input(f'{user.login}@{cur_path} > ')
    if ASK:
      ASK = False
      NOT_ANSWERED = False
      verified = verify(user, ANSWER, inp)
      if not verified: logout()
    else:
      cmd_res = handle_cmd(inp, cur_path, user, intercepted_commands)
      if cmd_res is not None: cur_path = cmd_res
