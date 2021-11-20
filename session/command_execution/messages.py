messages = {
  'NOT_FOUND': lambda: print('This command is unavailable'),
  'NO_PARENT_DIR':
    lambda: print('You have already reached the topmost level of this file system'),
  'NO_PERMISSION': lambda: print('You lack permissions to perform this action'),
  'ONE_ARG': lambda: print('Please, specify one argument'),
  'FILE_ARG': lambda: print('This file does not exist'),
  'CRYPTO_ERR': lambda: print(f'Unable to perform this action. Keys may be corrupted'),
}
