from dataclasses import dataclass
from users.user_account import UserAccount
import sys
sys.path.append('../')
from system_stats import USER_AMOUNT

@dataclass
class UsersList:
  users: list[UserAccount]

  def add_new_user(self, login, passwd, is_admin=False):
    if self.users_limit_reached(): return
    new_user = UserAccount(login, passwd, is_admin)
    self.users.append(new_user)
    return new_user

  def user_exists(self, login):
    return login in [u.login for u in self.users]

  def users_limit_reached(self):
    return len(self.users) >= USER_AMOUNT

  def get_user(self, login):
    return list(filter(lambda u: u.login == login, self.users))[0]
  