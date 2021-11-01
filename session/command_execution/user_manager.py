from pwd import getpwnam
from os import setuid
from subprocess import run, PIPE
from system_stats import OS_USERNAME

def check_user_exists(username):
  try:
    getpwnam(username)
  except KeyError:
    return False
  return True

def create_user_if_does_not_exist(username):
  if not check_user_exists(username):
    run(['useradd', '-r', username])

def change_os_user():
  create_user_if_does_not_exist(OS_USERNAME)
  uid = getpwnam(OS_USERNAME).pw_uid
  setuid(uid)

def exec_command(cmd, is_admin, dir):
  command = cmd.split()
  fn = None if is_admin else change_os_user
  res = run(command, stdout=PIPE, stderr=PIPE, preexec_fn=fn, cwd=dir)
  return res
