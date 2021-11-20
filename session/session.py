import os
import time
import threading
from session.command_execution.commands import handle_cmd
from session.stochastic_verification.verify import *
from utils.directory_manager import grant_access
from utils.logout import logout
from utils.wrapped_input import wrapped_input
from system_stats import DISK_NAME, QUESTIONS_INTERVAL_MIN
from monitor.journal_manager import add_level_two_threat, add_level_three_threat
from encryption.fft import fft_add, fft_pow, fft_multiply
from encryption.keys import generate_prime

ASK = False
ANSWER = ''
NOT_ANSWERED = False

def question(user):
  global ASK, ANSWER, NOT_ANSWERED
  while True:
    time.sleep(QUESTIONS_INTERVAL_MIN * 60)
    if NOT_ANSWERED:
      add_level_three_threat(user.login)
      handle_no_answer(user)
      logout()
    ASK = True
    ANSWER = ask(user)
    NOT_ANSWERED = True

def num(n):
  try: return int(n)
  except ValueError: return float(n)

def init_session(user):
  grant_access(user)
  cur_path = DISK_NAME
  fft_exec = lambda args, operation: print(
    operation(
      num(args[0]),
      num(args[1])
    ) if len(args) == 2 else 'Invalid arguments number' 
  )
  intercepted_commands = {
    'whoami': lambda _: print(user.login),
    'pwd': lambda _: print(cur_path),
    'clear': lambda _: os.system('clear'),
    'logout': logout,
    'fftadd': lambda args: fft_exec(args, fft_add),
    'fftmul': lambda args: fft_exec(args, fft_multiply),
    'fftpow': lambda args: fft_exec(args, fft_pow),
    'genprime': lambda _: print(generate_prime()),
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
      if not verified:
        add_level_three_threat(user.login)
        logout()
    else:
      cmd_res = handle_cmd(inp, cur_path, user, intercepted_commands)
      if cmd_res is None: continue
      (path, permission_err) = cmd_res
      cur_path = path
      if permission_err: add_level_two_threat(user.login)

