import data.users as usrs
import data.food as food
import data.db_connect as con
import pytest
import datetime

MIN_USERS = 1
MIN_USERNAME_LEN = 4


# TEST SETUP
@pytest.fixture(scope='function')
def temp_google_user():
    print("GOING TO CONNECT")
    con.connect_db()
    test_user = usrs._create_test_google_user()
    username = test_user[usrs.USERNAME]
    yield username
    if usrs.user_exists(username):
        usrs.remove_user(username)


@pytest.fixture(scope='function')
def temp_user():
    print("GOING TO CONNECT")
    con.connect_db()
    username = usrs._create_test_user()
    yield username
    if usrs.user_exists(username):
        if usrs.auth_expired(username):
            usrs.login_user(username, "TEST_PASSWORD")
        usrs.remove_user(username)


def test_get_test_name():
    username = usrs._get_test_username()
    print(f'{username=}')
    assert isinstance(username, str)
    assert len(username) == usrs.TEST_USERNAME_LENGTH


# USER METHODS
def test_get_users(temp_user):
    users = usrs.get_users()
    print(f'{users}')
    assert isinstance(users, list)
    assert len(users) > 0
    for user in users:
        assert isinstance(user, dict)
        print(f'{user=}')
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


def test_add_user_dup_name(temp_user):
    """
    Make sure a duplicate game name raises a ValueError.
    `temp_game` is the name of the game that our fixture added.
    """
    print(f'{temp_user=}')
    print(f'{usrs.user_exists(temp_user)}')
    with pytest.raises(ValueError):
        exp = usrs.generate_exp()
        usrs.create_user(temp_user, 'Jane', exp)


def test_add_user_blank_name():
    """
    Make sure a blank game name raises a ValueError.
    """
    with pytest.raises(ValueError):
        exp = usrs.generate_exp()
        usrs.create_user('', 'Jane', exp)

def test_add_user_long_name():
    """
    Make sure a blank game name raises a ValueError.
    """
    with pytest.raises(ValueError):
        exp = usrs.generate_exp()
        usrs.create_user('abcdefghijklmnopqrstuvwxyz', 'Jane', exp)

def test_del_user(temp_user):
    name = temp_user
    usrs.remove_user(name)
    assert not usrs.user_exists(name)


def test_del_user_not_there():
    name = usrs._get_test_name()
    with pytest.raises(ValueError):
        usrs.remove_user(name)


def test_login_user(temp_user):
    username = temp_user
    test_password = "TEST_PASSWORD"
    usrs.logout_user(username)
    token, refresh_token = usrs.login_user(username, test_password)
    assert not usrs.auth_expired(username)
    assert isinstance(token, str)
    assert isinstance(refresh_token, str)


def test_login_user_wrong_pw(temp_user):
    username = temp_user
    test_password = "WRONG_TEST_PASSWORD"
    with pytest.raises(ValueError):
        token = usrs.login_user(username, test_password)


def test_login_non_existent_user():
    username = usrs._get_test_username()
    test_password = "TEST_PASSWORD"
    with pytest.raises(ValueError):
        token = usrs.login_user(username, test_password)


def test_logout_user(temp_user):
    username = temp_user
    usrs.logout_user(username)
    assert usrs.auth_expired(username)


def test_logout_loggedout_user(temp_user):
    username = temp_user
    usrs.logout_user(username)
    with pytest.raises(usrs.AuthTokenExpired):
        usrs.logout_user(username)


# PANTRY METHODS
def test_get_pantry(temp_user):
    username = temp_user
    ingr_list = [{
        food.INGREDIENT: "egg",
        food.QUANTITY: 2.0,
        food.UNITS: "EACH",
        }]
    usrs.add_to_pantry(username, ingr_list)
    pantry_contents = usrs.get_pantry(username)
    for ingredient in pantry_contents:
        assert food.INGREDIENT in ingredient and isinstance(ingredient[food.INGREDIENT],str)
        assert food.QUANTITY in ingredient and isinstance(ingredient[food.QUANTITY],float)
        assert food.UNITS in ingredient and isinstance(ingredient[food.UNITS],str)

def test_add_to_pantry(temp_user):
    username = temp_user
    ingr_list = [{
        food.INGREDIENT: "egg",
        food.QUANTITY: 2.0,
        food.UNITS: "EACH",
        }]
    usrs.add_to_pantry(username, ingr_list)
    pantry_contents = usrs.get_pantry(username)
    assert len(pantry_contents) == 1
    ingredient = pantry_contents[0]
    assert food.INGREDIENT in ingredient and isinstance(ingredient[food.INGREDIENT],str) and ingredient[food.INGREDIENT] == "egg"
    assert food.QUANTITY in ingredient and isinstance(ingredient[food.QUANTITY],float) and ingredient[food.QUANTITY] == 2.0
    assert food.UNITS in ingredient and isinstance(ingredient[food.UNITS],str) and ingredient[food.UNITS] == "EACH"

