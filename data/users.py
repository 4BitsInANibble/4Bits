"""
This module interfaces with user data.
"""

import data.food
import random
from string import ascii_uppercase

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
            SAVED_RECIPES: [

                ],
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
            SAVED_RECIPES: [

                ],
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
            SAVED_RECIPES: [

                ],
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
            SAVED_RECIPES: [

                ],
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


def _get_test_user():
    test_user = {}
    test_user['username'] = _get_test_username()
    test_user['name'] = _get_test_name()
    return test_user


def get_users():

    return USERS


def get_user(username: str) -> str:
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    return USERS[username]


def create_user(username: str, name: str) -> str:
    if user_exists(username):
        raise ValueError(f'User {username} already exists')
    if len(username) < 5:
        raise ValueError(f'Username {username} is too short')

    print(type(username))
    print(type(name))

    USERS[username] = {
        NAME: name,
        PANTRY: [],
        SAVED_RECIPES: [],
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


def add_to_recipes(username, recipe):
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    USERS[username][SAVED_RECIPES].append(recipe)
    return f'Successfully added {recipe}'


def user_exists(username):
    return username in USERS
