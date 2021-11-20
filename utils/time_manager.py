from datetime import datetime
from system_stats import PASSWD_LIFETIME_DAYS, REPORT_INTERVAL_DAYS, KEYS_LIFETIME_DAYS

DATETIME_FORMAT = '%Y-%m-%dT%H:%M'

generate_timestamp = lambda: datetime.now().strftime(DATETIME_FORMAT)

def time_elapsed(timestamp, period_in_days):
  start_timestamp = datetime.strptime(timestamp, DATETIME_FORMAT)
  cur_timestamp = datetime.now()
  elapsed_minutes = (cur_timestamp - start_timestamp).total_seconds() / 60
  return elapsed_minutes > period_in_days * 24 * 60

check_passswd_expired = lambda timestamp: time_elapsed(timestamp, PASSWD_LIFETIME_DAYS)
check_report_expired = lambda timestamp: time_elapsed(timestamp, REPORT_INTERVAL_DAYS)
check_keys_expired = lambda timestamp: time_elapsed(timestamp, KEYS_LIFETIME_DAYS)
