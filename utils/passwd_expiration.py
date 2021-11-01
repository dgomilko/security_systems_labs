from datetime import datetime
from system_stats import PASSWD_LIFETIME_DAYS

DATETIME_FORMAT = '%Y-%m-%dT%H:%M'

generate_timestamp = lambda: datetime.now().strftime(DATETIME_FORMAT)

def check_passswd_expired(timestamp):
  start_timestamp = datetime.strptime(timestamp, DATETIME_FORMAT)
  cur_timestamp = datetime.now()
  elapsed_minutes = (cur_timestamp - start_timestamp).total_seconds() / 60
  return elapsed_minutes > PASSWD_LIFETIME_DAYS * 24 * 60
