import sys
sys.path.append('../')
from system_stats import MIN_USER_PASSWD_LEN

messages = {
  'WELCOME':
    lambda options: (print('Welcome to the system. Please register or login.' +
      f'\nOptions: {" | ".join(options)}')),
  'BLANK_LOGIN':
    lambda: print('Login cannot be blank. Please, try again'),
  'LOGIN_DOESNT_EXIST':
    lambda: print('Entered login does not exist. Please, check the spelling'),
  'LOGIN_EXISTS':
    lambda: print('Entered login is already in use'),
  'PASSWD_LEN':
    lambda: print(f'Your password cannot be less than {MIN_USER_PASSWD_LEN} symbols'),
  'PASSWD_WRONG':
    lambda attempts: print(f'Wrong password! {attempts} attempt(s) left'),
  'NEW_USERS_UNAVAILABLE':
    lambda: print('Sorry, but maximum number of users in the system has already been reached'),
  'UNKNOWN_OPTION':
    lambda invalid_option: print(f'{invalid_option} is not an option')
}
