import os
from getpass import getpass
from users.journal_manager import get_user, change_user_passwd, add_user
from auth.messages import messages
from auth.validators import *
from auth.messages import messages
from utils.time_manager import check_passswd_expired
from utils.wrapped_input import wrapped_input
from system_stats import QUESTIONS_PER_USER
from monitor.journal_manager import add_level_one_threat
from encryption.user_keys_manager import check_user_keys_expiration, replace_user_keys

def get_passwd():
    while True:
      password = getpass()
      while(not validate_password(password)):
        if not validate_passwd_len(password): messages['PASSWD_LEN']()
        if not validate_spaces(password): messages['PASSWD_SPACES']()
        if not validate_lowercase(password): messages['PASSWD_NO_LOWERCASE']()
        if not validate_uppercase(password): messages['PASSWD_NO_UPPERCASE']()
        if not validate_digit(password): messages['PASSWD_NO_NUM']()
        if not validate_special_char(password): messages['PASSWD_NO_SPECIAL_CHAR']()
        password = getpass()
      return password

def get_login(new):
    prompt = 'New login: ' if new else 'Login: '
    while True:
      login = wrapped_input(prompt)
      while(
        not validate_login_len(login) or
        (not new and not login_exists(login)) or
        (new and (login_exists(login) or not validate_spaces(login)))
      ):
        if not validate_login_len(login): messages['BLANK_LOGIN']()
        if new:
          if not validate_spaces(login): messages['LOGIN_SPACES']()
          else: messages['LOGIN_EXISTS']()
        else: messages['LOGIN_DOESNT_EXIST']()
        login = wrapped_input('Login: ')
      return login

def manage_passwd_expiration(user):
    new_passwd = ''
    while True:
      new_passwd = get_passwd()
      if new_passwd == user.password: messages['SAME_PASSWD']()
      else: break
    user = change_user_passwd(user, new_passwd)
    messages['PASSWD_CHANGED']()
    return user

def manage_keys_expiration(user):
  while True:
    answer = input('> ')
    if answer in ('y', 'yes'):
      replace_user_keys(user.login)
      messages['KEYS_CHANGED']()
      break
    elif answer in ('n', 'no'): break
    else: messages['UNKNOWN_OPTION'](answer)

def login_option():
    login = get_login(new=False)
    passwd_attempts = 3
    while True:
      password = getpass()
      while(not passwd_correct(password, login)):
        passwd_attempts -= 1
        add_level_one_threat(login)
        messages['PASSWD_WRONG'](passwd_attempts)
        if not passwd_attempts: return None
        password = getpass()
      break
    (user, timestamp) = get_user(login)
    if check_passswd_expired(timestamp):
      messages['PASSWD_EXPIRED']()
      user = manage_passwd_expiration(user)
    if check_user_keys_expiration(login):
      messages['KEYS_EXPIRED']()
      manage_keys_expiration(user)
    return user

def get_questions():
    messages['QUESTION'](QUESTIONS_PER_USER)
    questions_count = 0
    questions = list()
    while questions_count < QUESTIONS_PER_USER:
      question = wrapped_input(f'Question {questions_count + 1}: ')
      answer_prompt = f'Answer to question {questions_count + 1}: '
      answer = wrapped_input(answer_prompt)
      while(not validate_spaces(answer)):
        messages['ANSWER_SPACE'](QUESTIONS_PER_USER)
        answer = wrapped_input(answer_prompt)
      questions.append([question, answer])
      questions_count += 1
    return questions

def register_option():
    if not new_users_available():
      messages['NEW_USERS_UNAVAILABLE']()
      return None
    login = get_login(new=True)
    password = get_passwd()
    questions = get_questions()
    user, fn = add_user(login, password, questions)
    messages['REGISTER_COMPLETED'](fn)
    input('')
    os.system('clear')
    return user
