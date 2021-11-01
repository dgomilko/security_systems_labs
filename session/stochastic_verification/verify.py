from random import choice, uniform
from session.stochastic_verification.error_counter import register_error
from session.stochastic_verification.messages import messages
from users.journal_manager import get_secret_function, remove_user
from system_stats import QUESTIONS_INTERVAL_MIN, MISTAKES_CRITICAL_N

def ask(user):
  messages['PROMPT'](QUESTIONS_INTERVAL_MIN)
  if uniform(0, 1) < 0.25:
    fn = get_secret_function()
    x = round(uniform(-99, 99), 2)
    question = f'Enter the value of the secret function for the x = {x} (round the answer up to 2 decimal places)'
    answer_exp = round(fn(x), 2)
  else:
    entry = choice(user.questions)
    (question, answer_exp) = entry
    question = ' '.join(question.split()[1:])
  print(f'{question}\n')
  print('answer:')
  return answer_exp

def verify(user, exp, answer):
  if answer == exp:
    messages['SUCCESS']()
    return True
  (account_deleted, counter) = register_error(user.login)
  if account_deleted:
    remove_user(user)
    messages['DELETED']()
  else: messages['WARNING'](MISTAKES_CRITICAL_N - counter)
  return False

def handle_no_answer(user):
  (account_deleted, counter) = register_error(user.login)
  if account_deleted:
    remove_user(user)
    messages['DELETED']()
  else: messages['NO_ANSWER'](MISTAKES_CRITICAL_N - counter)
