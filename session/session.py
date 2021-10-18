from disk_access_utils.directory_manager import grant_access, check_disk
from disk_access_utils.user_manager import exec_command
from session.messages import messages
import sys
sys.path.append('../')
from system_stats import DISK_NAME

def logout(signum, frame):
  messages['LOGOUT']()
  check_disk()
  exit(1)

def init_session(user):
  grant_access(user)
  cur_path = DISK_NAME
  while True:
    cmd = input(f'{user.login}@{cur_path} > ')
    if cmd == 'logout':
      user.signed_in = False
      logout(None, None)
    cmd_name = cmd.split()[0]
    cmd_last_arg = cmd.split()[-1]
    if (
      cmd_name in ('cd', 'ls') and
      cmd_last_arg.startswith('..')
    ):
      if len(cmd_last_arg.split('/')) >= len(cur_path.split('/')):
        messages['NO_PARENT_DIR']()
        continue
    cmd_res = None
    try: cmd_res = exec_command(cmd, user.admin, cur_path)
    except FileNotFoundError:
      messages['NOT_FOUND']()
      continue
    if cmd_name == 'cd' and cmd_res.returncode == 0:
      if cmd_last_arg.startswith('..'):
        step = len(cmd_last_arg.split('/'))
        cur_path = '/'.join(cur_path.split('/')[:-step])
      else: cur_path = f'{cur_path}/{cmd_last_arg}'
    is_err = cmd_res.returncode != 0
    permission_err = 'Permission denied' in cmd_res.stderr.decode("utf-8")
    if is_err and permission_err: messages['NO_PERMISSION']()
    elif is_err: print(cmd_res.stderr.decode("utf-8")[:-1])
    else: print(cmd_res.stdout.decode("utf-8")[:-1])
