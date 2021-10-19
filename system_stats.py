import stat

USER_AMOUNT = 5
MIN_USER_PASSWD_LEN = 3
MIN_ADMIN_PASSWD_LEN = 2 * MIN_USER_PASSWD_LEN
DISK_NAME = 'disk'
ALL_SUBDISKS = ['A', 'B', 'C', 'D', 'E']
PERMITTED_SUBDISKS = ['A', 'E']
USER_PERMISSIONS = stat.S_IRWXO | stat.S_IRWXG
OS_USERNAME = 'file_system_user_account'
SESSION_TIMEOUT_SEC = 180
