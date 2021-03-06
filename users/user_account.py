from dataclasses import dataclass
from system_stats import MIN_USER_PASSWD_LEN, MIN_ADMIN_PASSWD_LEN

@dataclass
class UserAccount:
  login: str
  password: str
  questions: list[list[str]]
  admin: bool = False

  def __post_init__(self):
    expected_min_len = MIN_ADMIN_PASSWD_LEN if self.admin else MIN_USER_PASSWD_LEN
    assert len(self.password) > expected_min_len

  def check_passwd(self, passwd):
    return passwd == self.password
