import data.users as usrs
import data.food as food

import pytest

MIN_USERS = 1
MIN_USERNAME_LEN = 4


@pytest.fixture(scope='function')
def temp_user():
    username = usrs._get_test_username()
    name = usrs._get_test_name()
    ret = usrs.create_user(username, name)
    print(f'{ret=}')
    yield username
    if usrs.user_exists(username):
        usrs.remove_user(username)


def test_get_test_name():
    username = usrs._get_test_username()
    assert isinstance(username, str)
    assert len(username) == usrs.TEST_USERNAME_LENGTH


def test_get_users(temp_user):
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0
    for user in users:
        assert isinstance(user, str)

        assert len(user) > MIN_USERNAME_LEN
        assert isinstance(users[user], dict)

        assert usrs.NAME in users[user]
        assert isinstance(users[user][usrs.NAME], str)
        
        assert usrs.PANTRY in users[user]
        assert isinstance(users[user][usrs.PANTRY], list)
        
        for fooditem in users[user][usrs.PANTRY]:
            assert isinstance(fooditem, dict)

            assert food.INGREDIENT in fooditem
            assert isinstance(fooditem[food.INGREDIENT], str)

            assert food.QUANTITY in fooditem
            assert isinstance(fooditem[food.QUANTITY], float) or isinstance(fooditem[food.QUANTITY], int)
            
            assert food.UNITS in fooditem
            assert isinstance(fooditem[food.UNITS], str)
    print(f'{temp_user=}')
    assert usrs.user_exists(temp_user)


def test_add_user_dup_name(temp_user):
    """
    Make sure a duplicate game name raises a ValueError.
    `temp_game` is the name of the game that our fixture added.
    """
    with pytest.raises(ValueError):
        usrs.create_user(temp_user, 'Jane')


def test_add_user_blank_name():
    """
    Make sure a blank game name raises a ValueError.
    """
    with pytest.raises(ValueError):
        usrs.create_user('', 'Jane')


def test_del_game(temp_user):
    name = temp_user
    usrs.remove_user(name)
    assert not usrs.user_exists(name)


def test_del_game_not_there():
    name = usrs._get_test_name()
    with pytest.raises(ValueError):
        usrs.remove_user(name)
