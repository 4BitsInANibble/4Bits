import datetime
from unittest.mock import patch
import server.endpoints as ep
import random
from string import ascii_uppercase
import data.users as usrs
import data.food as food
import pytest
import data.db_connect as con

from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
    CONFLICT,
    NO_CONTENT,
    UNAUTHORIZED
)

TEST_CLIENT = ep.app.test_client()

def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.HELLO_RESP in resp_json


def test_endpoints():
    resp = TEST_CLIENT.get(ep.ENDPOINTS_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.AVAIL_ENDPOINTS in resp_json


def recipe_return():
    return [{
        "name": "Egg Fried Rice",
        "ingredients":  [{
            food.INGREDIENT: "egg",
            food.QUANTITY: "2",
            food.UNITS: "each"
        },
        {
            food.INGREDIENT: "rice",
            food.QUANTITY: "2",
            food.UNITS: "c."
        },
        {
            food.INGREDIENT: "oil",
            food.QUANTITY: "1",
            food.UNITS: "tbsp."
        }]
    }]


@patch('data.users.get_users', return_value=[usrs._create_test_patch_user()], autospec=True)
def test_get_users(connect_db):
    resp = TEST_CLIENT.get(ep.USERS_EP)
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert resp.status_code == OK

@patch('data.users.validate_access_token', return_value=None, autospec=True)
@patch('data.users.get_user', return_value=usrs._create_test_patch_user(), autospec=True)
def test_get_user_valid(mock_token, mock_user):
    username = "TEST_USERNAME"
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}')
    print(f'{resp.get_json()}')
    assert resp.status_code == OK

@patch('data.users.validate_access_token', return_value=None, autospec=True)
@patch('data.users.get_user', side_effect=ValueError(), autospec=True)
def test_get_user_invalid(mock_token, mock_user):    
    username = "TEST_USERNAME"
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}')
    print(f'{resp=}')
    assert resp.status_code == CONFLICT


@patch('data.users.validate_access_token', return_value=None, autospec=True)
@patch('data.users.get_pantry', return_value=[food.get_food("Chicken", 1.0, "pound", False)],
       autospec=True)
def test_get_pantry_valid(mock_token, mock_pantry):
    username = "TEST_USERNAME"
    resp = TEST_CLIENT.get(f'{ep.PANTRY_EP}/{username}')
    assert resp.status_code == OK


@patch('data.users.validate_access_token', return_value=None, autospec=True)
@patch('data.users.get_pantry', side_effect=ValueError(), autospec=True)
def test_get_pantry_invalid(mock_token, mock_pantry):
    username = "TEST_USERNAME"
    resp = TEST_CLIENT.get(f'{ep.PANTRY_EP}/{username}')
    print(f'{ep.USERS_EP}/{username}{ep.PANTRY_EP}')
    assert resp.status_code == CONFLICT


@patch('data.users.validate_access_token', return_value=None, autospec=True)
@patch('data.users.add_to_pantry', return_value=[food.get_food("Chicken", 1.0, "pound", False)],
       autospec=True)
def test_add_to_pantry_valid(mock_token, mock_pantry):
    username = "TEST_USERNAME"
    data = {
        'food': [{
            food.INGREDIENT: "test chicken thigh",
            food.QUANTITY: 1.0,
            food.UNITS: "lbs.",
        }]
    }
    resp = TEST_CLIENT.patch(f'{ep.PANTRY_EP}/{username}', json=data)
    assert resp.status_code == OK


@patch('data.users.validate_access_token', return_value=None, autospec=True)
@patch('data.users.add_to_pantry', side_effect=ValueError(), autospec=True)
def test_add_to_pantry_invalid(mock_token, mock_pantry):
    username = "TEST_USERNAME"
    data = {
        'food': [{
            food.INGREDIENT: "test chicken thigh",
            food.QUANTITY: 1.0,
            food.UNITS: "lbs.",
        }]
    }
    resp = TEST_CLIENT.patch(f'{ep.PANTRY_EP}/{username}', json=data)
    print(f'{ep.USERS_EP}/{username}{ep.PANTRY_EP}')
    assert resp.status_code == CONFLICT


@patch('data.users.validate_access_token', return_value=None, autospec=True)
@patch('data.users.empty_grocery_list', return_value=None,
       autospec=True)
def test_empty_grocery_list_valid(mock_token, mock_pantry):
    username = "TEST_USERNAME"
    resp = TEST_CLIENT.patch(f'{ep.PANTRY_EP}/{username}{ep.EMPTY_LIST_EP}')
    assert resp.status_code == NO_CONTENT


@patch('data.users.validate_access_token', return_value=None, autospec=True)
@patch('data.users.empty_grocery_list', side_effect=ValueError(), autospec=True)
def test_empty_grocery_list_invalid(mock_token, mock_pantry):
    username = "TEST_USERNAME"
    resp = TEST_CLIENT.patch(f'{ep.PANTRY_EP}/{username}{ep.EMPTY_LIST_EP}')
    print(f'{ep.USERS_EP}/{username}{ep.PANTRY_EP}')
    assert resp.status_code == CONFLICT


