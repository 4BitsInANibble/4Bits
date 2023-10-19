"""
This module interfaces with user data.
"""

INGREDIENT = 'ingredient'
QUANTITY = 'quantity'
UNITS = 'units'
CATEGORY = 'category'

FOOD_CATEGORIES = {'produce', 'carbs', 'dairy', 'meat', 'oil',
                   'starch', 'vegetables', 'fruits'}


def get_food(ingredient, quantity, units):
    food = {
        INGREDIENT: ingredient,
        QUANTITY: quantity,
        UNITS: units,
        CATEGORY: get_food_category(ingredient),
    }

    return food


def get_food_category(food):
    # check if food category already in system
    category = check_food_category(food)

    if category is None:
        # Use open ai to categorize into food groups
        category = query_food_category(food)
        resp = add_database_food(food, category)
        if not resp:
            raise Exception("Food Category Database Insertion Error")

    return category


def check_food_category(food):
    pass


def query_food_category(food):
    pass


def add_database_food(food, category):
    """
    Add Food Category to the Database
    Return bool for success of database insertion
    """
    return True