def test_check_low_stock_pantry(temp_user):
    username = temp_user
    ingr_list = [{
        food.INGREDIENT: "egg",
        food.QUANTITY: 3.0,
        food.UNITS: "EACH",
        },
        {
        food.INGREDIENT: "milk",
        food.QUANTITY: 1.0,
        food.UNITS: "EACH",
        },
        {
        food.INGREDIENT: "bread",
        food.QUANTITY: 0.5,
        food.UNITS: "EACH",
        }, ]
    usrs.add_to_pantry(username, ingr_list)
    low_quantity = usrs.check_low_stock_pantry(username)
    # print("in test_users.py:")
    # print(low_quantity)
    for item in low_quantity:
        assert item['ingredient'] != "egg"
        assert item['quantity'] <= 2

# RECIPE METHODS
def test_get_recipes(temp_user):
    username = temp_user
    recipe = {
        "name": "stir fry",
        "ingredients": [[{
            food.INGREDIENT: "chicken thigh",
            food.QUANTITY: 1.0,
            food.UNITS: "lbs.",
        }, {
            food.INGREDIENT: "soy sauce",
            food.QUANTITY: 3.0,
            food.UNITS: "oz.",
        }]]
    }
    usrs.add_to_recipes(username, recipe)
    retrieved_recipes = usrs.get_recipes(username)
    for recipe in retrieved_recipes:
        assert isinstance(recipe, dict)


def test_add_to_recipes(temp_user):
    username = temp_user
    recipe = {
        "name": "stir fry",
        "ingredients": [[{
            food.INGREDIENT: "egg noodle",
            food.QUANTITY: 1.0,
            food.UNITS: "lbs.",
        }, {
            food.INGREDIENT: "soy sauce",
            food.QUANTITY: 3.0,
            food.UNITS: "oz.",
        }]]
    }
    usrs.add_to_recipes(username, recipe)
    retrieved_recipes = usrs.get_recipes(username)
    assert retrieved_recipes[0]["name"] == "stir fry"


def test_delete_recipes(temp_user):
    username = temp_user
    recipe = {
        "name": "stir fry",
        "ingredients": [[{
            food.INGREDIENT: "egg noodle",
            food.QUANTITY: 1.0,
            food.UNITS: "lbs.",
        }, {
            food.INGREDIENT: "soy sauce",
            food.QUANTITY: 3.0,
            food.UNITS: "oz.",
        }]]
    }
    usrs.add_to_recipes(username, recipe)
    usrs.delete_recipe(username, "stir fry")
    retrieved_recipes = usrs.get_recipes(username)
    print(retrieved_recipes)
    assert retrieved_recipes == []  


# GROCERY LIST METHODS
def test_get_grocery_list(temp_user):
    username = temp_user
    ingr_list = [{
        food.INGREDIENT: "egg",
        food.QUANTITY: 2.0,
        food.UNITS: "EACH",
        }]
    usrs.add_to_grocery_list(username, ingr_list)
    grocery_list_contents = usrs.get_grocery_list(username)
    for ingredient in grocery_list_contents:
        assert food.INGREDIENT in ingredient and isinstance(ingredient[food.INGREDIENT],str)
        assert food.QUANTITY in ingredient and isinstance(ingredient[food.QUANTITY],float)
        assert food.UNITS in ingredient and isinstance(ingredient[food.UNITS],str)


def test_add_to_grocery_list(temp_user):
    username = temp_user
    ingr_list = [{
        food.INGREDIENT: "egg",
        food.QUANTITY: 2.0,
        food.UNITS: "EACH",
        }]
    usrs.add_to_grocery_list(username, ingr_list)
    contents = usrs.get_grocery_list(username)
    assert len(contents) == 1
    ingredient = contents[0]
    assert food.INGREDIENT in ingredient and isinstance(ingredient[food.INGREDIENT],str) and ingredient[food.INGREDIENT] == "egg"
    assert food.QUANTITY in ingredient and isinstance(ingredient[food.QUANTITY],float) and ingredient[food.QUANTITY] == 2.0
    assert food.UNITS in ingredient and isinstance(ingredient[food.UNITS],str) and ingredient[food.UNITS] == "EACH"