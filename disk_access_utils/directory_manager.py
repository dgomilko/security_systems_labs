import os
import stat
import pwd
import sys
sys.path.append('../')
from system_stats import DISK_NAME, USER_PERMISSIONS, ALL_SUBDISKS, PERMITTED_SUBDISKS

def create_dir_if_does_not_exist(path):
  if not os.path.exists(path): os.mkdir(path)

def chmod_if_not_equal(path, mode):
  if not oct(os.stat(path).st_mode) == mode:
    os.chmod(path, mode)

def chown_if_not_equal(path, uid, gid):
  cur_owner = pwd.getpwuid(os.stat(path).st_uid).pw_uid
  if cur_owner != uid: 
    print("dd")
    os.chown(path, uid, gid)

def check_disk():
  min_permissions = 0o42000
  create_dir_if_does_not_exist(DISK_NAME)
  for subdisk in ALL_SUBDISKS:
    path = f'{DISK_NAME}/{subdisk}'
    create_dir_if_does_not_exist(path)
    chown_if_not_equal(path, 0, 0)
    chmod_if_not_equal(path, min_permissions)
  chown_if_not_equal(DISK_NAME, 0, 0)
  chmod_if_not_equal(DISK_NAME, min_permissions)

def grant_access(user):
  is_admin = user.admin
  read_permission = stat.S_IRGRP | stat.S_IXGRP
  if not is_admin:
    chmod_if_not_equal(DISK_NAME, read_permission)
    for subdisk in PERMITTED_SUBDISKS:
      path = f'{DISK_NAME}/{subdisk}'
      chmod_if_not_equal(path, USER_PERMISSIONS)
  user.signed_in = True
