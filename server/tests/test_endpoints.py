from unittest.mock import patch
import server.endpoints as ep
import random
from string import ascii_uppercase
import data.users as usrs

from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
    CONFLICT,
    NO_CONTENT
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


def test_get_users():
    resp = TEST_CLIENT.get(ep.USERS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json[ep.DATA], dict)


def test_get_user_valid():
    username = 'cc6956'
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}')
    assert resp.status_code == 200

def test_get_user_invalid():
    username = ''.join(random.choices(ascii_uppercase, k=6))
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}')
    print(f'{resp.get_json()}')
    assert resp.status_code == 409


def test_get_pantry_valid():
    username = 'cc6956'
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}{ep.PANTRY_EP}')
    assert resp.status_code == OK


def test_get_pantry_invalid():
    username = ''.join(random.choices(ascii_uppercase, k=6))
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}{ep.PANTRY_EP}')
    print(f'{ep.USERS_EP}/{username}{ep.PANTRY_EP}')
    assert resp.status_code == CONFLICT


def test_get_recipes_valid():
    username = 'cc6956'
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}{ep.RECIPE_EP}')
    assert resp.status_code == OK


def test_get_recipes_invalid():
    username = ''.join(random.choices(ascii_uppercase, k=6))
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}{ep.RECIPE_EP}')
    resp_json = resp.get_json()
    assert resp.status_code == CONFLICT


def test_delete_user():
    username = 'cc6956'
    resp = TEST_CLIENT.delete(f'{ep.USERS_EP}/{username}')
    assert resp.status_code == NO_CONTENT


@patch('data.users.create_user', return_value=None, autospec=True)
def test_add_user(mock_add):
    data = usrs._get_test_user()
    resp = TEST_CLIENT.post(f'{ep.USERS_EP}', json=data)
    print(f'{resp=}')
    assert resp.status_code == OK


@patch('data.users.create_user', side_effect=ValueError(), autospec=True)
def test_add_user_dup(mock_add):
    data = usrs._get_test_user()
    resp = TEST_CLIENT.post(f'{ep.USERS_EP}', json=data)
    print(f'{resp=}')
    assert resp.status_code == CONFLICT

