messages = {
  'PROMPT': lambda t: print(f'\nPlease, answer this questions in {t} minutes:'),
  'SUCCESS': lambda: print('The answer is correct, you may continue your work'),
  'WARNING': lambda n: print(f'Incorrect answer! Please, relogin into your account ({n} attempts left)'),
  'DELETED': lambda: print('The limit of incorrect answers is exceeded, you will have to recreate your account'),
  'NO_ANSWER': lambda n: print(f'Your time to answer this question has ran out. This will count as an incrorrect answer ({n} attempts left)')
}
