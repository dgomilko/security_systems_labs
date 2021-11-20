import os
from system_stats import OPERATIVE_JOURNAL
from utils.time_manager import generate_timestamp

def journal_empty():
  return not (
    os.path.exists(OPERATIVE_JOURNAL) and
    os.stat(OPERATIVE_JOURNAL)
  )

def add_record(username, level):
  with open(OPERATIVE_JOURNAL, 'a+') as f:
    timestamp = generate_timestamp()
    record = f'{username} {timestamp} {level}\n'
    f.write(record)
  
add_level_one_threat = lambda username: add_record(username, 1)
add_level_two_threat = lambda username: add_record(username, 2)
add_level_three_threat = lambda username: add_record(username, 3)

def get_users_stats():
  stats = dict()
  with open(OPERATIVE_JOURNAL) as f: lines = f.readlines()
  for line in lines:
    (user, _, level) = line.split()
    if not user in stats.keys(): stats[user] = [0, 0, 0]
    stats[user][int(level) - 1] += 1
  return stats

def clear_journal():
  open(OPERATIVE_JOURNAL, 'w').close()