@patch('data.users.validate_access_token', return_value=None, autospec=True)
@patch('data.users.get_saved_recipes', 
       return_value=recipe_return(),
       autospec=True)
def test_get_recipes_valid(mock_token, mock_recipes):
    username = "TEST_USERNAME"
    resp = TEST_CLIENT.get(f'{ep.RECIPE_EP}{ep.FAVORITE_EP}/{username}')
    assert resp.status_code == OK


@patch('data.users.validate_access_token', return_value=None, autospec=True)
@patch('data.users.add_to_saved_recipes', 
       return_value=recipe_return(),
       autospec=True)
def test_add_to_saved_recipes_valid(mock_token, mock_recipes):
    username = "TEST_USERNAME"
    data = {
        'recipe': "stir fry"
    }
    resp = TEST_CLIENT.patch(f'{ep.RECIPE_EP}{ep.FAVORITE_EP}/{username}', json=data)
    assert resp.status_code==OK

@patch('data.users.validate_access_token', return_value=None, autospec=True)
@patch('data.users.add_to_saved_recipes', side_effect=ValueError(), autospec=True)
def test_add_to_saved_recipes_invalid(mock_token, mock_recipes): #unsure... gayatri
    username = "TEST_USERNAME"
    data = {
        'recipe': "stir fry"
    }
    resp = TEST_CLIENT.patch(f'{ep.RECIPE_EP}{ep.FAVORITE_EP}/{username}', json=data)
    print(f'{resp=}')
    assert resp.status_code==CONFLICT


@patch('data.users.validate_access_token', return_value=None, autospec=True)
@patch('data.users.recommend_recipes', 
       return_value=recipe_return(),
       autospec=True)
def test_get_rec_recipes_valid(mock_token, mock_recipes):
    username = "TEST_USERNAME"
    resp = TEST_CLIENT.get(f'{ep.RECIPE_EP}{ep.RECOMMENDED_EP}/{username}')
    assert resp.status_code == OK


@patch('data.users.random_recipes', 
       return_value=recipe_return(),
       autospec=True)
def test_get_random_recipes_valid(mock_recipes):
    username = "TEST_USERNAME"
    resp = TEST_CLIENT.get(f'{ep.RECIPE_EP}{ep.RANDOM_EP}')
    assert resp.status_code == OK


@patch('data.users.validate_access_token', return_value=None, autospec=True)
@patch('data.users.get_saved_recipes', side_effect=ValueError(), autospec=True)
def test_get_recipes_invalid(mock_token, mock_recipes):
    username = "TEST_USERNAME"
    resp = TEST_CLIENT.get(f'{ep.RECIPE_EP}{ep.FAVORITE_EP}/{username}')
    resp_json = resp.get_json()
    assert resp.status_code == CONFLICT


@patch('data.users.validate_access_token', return_value=None, autospec=True)
@patch('data.users.remove_from_saved_recipes', return_value=None, autospec=True)
def test_remove_from_saved_recipes(mock_token, mock_recipes):
    username = "TEST_USERNAME"
    data = {
        'recipe': "stir fry"
    }
    resp = TEST_CLIENT.delete(f'{ep.RECIPE_EP}{ep.FAVORITE_EP}/{username}', json=data)
    resp_json = resp.get_json()
    assert resp.status_code == OK


@patch('data.users.validate_access_token', return_value=None, autospec=True)
@patch('data.users.remove_user', return_value=None, autospec=True)
def test_remove_user(mock_token, mock_remove):
    username = "TEST_USERNAME"
    resp = TEST_CLIENT.delete(f'{ep.USERS_EP}/{username}')
    assert resp.status_code == NO_CONTENT


@patch('data.users.validate_access_token', return_value=None, autospec=True)
@patch('data.users.remove_user', return_value=None, autospec=True)
def test_remove_nonexist_user(mock_token, mock_remove):
    username = usrs._get_test_username()
    resp = TEST_CLIENT.delete(f'{ep.USERS_EP}/{username}')
    assert resp.status_code == NO_CONTENT


@patch('data.users.refresh_user_token', return_value=("test", "test"), autospec=True)
def test_refresh_user_token(mock_add):
    data = {
        "refresh_token": "TEST_REFRESH_TOKEN"
    }

    resp = TEST_CLIENT.patch(f'{ep.USERS_EP}{ep.REFRESH_EP}', json=data)
    print(f'{resp=}')
    print(f'{ep.USERS_EP}{ep.REFRESH_EP}')
    assert resp.status_code == OK


@patch('data.users.validate_access_token', return_value=None, autospec=True)
@patch('data.users.logout_user', return_value=None, autospec=True)
def test_logout_user(mock_token, mock_add):
    test_username = "TEST_USERNAME"
    resp = TEST_CLIENT.patch(f'{ep.USERS_EP}/{test_username}{ep.LOGOUT_EP}')
    print(f'{resp=}')
    assert resp.status_code == OK
