from users.users_list import UserAccount, UsersList

users = UsersList([
  UserAccount('user1', '12345'),
  UserAccount('admin1', '12345678', True)
])
