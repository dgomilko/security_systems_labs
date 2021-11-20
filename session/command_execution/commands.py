
from session.command_execution.messages import messages
from session.command_execution.user_manager import exec_command
from session.command_execution.path_handler import *
from system_stats import PERMITTED_SUBDISKS
from encryption.crypto import encrypt, encrypt_file, decrypt_file
from system_stats import USER_KEYS_PATH

decode_and_print = lambda res: print(res.decode("utf-8")[:-1])

def execute(cmd, user, path):
  cmd_res = None
  cmd_split = cmd.split()
  cmd_name = cmd_split[0]
  last_arg = cmd_split[-1]
  admin = user.admin or cmd_name == 'cd' and manage_cd_permissions(path, last_arg)
  try: cmd_res = exec_command(cmd, admin, path)
  except FileNotFoundError: messages['NOT_FOUND']()
  return cmd_res 

def manage_res(cmd_res):
  is_err = cmd_res.returncode != 0
  permission_err = 'Permission denied' in cmd_res.stderr.decode("utf-8")
  if is_err and permission_err: messages['NO_PERMISSION']()
  elif is_err: decode_and_print(cmd_res.stderr)
  else: decode_and_print(cmd_res.stdout)
  return permission_err

def crypto_cmd(file, path, login, encrypt=True):
  if len(file) != 1: return messages['ONE_ARG']()
  f = file[0]
  if not is_file(path, f): return messages['FILE_ARG']()
  if not inside_permitted_dir(path, f):
    messages['NO_PERMISSION']()
    return True
  full_path = f'{path}/{f}'
  if encrypt: res = encrypt_file(full_path, USER_KEYS_PATH, login)
  else: res = decrypt_file(full_path, USER_KEYS_PATH, login)
  if res is None: messages['CRYPTO_ERR']()

def handle_root_ls(cmd, user, path):
  res = execute(cmd, user, path)
  if res is None: return None
  if user.admin or res.returncode: return manage_res(res)
  all_disks = res.stdout.decode("utf-8")[:-1].split('\n')
  out = list(filter(lambda a: a.split()[-1] in PERMITTED_SUBDISKS, all_disks))
  print('\n'.join(out))

def handle_cmd(cmd, cur_path, user, intercepted):
  if not len(cmd): return None
  split_cmd = cmd.split()
  cmd_name = split_cmd[0]
  cmd_args = split_cmd[1:]
  cmd_last_arg = split_cmd[-1]
  if cmd_name in intercepted.keys():
    intercepted[cmd_name](cmd_args)
    return None
  if cmd_name in ('encrypt', 'decrypt'):
    encrypt = cmd_name == 'encrypt'
    permission_err = crypto_cmd(cmd_args, cur_path, user.login, encrypt)
    return (cur_path, permission_err)
  if cmd_name in ('ls', 'cd') and not inside_root_dir(cmd_last_arg, cur_path): 
    messages['NO_PARENT_DIR']()
    return None
  if cmd_name == 'ls' and target_root_dir(cmd, cur_path):
    permission_err = handle_root_ls(cmd, user, cur_path)
    return (cur_path, permission_err)
  cmd_res = execute(cmd, user, cur_path)
  if cmd_res is None: return None
  if cmd_name == 'cd' and cmd_res.returncode == 0:
    cur_path = get_new_path(cmd_last_arg, cur_path)
  permission_err = manage_res(cmd_res)
  return (cur_path, permission_err)
