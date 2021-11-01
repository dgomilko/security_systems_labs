import os
from getpass import getpass
from users import journal_manager
from auth.messages import messages
from auth.validators import *
from auth.messages import messages
from utils.passwd_expiration import check_passswd_expired
from utils.wrapped_input import wrapped_input
from system_stats import QUESTIONS_PER_USER

def get_passwd():
    while True:
      password = getpass()
      while(not validate_passwd_len(password) or not validate_spaces(password)):
        if not validate_passwd_len(password): messages['PASSWD_LEN']()
        else: messages['PASSWD_SPACES']()
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
    user = journal_manager.change_user_passwd(user, new_passwd)
    messages['PASSWD_CHANGED']()
    return user

def login_option():
    login = get_login(new=False)
    passwd_attempts = 3
    while True:
      password = getpass()
      while(not passwd_correct(password, login)):
        passwd_attempts -= 1
        messages['PASSWD_WRONG'](passwd_attempts)
        if not passwd_attempts: return None
        password = getpass()
      break
    (user, timestamp) = journal_manager.get_user(login)
    if check_passswd_expired(timestamp):
      messages['PASSWD_EXPIRED']()
      return manage_passwd_expiration(user)
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
    user, fn = journal_manager.add_user(login, password, questions)
    messages['REGISTER_COMPLETED'](fn)
    input('')
    os.system('clear')
    return user
