"""
This module interfaces with user data.
"""


INGREDIENT = 'ingredient'
QUANTITY = 'quantity'
UNITS = 'units'


def get_food(ingredient, quantity, units):
    food = {
        INGREDIENT: ingredient,
        QUANTITY: quantity,
        UNITS: units
    }

    return food
