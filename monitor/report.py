import os
from utils.time_manager import check_report_expired, generate_timestamp
from monitor.journal_manager import journal_empty, get_users_stats, clear_journal
from system_stats import REPORT_PATH, MISTAKES_CRITICAL_N

def init_analyzer():
  no_entries = journal_empty()
  if no_entries: return
  no_report = not os.path.exists(REPORT_PATH)
  new_report_needed = no_report
  if not no_report:
    with open(REPORT_PATH) as f:
      last_report_datetime = f.readline().strip()
    last_report_expired = check_report_expired(last_report_datetime)
    new_report_needed = last_report_expired
  if new_report_needed: generate_report()

def generate_report():
  stats = get_users_stats()
  cur_time = generate_timestamp()
  with open(REPORT_PATH, 'w+') as f:
    f.write(f'{cur_time}\n')
    for user, threats in stats.items():
      (level_1, level_2, level_3) = threats
      total = sum(threats)
      report = f'{user}: level 1: {level_1}, level 2: {level_2}, level 3: {level_3}, total: {total}'
      high_rate = analyse_threats(threats)
      if high_rate: report += '  < high level of suspicious activity!'
      f.write(f'{report}\n')
  clear_journal()

def analyse_threats(threats):
  thresholds = [
    MISTAKES_CRITICAL_N * 3,
    MISTAKES_CRITICAL_N * 2,
    MISTAKES_CRITICAL_N
  ]
  for threat_n, threshold in zip(threats, thresholds):
    if threat_n > threshold: return True
  return False
