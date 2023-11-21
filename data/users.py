"""
This module interfaces with user data.
"""

import data.food
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
SAVED_RECIPES = 'Saved_Recipes'
INSTACART_USR = 'Instacart_User_Info'
GROCERY_LIST = 'Grocery List'
ALLERGENS = 'Allergens'
USERS = {
    'cc6956':
        {
            NAME: 'Calvin',
            PANTRY: [
                data.food.get_food('chicken breast', 1, 'lb'),
                data.food.get_food('soy sauce', 1, 'gal'),
                ],
            SAVED_RECIPES: {},
            INSTACART_USR: None,
            GROCERY_LIST: [],
            ALLERGENS: [],
        },
    'gt2125':
        {
            NAME: 'Gayatri',
            PANTRY: [
                data.food.get_food('romaine lettace', 1, 'lb'),
                data.food.get_food('egg', 24, 'count'),
                ],
            SAVED_RECIPES: {},
            INSTACART_USR: None,
            GROCERY_LIST: [],
            ALLERGENS: [],
        },
    'yh3595':
        {
            NAME: 'Jason',
            PANTRY: [
                data.food.get_food('steak', 3, 'lb'),
                data.food.get_food('potatoes', 5, 'count'),
                ],
            SAVED_RECIPES: {},
            INSTACART_USR: None,
            GROCERY_LIST: [],
            ALLERGENS: [],
        },
    'nz2065':
        {
            NAME: 'Nashra',
            PANTRY: [
                data.food.get_food('chicken thigh', 0.25, 'lb'),
                data.food.get_food('grapes', 5, 'count'),
                ],
            SAVED_RECIPES: {},
            INSTACART_USR: None,
            GROCERY_LIST: [],
            ALLERGENS: [],
        },
}


def _get_test_username():
    username = ''.join(random.choices(ascii_uppercase, k=TEST_USERNAME_LENGTH))
    while user_exists(username):
        username = ''.join(random.choices(
            ascii_uppercase, k=TEST_USERNAME_LENGTH))
    return username


def _get_test_name():
    name = ''.join(random.choices(ascii_uppercase, k=TEST_NAME_LENGTH))
    while user_exists(name):
        name = ''.join(random.choices(ascii_uppercase, k=TEST_NAME_LENGTH))
    return name


def user_exists(username):
    user = con.fetch_one(con.USERS_COLLECTION, {"Username": username})

    return user is not None


def _get_test_user():
    test_user = {}
    test_user['username'] = _get_test_username()
    test_user['name'] = _get_test_name()
    return test_user


def get_users():

    return con.fetch_all(con.USERS_COLLECTION)


def get_user(username: str) -> str:
    try:
        res = con.fetch_one(con.USERS_COLLECTION, {"_id": username})
    except ValueError:
        raise ValueError(f'User {username} does not exist')

    return res


def create_user(username: str, name: str) -> str:
    if len(username) < 5:
        raise ValueError(f'Username {username} is too short')

    if user_exists(username):
        raise ValueError(f'User {username} already exists')

    print(type(username))
    print(type(name))

    USERS[username] = {
        NAME: name,
        PANTRY: [],
        SAVED_RECIPES: {},
        INSTACART_USR: None,
        GROCERY_LIST: [],
        ALLERGENS: [],
    }

    return f'Successfully added {username}'


def remove_user(username):
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    del USERS[username]

    return f'Successfully deleted {username}'


def get_pantry(username):
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    return USERS[username][PANTRY]


def add_to_pantry(username: str, food: str) -> str:
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    USERS[username][PANTRY].append(food)
    return f'Successfully added {food}'


def get_recipes(username):
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    return USERS[username][SAVED_RECIPES]


def generate_recipe(username, query):
    app_key = '274c6a9381c49bc303a30cebb49c84d4'
    app_id = '29bf3511'
    query_string = 'https://api.edamam.com/api/recipes\
        /v2?type=public&q=' + query + '&app_id=' + app_id +\
        '&app_key=' + app_key
    x = requests.get(query_string)
    return x  # return full recipe response body


def add_to_recipes(username, recipe):
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    USERS[username][SAVED_RECIPES][recipe] = 0
    return f'Successfully added {recipe}'


def made_recipe(username, recipe):
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    USERS[username][SAVED_RECIPES][recipe] += 1
    return f'Successfully incremented streak counter for {recipe}'


def remove_recipe(username, recipe):
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    USERS[username][SAVED_RECIPES].remove(recipe)
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
