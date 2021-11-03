from system_stats import MIN_USER_PASSWD_LEN

messages = {
  'WELCOME':
    lambda options: (print('Welcome to the system. Please register or login.' +
      f'\nOptions: {" | ".join(options)}')),
  'CORRUPTED_FILES':
    lambda err: print(f'System files are corrupted: {err}'),
  'BLANK_LOGIN':
    lambda: print('Login cannot be blank. Please, try again'),
  'LOGIN_DOESNT_EXIST':
    lambda: print('Entered login does not exist. Please, check the spelling'),
  'LOGIN_SPACES':
    lambda: print('Login should not contain any whitespaces'),
  'LOGIN_EXISTS':
    lambda: print('Entered login is already in use'),
  'PASSWD_LEN':
    lambda: print(f'Your password cannot be less than {MIN_USER_PASSWD_LEN} symbols'),
  'PASSWD_SPACES':
    lambda: print('Password should not contain any whitespaces'),
  'PASSWD_WRONG':
    lambda attempts: print(f'Wrong password! {attempts} attempt(s) left'),
  'NEW_USERS_UNAVAILABLE':
    lambda: print('Sorry, but maximum number of users in the system has already been reached'),
  'REGISTER_COMPLETED':
    lambda fn: print(f'Your account has been succesfully created! The secret function is {fn}. Press "Enter" to continue'),
  'UNKNOWN_OPTION':
    lambda invalid_option: print(f'{invalid_option} is not an option'),
  'QUESTION':
    lambda n: print(f'During the session you will be asked some questions in order to verify it is really you. Please, enter {n} questions and answers'),
  'ANSWER_SPACE':
    lambda: print(f'Please, do not use whitespaces in your answers'),
  'PASSWD_EXPIRED':
    lambda: print(f'Your password has expired. Please, choose a new one'),
  'SAME_PASSWD':
    lambda: print(f'New password should not be the same as the old one'),
  'PASSWD_CHANGED':
    lambda: print(f'Your password is successfully changed'),
  'PASSWD_NO_LOWERCASE':
    lambda: print('Your password does not have a lower case character. Please add at least one'),
  'PASSWD_NO_UPPERCASE':
    lambda: print('Your password does not have an upper case character. Please add at least one'),
  'PASSWD_NO_SPECIAL_CHAR':
    lambda: print('Your password does not have a valid special character ($!@%^&*#). Please add at least one valid special character'),
  'PASSWD_NO_NUM':
    lambda: print('Your password does not have a number. Please add at least one number'),
}
