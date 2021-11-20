from math import *
from users.messages import messages
from users.user_account import UserAccount
from utils.time_manager import generate_timestamp
from encryption.crypto import decrypt_file_contents, text_encryption
from encryption.keys import generate_key_pair
from encryption.user_keys_manager import *
from system_stats import *

def get_user_data():
  data = (decrypt_file_contents(REGISTRATION_JOURNAL, f'{DISK_NAME}/admin')
    .split('\n'))
  return data[:-1] if data else data

def replace_file_contents(user_data):
  new_contents = text_encryption('\n'.join(user_data), f'{DISK_NAME}/admin', None)
  with open(REGISTRATION_JOURNAL, 'w') as f: f.write(new_contents.decode('utf-8'))

def check_users_data_files():
  users_count = 0
  create_keys_if_not_exist()
  user_data = get_user_data()
  for i, line in enumerate(user_data):
    if i == 0: continue
    users_count += 1
    split_data = line.split()
    if len(split_data) != 4 + QUESTIONS_PER_USER * 2:
      return messages['USER_DATA']
    if users_count > USER_AMOUNT: return messages['USERS_LIM']
    create_user_keys_if_not_exist(split_data[0])
  with open(QUESTIONS_STORAGE, 'a+') as f:
    f.seek(0)
    questions_count = sum(1 for _ in f)
    if questions_count < users_count * QUESTIONS_PER_USER:
      return messages['QUESTIONS_NUM']
  return None

def users_limit_reached():
  user_data = get_user_data()
  return sum(1 for _ in user_data) - 1 == USER_AMOUNT

def check_user(login):
  user_data = get_user_data()
  for i, line in enumerate(user_data):
    if i == 0: continue
    split_data = line.split()
    if split_data[0] != login: continue
    else: return i
  return None

def get_user(login):
  user_data = get_user_data()
  user_idx = check_user(login)
  if user_idx is None: return user_idx
  split_data = user_data[user_idx].split()
  (_, is_admin, passwd) = split_data[:3]
  questions_raw = split_data[3:3 + QUESTIONS_PER_USER * 2]
  questions = [questions_raw[i:i + 2] for i in range(0, len(questions_raw), 2)]
  questions_file = open(QUESTIONS_STORAGE, 'r')
  questions_list = questions_file.readlines()
  for entry in questions:
    question_text = ''
    for question in questions_list:
      split = question.split()
      if split[0] == entry[0]: question_text = question
    entry[0] = question_text
  user = UserAccount(login, passwd, questions, is_admin == '1')
  return (user, split_data[-1])

def add_user(login, passwd, questions, admin=False):
  user_data = get_user_data()
  result_string = f'{login} {int(admin)} {passwd}'
  questions_count = 0
  with open(QUESTIONS_STORAGE, 'a+') as f:
    f.seek(0)
    questions_count = sum(1 for _ in f)
    for i, (question, _) in enumerate(questions):
      f.write(f'{questions_count + i} {question}\n')
  for i, (_, answer) in enumerate(questions):
    result_string += f' {questions_count + i} {answer}'
  timestamp = generate_timestamp()
  result_string += f' {timestamp}\n'
  fn = user_data[0].rstrip()
  user_data.append(result_string)
  replace_file_contents(user_data)
  generate_key_pair(USER_KEYS_PATH, login)
  return (UserAccount(login, passwd, questions, admin), fn)

def change_user_passwd(user, passwd):
  user_data = get_user_data()
  user_idx = check_user(user.login)
  line = user_data[user_idx]
  split_data = line.split()
  split_data[2] = passwd
  split_data[-1] = generate_timestamp()
  new_line = ' '.join(split_data)
  changes = line.replace(line, f'{new_line}\n')
  user_data[user_idx] = changes
  replace_file_contents(user_data)
  user.password = passwd
  return user

def remove_user(user):
  user_data = get_user_data()
  new_data = list()
  for line in user_data:
    if line.split()[0] != user.login: new_data.append(line)
  replace_file_contents(new_data)
  with open(QUESTIONS_STORAGE, 'r') as f: q_lines = f.readlines()
  question_nums = [entry[0].split()[0] for entry in user.questions]
  with open(QUESTIONS_STORAGE, "w") as f:
    for line in q_lines:
      if line.split()[0] not in question_nums: f.write(line)
  remove_user_keys(user.login)

def get_secret_function():
  user_data = get_user_data()
  fn_str = user_data[0].rstrip()
  return lambda x: eval(fn_str, globals(), locals())
