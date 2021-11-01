from system_stats import MIN_USER_PASSWD_LEN
from users import journal_manager

validate_login_len = lambda login: len(login) > 0
login_exists = lambda login: journal_manager.check_user(login) is not None
is_admin_login = lambda login: journal_manager.get_user(login)[0].admin
validate_passwd_len = lambda passwd: len(passwd) >= MIN_USER_PASSWD_LEN
passwd_correct = lambda passwd, login: journal_manager.get_user(login)[0].check_passwd(passwd)
new_users_available = lambda: not journal_manager.users_limit_reached()
validate_spaces = lambda input: not any(c.isspace() for c in input)
