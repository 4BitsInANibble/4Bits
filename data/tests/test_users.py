import data.users as usrs


MIN_USERS = 1
MIN_USERNAME_LEN = 4
def test_get_users():
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0
    for user in users:
        assert isinstance(user, str)
        assert len(user) > MIN_USERNAME_LEN
        assert isinstance(users[user], dict)
       

