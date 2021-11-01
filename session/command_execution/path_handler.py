from os.path import abspath
from system_stats import DISK_NAME, PERMITTED_SUBDISKS

def manage_cd_permissions(path, cd_arg):
  inside_subdir = False
  for disk in PERMITTED_SUBDISKS:
    full_cd_path = abspath(f'{path}/{cd_arg}')
    parent = abspath(f'{DISK_NAME}/{disk}')
    if parent in full_cd_path: inside_subdir = True
  return inside_subdir or is_root_dir(path, cd_arg)

def is_root_dir(path, cmd_arg):
  return abspath(f'{path}/{cmd_arg}') == abspath(DISK_NAME)

def inside_root_dir(cmd_path, path):
  full_cmd_path = abspath(f'{path}/{cmd_path}')
  full_root_path = abspath(DISK_NAME)
  return full_root_path in full_cmd_path

def get_new_path(cmd_path, path):
  full_cmd_path = abspath(f'{path}/{cmd_path}')
  split_path = full_cmd_path.split('/')
  root_idx = split_path.index(DISK_NAME)
  new_path = ('/').join(split_path[root_idx:])
  return new_path

def target_root_dir(cmd, path):
  split_cmd = cmd.split()
  no_dir_arg = all(f.startswith('-') for f in split_cmd[1:])
  return (
    ((len(split_cmd) == 1 or no_dir_arg) and path == DISK_NAME) or
    is_root_dir(path, split_cmd[-1])
  ) 
  