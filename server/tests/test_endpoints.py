import datetime
from unittest.mock import patch
import server.endpoints as ep
import random
from string import ascii_uppercase
import data.users as usrs
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


@patch('data.users.get_users', return_value=None, autospec=True)
def test_get_users(connect_db):
    resp = TEST_CLIENT.get(ep.USERS_EP)
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert resp.status_code == OK


@patch('data.users.get_user', return_value=None, autospec=True)
def test_get_user_valid(mock_user):
    username = "TEST_USERNAME"
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}')
    print(f'{resp.get_json()}')
    assert resp.status_code == OK


@patch('data.users.get_user', side_effect=ValueError(), autospec=True)
def test_get_user_invalid(mock_user):    
    username = "TEST_USERNAME"
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}')
    print(f'{resp=}')
    assert resp.status_code == CONFLICT


@patch('data.users.get_pantry', return_value=None, autospec=True)
def test_get_pantry_valid(mock_pantry):
    username = "TEST_USERNAME"
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}{ep.PANTRY_EP}')
    assert resp.status_code == OK


@patch('data.users.get_pantry', side_effect=ValueError(), autospec=True)
def test_get_pantry_invalid(mock_pantry):
    username = "TEST_USERNAME"
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}{ep.PANTRY_EP}')
    print(f'{ep.USERS_EP}/{username}{ep.PANTRY_EP}')
    assert resp.status_code == CONFLICT


@patch('data.users.get_recipes', return_value=None, autospec=True)
def test_get_recipes_valid(mock_recipes):
    username = "TEST_USERNAME"
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}{ep.RECIPE_EP}')
    assert resp.status_code == OK


@patch('data.users.get_recipes', side_effect=ValueError(), autospec=True)
def test_get_recipes_invalid(mock_recipes):
    username = "TEST_USERNAME"
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}{ep.RECIPE_EP}')
    resp_json = resp.get_json()
    assert resp.status_code == CONFLICT


@patch('data.users.remove_user', return_value=None, autospec=True)
def test_remove_user(mock_remove):
    username = "TEST_USERNAME"
    resp = TEST_CLIENT.delete(f'{ep.USERS_EP}/{username}')
    assert resp.status_code == NO_CONTENT


@patch('data.users.remove_user', return_value=None, autospec=True)
def test_remove_nonexist_user(mock_remove):
    username = usrs._get_test_username()
    resp = TEST_CLIENT.delete(f'{ep.USERS_EP}/{username}')
    assert resp.status_code == NO_CONTENT


@patch('data.users.generate_google_user', return_value=None, autospec=True)
def test_add_google_user(mock_add):
    headers = {
        "Authorization": "TESTING",
    }

    resp = TEST_CLIENT.post(f'{ep.USERS_EP}{ep.REGISTER_EP}{ep.GOOGLE_EP}', headers=headers)
    print(f'{resp=}')
    assert resp.status_code == OK


@patch('data.users.generate_google_user', side_effect=ValueError(), autospec=True)
def test_add_google_user_dup(mock_add):
    headers = {
        "Authorization": "TESTING"
    }

    resp = TEST_CLIENT.post(f'{ep.USERS_EP}{ep.REGISTER_EP}{ep.GOOGLE_EP}', headers=headers)
    print(f'{resp=}')
    assert resp.status_code == CONFLICT


@patch('data.users.register_user', return_value=("test", "test"), autospec=True)
def test_add_google_user(mock_add):
    data = {
        "username": "TEST_USERNAME",
        "name": "TEST_NAME",
        "password": "TEST_PASSWORD",
    }

    resp = TEST_CLIENT.post(f'{ep.USERS_EP}', json=data)
    print(f'{resp=}')
    assert resp.status_code == OK


@patch('data.users.register_user', side_effect=ValueError(), autospec=True)
def test_add_google_user_dup(mock_add):
    data = {
        "username": "TEST_USERNAME",
        "name": "TEST_NAME",
        "password": "TEST_PASSWORD",
    }

    resp = TEST_CLIENT.post(f'{ep.USERS_EP}', json=data)
    print(f'{resp=}')
    assert resp.status_code == CONFLICT


@patch('data.users.refresh_user_token', return_value=("test", "test"), autospec=True)
def test_refresh_user_token(mock_add):
    data = {
        "refresh_token": "TEST_REFRESH_TOKEN"
    }

    resp = TEST_CLIENT.patch(f'{ep.USERS_EP}{ep.REFRESH_EP}', json=data)
    print(f'{resp=}')
    assert resp.status_code == OK


@patch('data.users.logout_user', return_value=None, autospec=True)
def test_logout_user(mock_add):
    test_username = "TEST_USERNAME"
    resp = TEST_CLIENT.patch(f'{ep.USERS_EP}/{test_username}{ep.LOGOUT_EP}')
    print(f'{resp=}')
    assert resp.status_code == NO_CONTENT
