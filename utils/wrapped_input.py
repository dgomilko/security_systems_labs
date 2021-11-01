from utils.logout import logout

def wrapped_input(prompt):
  try: inp = input(prompt)
  except EOFError: logout()
  return inp
