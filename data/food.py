"""
This module interfaces with user data.
"""
from typing import Optional
from bson.objectid import ObjectId

INGREDIENT = 'ingredient'
QUANTITY = 'quantity'
UNITS = 'units'
CATEGORY = 'category'

FOOD_CATEGORIES = {'produce', 'carbs', 'dairy', 'meat', 'oil',
                   'starch', 'vegetables', 'fruits'}


def get_food(ingredient: str, quantity: float, units: str, add_id=True) -> str:
    food = {
        INGREDIENT: ingredient,
        QUANTITY: quantity,
        UNITS: units,
        "_id": ObjectId()
        # CATEGORY: get_food_category(ingredient),
        # CATEGORY: None
    }

    if not add_id:
        del food['_id']

    return food


def get_food_category(food: str) -> str:
    # check if food category already in system
    category = check_food_category(food)

    if category is None:
        # Use open ai to categorize into food groups
        category = query_food_category(food)
        resp = add_database_food(food, category)
        if not resp:
            raise Exception("Food Category Database Insertion Error")

    return category


def check_food_category(food: str) -> Optional[str]:
    pass


def query_food_category(food: str) -> str:
    """
    Use chat-gpt to determine which category
    in FOOD_CATEGORIES food lies in
    """
    pass


def add_database_food(food: str, category: str) -> bool:
    """
    Add Food Category to the Database
    Return bool for success of database insertion
    """
    return True
