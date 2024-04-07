import data.users as usrs
import data.food as food
import data.db_connect as con
import pytest
import datetime
from bson.objectid import ObjectId

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
    for ingr in pantry_contents:
        print("INGREDIENT FROM PANTRY: ")
        print(ingr)
        food_obj = con.fetch_one(
            con.FOOD_COLLECTION,
            {con.MONGO_ID: ingr[food.INGREDIENT]}
        )
        print("INGREDIENT ")
        print(ingr)
        assert food.INGREDIENT in ingr and isinstance(ingr[food.INGREDIENT],ObjectId)
        assert food.QUANTITY in ingr and isinstance(ingr[food.QUANTITY],float)
        assert food.UNITS in ingr and isinstance(ingr[food.UNITS],str)

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
    ingredient = con.fetch_one(
            con.FOOD_COLLECTION,
            {con.MONGO_ID: pantry_contents[0][food.INGREDIENT]}
        )
    
    assert food.INGREDIENT in pantry_contents[0] and isinstance(pantry_contents[0][food.INGREDIENT],ObjectId) and ingredient["name"] == "egg"
    assert food.QUANTITY in pantry_contents[0] and isinstance(pantry_contents[0][food.QUANTITY],float) and pantry_contents[0][food.QUANTITY] == 2.0
    assert food.UNITS in pantry_contents[0] and isinstance(pantry_contents[0][food.UNITS],str) and pantry_contents[0][food.UNITS] == "EACH"


# BAD TEST PLEASE FIX OR REMOVE
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
    

def test_mod_pantry_ingredient_amount(temp_user):
    username = temp_user
    ingredient_name = "carrot"
    old_amt = 1.0
    new_amount = 3.0
    ingr_list = [{
        food.INGREDIENT: ingredient_name,
        food.QUANTITY: old_amt,
        food.UNITS: "EACH",
        }]
    usrs.add_to_pantry(username, ingr_list)
    usrs.modify_pantry_ingredient_amount(username, ingredient_name, new_amount)
    pantry_contents = usrs.get_pantry(username)
    print(f"{pantry_contents=}")
    for ingr in pantry_contents:
        # print("INGREDIENT:", item['ingredient'])
        item = con.fetch_one(
            con.FOOD_COLLECTION,
            {con.MONGO_ID: ingr[food.INGREDIENT]}
        )
        assert item['name'] == "carrot"
        assert ingr[food.QUANTITY] == 3.0


# RECIPE METHODS
def test_get_recipes(temp_user):
    username = temp_user
    recipe = {
        "name": "stir fry",
        "ingredients": [{
            food.INGREDIENT: "chicken thigh",
            food.QUANTITY: 1.0,
            food.UNITS: "lbs.",
        }, {
            food.INGREDIENT: "soy sauce",
            food.QUANTITY: 3.0,
            food.UNITS: "oz.",
        }]
    }
    usrs.add_to_saved_recipes(username, recipe)
    retrieved_recipes = usrs.get_saved_recipes(username)
    for recipe in retrieved_recipes:
        assert isinstance(recipe, dict)
        assert isinstance(recipe[con.MONGO_ID], ObjectId)
        assert "name" in recipe



# RECIPE METHODS
# def test_rec_recipes(temp_user):
#     username = temp_user
#     ingr_list = [{
#         food.INGREDIENT: "egg",
#         food.QUANTITY: 3.0,
#         food.UNITS: "EACH",
#         },
#         {
#         food.INGREDIENT: "milk",
#         food.QUANTITY: 1.0,
#         food.UNITS: "EACH",
#         },
#         {
#         food.INGREDIENT: "bread",
#         food.QUANTITY: 0.5,
#         food.UNITS: "EACH",
#         }
#     ]
#     recipe = {
#         "name": "test",
#         "ingredients": [
#             {
#                 food.INGREDIENT: "egg",
#                 food.QUANTITY: 3.0,
#                 food.UNITS: "EACH",
#             },
#             {
#                 food.INGREDIENT: "broccoli",
#                 food.QUANTITY: 3.0,
#                 food.UNITS: "EACH",
#             },
#         ]
#     }
#     usrs.add_to_recipes(username, recipe)
#     usrs.add_to_pantry(username, ingr_list)
#     usrs.recommend_recipes(username)
#     assert False


def test_add_to_saved_recipes(temp_user):
    username = temp_user
    recipe = {
        "name": "stir fry",
        "ingredients": [{
            food.INGREDIENT: "egg noodle",
            food.QUANTITY: 1.0,
            food.UNITS: "lbs.",
        }, {
            food.INGREDIENT: "soy sauce",
            food.QUANTITY: 3.0,
            food.UNITS: "oz.",
        }]
    }
    usrs.add_to_saved_recipes(username, recipe)
    retrieved_recipes = usrs.get_saved_recipes(username)
    assert retrieved_recipes[0]["name"] == "stir fry"


def test_delete_recipes(temp_user):
    username = temp_user
    recipe = {
        "name": "stir fry",
        "ingredients": [{
            food.INGREDIENT: "egg noodle",
            food.QUANTITY: 1.0,
            food.UNITS: "lbs.",
        }, {
            food.INGREDIENT: "soy sauce",
            food.QUANTITY: 3.0,
            food.UNITS: "oz.",
        }]
    }
    usrs.add_to_saved_recipes(username, recipe)
    usrs.remove_from_saved_recipes(username, "stir fry")
    retrieved_recipes = usrs.get_saved_recipes(username)
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
        assert food.INGREDIENT in ingredient and isinstance(ingredient[food.INGREDIENT],ObjectId)
        assert food.QUANTITY in ingredient and isinstance(ingredient[food.QUANTITY],float)
        assert food.UNITS in ingredient and isinstance(ingredient[food.UNITS],str)


def test_recommend_recipes(temp_user):
    username = temp_user
    ingr_list = [
    {
        food.INGREDIENT: "egg",
        food.QUANTITY: 2.0,
        food.UNITS: "EACH",
    },
    {
        food.INGREDIENT: "rice",
        food.QUANTITY: 10.0,
        food.UNITS: "c.",
    },
    {
        food.INGREDIENT: "soy sauce",
        food.QUANTITY: 16.0,
        food.UNITS: "oz.",
    },
    ]
    
    usrs.add_to_pantry(username, ingr_list)
    
    recipes = [
    {
        "name": "chicken",
        "ingredients": [{
            food.INGREDIENT: "chicken",
            food.QUANTITY: 1.0,
            food.UNITS: "lb.",
        }],
        "url": "google.com"
    },
    {
        "name": "egg fried rice",
        "ingredients": [*ingr_list, {
            food.INGREDIENT: "sesame oil",
            food.QUANTITY: 1.0,
            food.UNITS: "tsp.",
        }],
        "url": "google.com"
    },
    ]
    for recipe in recipes:
        usrs.add_to_recipes(recipe)
    res = usrs.recommend_recipes(username)
    print(res)
    i = 0
    for entry in res:
        assert entry['name'] == recipes[i]['name']
        i += 1
