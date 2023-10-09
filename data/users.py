"""
This module interfaces with user data.
"""

import data.food as food

NAME = 'Name'
PANTRY = 'Pantry'
SAVED_RECIPES = 'Saved_Recipes'
USERS = {
        'cc6956':
            {
                NAME: 'Calvin',
                PANTRY: [
                    food.get_food('chicken breast', 1, 'lb'),
                    food.get_food('soy sauce', 1, 'gal'),
                    ],
                SAVED_RECIPES: [

                    ],
            },
        'gt2125':
            {
                NAME: 'Gayatri',
                PANTRY: [
                    food.get_food('romaine lettace', 1, 'lb'),
                    food.get_food('egg', 24, 'count'),
                    ],
                SAVED_RECIPES: [

                    ],
            },
        'yh3595':
            {
                NAME: 'Jason',
                PANTRY: [
                    food.get_food('steak', 3, 'lb'),
                    food.get_food('potatoes', 5, 'count'),
                    ],
                SAVED_RECIPES: [

                    ],
            },
        'nz2065':
            {
                NAME: 'Nashra',
                PANTRY: [
                    food.get_food('chicken thigh', 0.25, 'lb'),
                    food.get_food('grapes', 5, 'count'),
                    ],
                SAVED_RECIPES: [

                    ],
            },
    }


def get_users():

    return USERS

def create_user(username, name):

    USERS[username] = {NAME: {name}, PANTRY: [], SAVED_RECIPES: [],}
    return USERS

def add_to_pantry(username, food):

    USERS[username][PANTRY].append(food)
    return 'Successfully added {food}'
