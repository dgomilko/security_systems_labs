import sys
sys.path.append('../')
from system_stats import MIN_USER_PASSWD_LEN
from users.system_users import users

validate_login_len = lambda login: len(login) > 0
login_exists = lambda login: users.user_exists(login)
is_admin_login = lambda login: users.get_user(login).admin
validate_passwd_len = lambda passwd: len(passwd) >= MIN_USER_PASSWD_LEN
passwd_correct = lambda passwd, login: users.get_user(login).check_passwd(passwd)
new_users_available = lambda: not users.users_limit_reached()
