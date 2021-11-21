import os
from datetime import datetime
from encryption.keys import generate_key_pair, PUB_NAME, PRIV_NAME
from encryption.crypto import encrypt_file
from utils.time_manager import check_keys_expired, DATETIME_FORMAT
from system_stats import USER_KEYS_PATH, DISK_NAME, REGISTRATION_JOURNAL

def create_user_keys_if_not_exist(login):
  user_keys = [
    f for f in os.listdir(USER_KEYS_PATH) if os.path.isfile(f'{USER_KEYS_PATH}/{f}')
  ]
  keys_exist = (
    f'{login}_{PUB_NAME}' in user_keys and
    f'{login}_{PRIV_NAME}' in user_keys
  )
  if not keys_exist: generate_key_pair(USER_KEYS_PATH, login)

def create_keys_if_not_exist():
  path = f'{DISK_NAME}/admin'
  keys_exist = (
    os.path.exists(f'{DISK_NAME}/admin/{PRIV_NAME}') and
    os.path.exists(f'{DISK_NAME}/admin/{PUB_NAME}')
  )
  if not keys_exist:
   generate_key_pair(path)
   encrypt_file(REGISTRATION_JOURNAL, path)

def remove_user_keys(login):
  for f in (f'{login}_{PRIV_NAME}', f'{login}_{PUB_NAME}'):
    path = f'{USER_KEYS_PATH}/{f}'
    if os.path.exists(path): os.remove(path)

def check_user_keys_expiration(login):
  for f in (f'{login}_{PRIV_NAME}', f'{login}_{PUB_NAME}'):
    path = f'{USER_KEYS_PATH}/{f}'
    creation = (datetime
      .fromtimestamp(os.path.getctime(path))
      .strftime(DATETIME_FORMAT))
    return check_keys_expired(creation)

def replace_user_keys(login):
  remove_user_keys(login)
  generate_key_pair(USER_KEYS_PATH, login)
