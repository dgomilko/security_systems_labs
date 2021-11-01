from system_stats import ERRORS_COUNTER, MISTAKES_CRITICAL_N

def register_error(login):
  with open(ERRORS_COUNTER, 'a+') as f:
    f.seek(0)
    lines = f.readlines()
  found = False
  counter = 0
  for i, line in enumerate(lines):
    split = line.split()
    if split[0] == login:
      found = True
      counter = int(split[-1]) + 1
      if counter == MISTAKES_CRITICAL_N:
        rm_user(i)
        return (True, MISTAKES_CRITICAL_N)
      else:
        new_line = f'{login} {counter}'
        lines[i] = new_line
  if found:
    fout = open(ERRORS_COUNTER, "w")
    fout.writelines(lines)
    fout.close()
  else:
    counter = 1
    add_user_record(login)
  return (False, counter)

def add_user_record(login):
  result_string = f'{login} 1'
  with open(ERRORS_COUNTER, 'a+') as f:
    f.seek(0)
    f.write(f'{result_string}\n')

def rm_user(idx):
  with open(ERRORS_COUNTER, 'r') as f: lines = f.readlines()
  with open(ERRORS_COUNTER, "w") as f:
    for i, line in enumerate(lines):
      if i != idx: f.write(line)
  