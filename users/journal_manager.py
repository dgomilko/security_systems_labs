from math import *
from users.messages import messages
from users.user_account import UserAccount
from utils.passwd_expiration import generate_timestamp
from system_stats import *

def check_users_data_files():
  users_count = 0
  with open(REGISTRATION_JOURNAL, 'a+') as f:
    for _, line in enumerate(f, start=1):
      users_count += 1
      split_data = line.split()
      if len(split_data) != 4 + QUESTIONS_PER_USER * 2:
        return messages['USER_DATA']
    if users_count > USER_AMOUNT: return messages['USERS_LIM']
  with open(QUESTIONS_STORAGE, 'a+') as f:
   questions_count = sum(1 for _ in f)
   if questions_count < users_count * QUESTIONS_PER_USER:
     return messages['QUESTIONS_NUM']
  return None

def users_limit_reached():
  with open(REGISTRATION_JOURNAL, 'r') as f:
    return sum(1 for _ in f) - 1 == USER_AMOUNT

def check_user(login):
  with open(REGISTRATION_JOURNAL) as f:
    lines = f.readlines()
  for i, line in enumerate(lines, start=1):
    split_data = line.split()
    if split_data[0] != login: continue
    else: return i - 1
  return None

def get_user(login):
  with open(REGISTRATION_JOURNAL) as f: lines = f.readlines()
  user_idx = check_user(login)
  if user_idx is None: return user_idx
  split_data = lines[user_idx].split()
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
  with open(REGISTRATION_JOURNAL, 'a+') as f:
    f.seek(0)
    fn = f.readline().rstrip()
    f.write(result_string)
  return (UserAccount(login, passwd, questions, admin), fn)

def change_user_passwd(user, passwd):
  with open(REGISTRATION_JOURNAL) as f: lines = f.readlines()
  user_idx = check_user(user.login)
  line = lines[user_idx]
  split_data = line.split()
  split_data[2] = passwd
  split_data[-1] = generate_timestamp()
  new_line = ' '.join(split_data)
  changes = line.replace(line, f'{new_line}\n')
  lines[user_idx] = changes
  fout = open(REGISTRATION_JOURNAL, "w")
  fout.writelines(lines)
  fout.close()
  user.password = passwd
  return user

def remove_user(user):
  with open(REGISTRATION_JOURNAL, 'r') as f: u_lines = f.readlines()
  with open(REGISTRATION_JOURNAL, "w") as f:
    for line in u_lines:
      if line.split()[0] != user.login: f.write(line)
  with open(QUESTIONS_STORAGE, 'r') as f: q_lines = f.readlines()
  question_nums = [entry[0].split()[0] for entry in user.questions]
  with open(QUESTIONS_STORAGE, "w") as f:
    for line in q_lines:
      if line.split()[0] not in question_nums: f.write(line)

def get_secret_function():
  with open(REGISTRATION_JOURNAL) as f:
    f.seek(0)
    fn_str = f.readline().rstrip()
  return lambda x: eval(fn_str, globals(), locals())
