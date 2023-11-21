"""
This module interfaces with user data.
"""

# import data.food
import random
from string import ascii_uppercase
import requests
import data.db_connect as con
from PIL import Image
import pytesseract


TEST_USERNAME_LENGTH = 6
TEST_NAME_LENGTH = 6

NAME = 'Name'
PANTRY = 'Pantry'
USERNAME = "Username"
SAVED_RECIPES = 'Saved_Recipes'
INSTACART_USR = 'Instacart_User_Info'
GROCERY_LIST = 'Grocery List'
ALLERGENS = 'Allergens'
# USERS = {
#     'cc6956':
#         {
#             NAME: 'Calvin',
#             PANTRY: [
#                 data.food.get_food('chicken breast', 1, 'lb'),
#                 data.food.get_food('soy sauce', 1, 'gal'),
#                 ],
#             SAVED_RECIPES: {},
#             INSTACART_USR: None,
#             GROCERY_LIST: [],
#             ALLERGENS: [],
#         },
#     'gt2125':
#         {
#             NAME: 'Gayatri',
#             PANTRY: [
#                 data.food.get_food('romaine lettace', 1, 'lb'),
#                 data.food.get_food('egg', 24, 'count'),
#                 ],
#             SAVED_RECIPES: {},
#             INSTACART_USR: None,
#             GROCERY_LIST: [],
#             ALLERGENS: [],
#         },
#     'yh3595':
#         {
#             NAME: 'Jason',
#             PANTRY: [
#                 data.food.get_food('steak', 3, 'lb'),
#                 data.food.get_food('potatoes', 5, 'count'),
#                 ],
#             SAVED_RECIPES: {},
#             INSTACART_USR: None,
#             GROCERY_LIST: [],
#             ALLERGENS: [],
#         },
#     'nz2065':
#         {
#             NAME: 'Nashra',
#             PANTRY: [
#                 data.food.get_food('chicken thigh', 0.25, 'lb'),
#                 data.food.get_food('grapes', 5, 'count'),
#                 ],
#             SAVED_RECIPES: {},
#             INSTACART_USR: None,
#             GROCERY_LIST: [],
#             ALLERGENS: [],
#         },
# }


def _get_test_username():
    con.connect_db()
    username = ''.join(random.choices(ascii_uppercase, k=TEST_USERNAME_LENGTH))
    while user_exists(username):
        username = ''.join(random.choices(
            ascii_uppercase, k=TEST_USERNAME_LENGTH))
    return username


def _get_test_name():
    con.connect_db()
    name = ''.join(random.choices(ascii_uppercase, k=TEST_NAME_LENGTH))
    while user_exists(name):
        name = ''.join(random.choices(ascii_uppercase, k=TEST_NAME_LENGTH))
    return name


def user_exists(username):
    con.connect_db()
    try:
        con.fetch_one(con.USERS_COLLECTION, {USERNAME: username})
        res = True
    except ValueError:
        res = False
    return res


def _get_test_user():
    test_user = {}
    test_user[USERNAME] = _get_test_username()
    test_user[NAME] = _get_test_name()
    return test_user


def get_users():
    con.connect_db()
    users = con.fetch_all(con.USERS_COLLECTION)
    for user in users:
        user["_id"] = str(user["_id"])
    return users


def get_user(username: str) -> str:
    con.connect_db()
    try:
        res = con.fetch_one(con.USERS_COLLECTION, {USERNAME: username})
        res["_id"] = str(res["_id"])
    except ValueError:
        raise ValueError(f'User {username} does not exist')

    return res


def create_user(username: str, name: str) -> str:
    con.connect_db()
    if len(username) < 5:
        raise ValueError(f'Username {username} is too short')

    if user_exists(username):
        raise ValueError(f'User {username} already exists')

    print(type(username))
    print(type(name))

    new_user = {
        USERNAME: username,
        NAME: name,
        PANTRY: [],
        SAVED_RECIPES: {},
        INSTACART_USR: None,
        GROCERY_LIST: [],
        ALLERGENS: [],
    }

    add_ret = con.insert_one(con.USERS_COLLECTION, new_user)
    print(f'{add_ret}')
    return f'Successfully added {username}'


def remove_user(username):
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    del_res = con.del_one(con.USERS_COLLECTION, {USERNAME: username})

    print(f'{del_res}')
    return f'Successfully deleted {username}'


def get_pantry(username):
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    pantry_res = con.fetch_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {PANTRY: 1, "_id": 0}
    )

    return pantry_res


def add_to_pantry(username: str, food: list[str]) -> str:
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    con.update_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {"$push": {PANTRY: {"$each": food}}}
    )
    return f'Successfully added {food}'


def get_recipes(username):
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    recipes_res = con.fetch_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {SAVED_RECIPES: 1, "_id": 0}
    )

    return recipes_res


def generate_recipe(username, query):
    app_key = '274c6a9381c49bc303a30cebb49c84d4'
    app_id = '29bf3511'
    query_string = 'https://api.edamam.com/api/recipes\
        /v2?type=public&q=' + query + '&app_id=' + app_id +\
        '&app_key=' + app_key
    x = requests.get(query_string)
    return x  # return full recipe response body


def add_to_recipes(username, recipe):
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    con.update_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {"$push": {SAVED_RECIPES: {recipe: 0}}}
    )

    return f'Successfully added {recipe}'


def made_recipe(username, recipe):
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    con.update_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {"$inc": {f'{SAVED_RECIPES}.{recipe}': 1}}
    )

    return f'Successfully incremented streak counter for {recipe}'


def remove_recipe(username, recipe):
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    con.update_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {"$pull": {SAVED_RECIPES: recipe}}
    )

    return f'Successfully removed {recipe}'


def recognize_receipt(image_path=None, image=None):
    if (image_path and not image):
        # Load the image from the specified path
        image = Image.open(image_path)
    elif (not image):  # neither the path nor image is provided
        return None
    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(image)
    # Print or save the extracted text
    print(text)
    # Optionally, save the text to a file
    # with open('extracted_text.txt', 'w', encoding='utf-8') as file:
    #     file.write(text)
    return text
