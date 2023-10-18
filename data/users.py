"""
This module interfaces with user data.
"""

import data.food

NAME = 'Name'
PANTRY = 'Pantry'
SAVED_RECIPES = 'Saved_Recipes'
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
        },
}


def get_users():

    return USERS


def get_user(username):
    if username not in USERS:
        raise KeyError()

    return USERS[username]


def create_user(username, name):
    if username in USERS:
        raise Exception("User Already Exists")

    print(type(username))
    print(type(name))

    USERS[username] = {
        NAME: name,
        PANTRY: [],
        SAVED_RECIPES: [],
    }

    return USERS


def add_to_pantry(username, food):
    if username not in USERS:
        raise KeyError(f'User {username} does not exist')

    USERS[username][PANTRY].append(food)
    return f'Successfully added {food}'


def get_pantry(username):
    if username not in USERS:
        raise KeyError(f'User {username} does not exist')

    return USERS[username][PANTRY]
