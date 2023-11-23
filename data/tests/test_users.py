import data.users as usrs
import data.food as food
import data.db_connect as con
import pytest
import datetime

MIN_USERS = 1
MIN_USERNAME_LEN = 4


@pytest.fixture(scope='function')
def temp_user():
    print("GOING TO CONNECT")
    con.connect_db()
    test_user = usrs._create_test_user()
    username = test_user[usrs.USERNAME]
    yield username
    if usrs.user_exists(username):
        usrs.remove_user(username)



def test_get_users(temp_user):
    users = usrs.get_users()
    print(f'{users}')
    assert isinstance(users, list)
    assert len(users) > 0
    for user in users:
        assert isinstance(user, dict)

        assert len(user) > MIN_USERNAME_LEN
        assert isinstance(user, dict)

        assert usrs.NAME in user
        assert isinstance(user[usrs.NAME], str)
        
        assert usrs.PANTRY in user
        assert isinstance(user[usrs.PANTRY], list)
        
        for fooditem in user[usrs.PANTRY]:
            assert isinstance(fooditem, dict)

            assert food.INGREDIENT in fooditem
            assert isinstance(fooditem[food.INGREDIENT], str)

            assert food.QUANTITY in fooditem
            assert isinstance(fooditem[food.QUANTITY], float) or isinstance(fooditem[food.QUANTITY], int)
            
            assert food.UNITS in fooditem
            assert isinstance(fooditem[food.UNITS], str)
    print(f'{temp_user=}')
    assert usrs.user_exists(temp_user)


def test_get_test_name():
    username = usrs._get_test_username()
    print(f'{username=}')
    assert isinstance(username, str)
    assert len(username) == usrs.TEST_USERNAME_LENGTH


def test_add_user_dup_name(temp_user):
    """
    Make sure a duplicate game name raises a ValueError.
    `temp_game` is the name of the game that our fixture added.
    """
    print(f'{temp_user=}')
    print(f'{usrs.user_exists(temp_user)}')
    with pytest.raises(ValueError):
        exp = usrs._get_test_exp()
        usrs.create_user(temp_user, 'Jane', exp)


def test_add_user_blank_name():
    """
    Make sure a blank game name raises a ValueError.
    """
    with pytest.raises(ValueError):
        exp = usrs._get_test_exp()
        usrs.create_user('', 'Jane', exp)


def test_del_game(temp_user):
    name = temp_user
    usrs.remove_user(name)
    assert not usrs.user_exists(name)


def test_del_game_not_there():
    name = usrs._get_test_name()
    with pytest.raises(ValueError):
        usrs.remove_user(name)
