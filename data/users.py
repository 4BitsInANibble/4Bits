"""
This module interfaces with user data.
"""

import data.food

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


def get_users():

    return USERS


def get_user(username: str) -> str:
    if username not in USERS:
        raise KeyError()

    return USERS[username]


def create_user(username: str, name: str) -> dict:
    if username in USERS:
        raise Exception("User Already Exists")

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

    return USERS


def remove_user(username):
    if username not in USERS:
        raise KeyError()

    del USERS[username]

    return USERS


def get_pantry(username):
    if username not in USERS:
        raise KeyError(f'User {username} does not exist')

    return USERS[username][PANTRY]


def get_pantry(username):
    if username not in USERS:
        raise KeyError(f'User {username} does not exist')

    return USERS[username][PANTRY]


def add_to_pantry(username: str, food: str) -> str:
    if username not in USERS:
        raise KeyError(f'User {username} does not exist')

    USERS[username][PANTRY].append(food)
    return f'Successfully added {food}'


def get_recipes(username):
    if username not in USERS:
        raise KeyError(f'User {username} does not exist')

    return USERS[username][SAVED_RECIPES]


def add_to_recipes(username, recipe):
    if username not in USERS:
        raise KeyError(f'User {username} does not exist')

    USERS[username][SAVED_RECIPES].append(recipe)
    return f'Successfully added {recipe}'
