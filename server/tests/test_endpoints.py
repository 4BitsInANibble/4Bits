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

TEST_OAUTH_TOKEN = {
        'email': "TESTING",
        'name': "TESTING",
        'exp': int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp())
    }

@pytest.fixture(scope='function')
def connect_db():
    con.connect_db()


@pytest.fixture(scope='function')
def valid_username():
    temp_user = False
    
    try:
        user = usrs.get_users()[0]
        print(f'{user}')
    except IndexError:
        temp_user = True
        user = usrs._create_test_user()
        
    username = user[usrs.USERNAME]
    
    print(f'{username=}')
    yield username

    if temp_user:
        usrs.remove_user(username)
    



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


def test_get_users(connect_db):
    resp = TEST_CLIENT.get(ep.USERS_EP)
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert isinstance(resp_json[ep.DATA], list)


def test_get_user_valid(connect_db, valid_username):
    username = valid_username
    print(f'{username=}')
    print(f'{usrs.user_exists(username)}')
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}')
    print(f'{resp.get_json()}')
    assert resp.status_code == OK


def test_get_user_invalid(connect_db):    
    username = ''.join(random.choices(ascii_uppercase, k=6))
    print(f"{username=}")
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}')
    print(f'{resp=}')
    assert resp.status_code == CONFLICT


def test_get_pantry_valid(connect_db, valid_username):
    username = valid_username
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}{ep.PANTRY_EP}')
    assert resp.status_code == OK


def test_get_pantry_invalid(connect_db):
    username = ''.join(random.choices(ascii_uppercase, k=6))
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}{ep.PANTRY_EP}')
    print(f'{ep.USERS_EP}/{username}{ep.PANTRY_EP}')
    assert resp.status_code == CONFLICT


def test_get_recipes_valid(connect_db, valid_username):
    username = valid_username
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}{ep.RECIPE_EP}')
    assert resp.status_code == OK


def test_get_recipes_invalid(connect_db):
    username = ''.join(random.choices(ascii_uppercase, k=6))
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}{ep.RECIPE_EP}')
    resp_json = resp.get_json()
    assert resp.status_code == CONFLICT


@patch('data.users.remove_user', return_value=None, autospec=True)
def test_remove_user(connect_db, valid_username):
    username = valid_username
    resp = TEST_CLIENT.delete(f'{ep.USERS_EP}/{username}')
    assert resp.status_code == NO_CONTENT


@patch('data.users.remove_user', return_value=None, autospec=True)
def test_remove_nonexist_user(connect_db):
    username = usrs._get_test_username()
    resp = TEST_CLIENT.delete(f'{ep.USERS_EP}/{username}')
    assert resp.status_code == NO_CONTENT


@patch('data.users.create_user', return_value=None, autospec=True)
@patch('google.oauth2.id_token.verify_oauth2_token', return_value=TEST_OAUTH_TOKEN, autospec=True)
def test_add_user(mock_add, mock_token):
    data = {
        "id_token": "TESTING"
    }

    resp = TEST_CLIENT.post(f'{ep.USERS_EP}', json=data)
    print(f'{resp=}')
    assert resp.status_code == OK

@patch('data.users.create_user', side_effect=ValueError(), autospec=True)
@patch('google.oauth2.id_token.verify_oauth2_token', return_value=TEST_OAUTH_TOKEN, autospec=True)
def test_add_user_dup(mock_add, mock_token):
    data = {
        "id_token": "TESTING"
    }

    resp = TEST_CLIENT.post(f'{ep.USERS_EP}', json=data)
    print(f'{resp=}')
    assert resp.status_code == CONFLICT


@patch('data.users.create_user', return_value=None, autospec=True)
@patch('google.oauth2.id_token.verify_oauth2_token', side_effect=usrs.AuthTokenExpired(), autospec=True)
def test_add_user_expired(mock_add, mock_token):
    data = {
        "id_token": "TESTING"
    }

    resp = TEST_CLIENT.post(f'{ep.USERS_EP}', json=data)
    print(f'{resp=}')
    assert resp.status_code == UNAUTHORIZED

