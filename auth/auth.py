from getpass import getpass
from users.system_users import users
from auth.validators import *
from auth.messages import messages

def login_option():
    while True:
      login = input('Login: ')
      while(not validate_login_len(login) or not login_exists(login)):
        if not validate_login_len(login): messages['BLANK_LOGIN']()
        else: messages['LOGIN_DOESNT_EXIST']()
        login = input('Login: ')
      break
    passwd_attempts = 3
    while True:
      password = getpass()
      while(not passwd_correct(password, login)):
        passwd_attempts -= 1
        messages['PASSWD_WRONG'](passwd_attempts)
        if not passwd_attempts: return False
        password = getpass()
      break
    return users.get_user(login)

def register_option():
  if not new_users_available():
    messages['NEW_USERS_UNAVAILABLE']()
    return False
  while True:
    login = input('New login: ')
    while(not validate_login_len(login) or login_exists(login)):
      if not validate_login_len(login): messages['BLANK_LOGIN']()
      else: messages['LOGIN_EXISTS']()
      login = input('New login: ')
    break
  while True:
    password = getpass()
    while(not validate_passwd_len(password)):
      messages['PASSWD_LEN']()
      password = getpass()
    break
  user = users.add_new_user(login, password)
  return user

def login():
  commands = {
    "login": login_option,
    "register": register_option,
    "exit": lambda: None
  }
  print("Welcome to the system. Please register or login.")
  print("Options: register | login | exit")
  while True:
    option = input("> ")
    if option in commands:
      result = commands[option]()
      if result is None: break
      else: return result
    else: messages['UNKNOWN_OPTION'](option)
