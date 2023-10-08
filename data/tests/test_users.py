import data.users as usrs
import data.food as food

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
