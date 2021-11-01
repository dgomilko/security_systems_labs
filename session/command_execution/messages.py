messages = {
  'NOT_FOUND':
    lambda: print('This command is unavailable'),
  'NO_PARENT_DIR':
    lambda: print('You have already reached the topmost level of this file system'),
  'NO_PERMISSION':
    lambda: print('You lack permissions to perform this action')
}
