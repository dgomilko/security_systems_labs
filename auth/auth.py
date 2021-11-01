from users import journal_manager
from auth.messages import messages
from auth.validators import *
from auth.options import login_option, register_option
from utils.wrapped_input import wrapped_input

def login():
  journal_parse_err = journal_manager.check_users_data_files()
  if journal_parse_err is not None:
    messages['CORRUPTED_FILES'](journal_parse_err)
    return None
  commands = {
    'login': login_option,
    'register': register_option,
    'exit': lambda: None
  }
  messages['WELCOME'](commands.keys())
  while True:
    option = wrapped_input('> ')
    if option in commands: return commands[option]()
    else: messages['UNKNOWN_OPTION'](option)
