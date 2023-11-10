import server.endpoints as ep
import random
from string import ascii_uppercase

from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
    CONFLICT,
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
    print(f'{ep.USERS_EP}/{username}')
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    usr = resp_json[ep.DATA]
    print(f'{usr=}')
    assert isinstance(usr, dict)
    assert usr != {}
    assert resp_json[ep.USER_EXISTS]


def test_get_user_invalid():
    username = ''.join(random.choices(ascii_uppercase, k=6))
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}')
    print(f'{ep.USERS_EP}/{username}')
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp.json=}')
    usr = resp_json[ep.DATA]
    print(f'{usr=}')
    assert isinstance(usr, dict)
    assert usr == {}
    assert not resp_json[ep.USER_EXISTS]


def test_get_pantry_valid():
    username = 'cc6956'
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}{ep.PANTRY_EP}')
    resp_json = resp.get_json()
    pantry_owner = resp_json[ep.PANTRY_OWNER]
    assert pantry_owner == username


def test_get_pantry_invalid():
    username = ''.join(random.choices(ascii_uppercase, k=6))
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}{ep.PANTRY_EP}')
    print(f'{ep.USERS_EP}/{username}{ep.PANTRY_EP}')
    print(f'{resp.status}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert not resp_json[ep.USER_EXISTS]


def test_get_recipes_valid():
    username = 'cc6956'
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}{ep.RECIPE_EP}')
    resp_json = resp.get_json()
    recipe_owner = resp_json[ep.RECIPE_OWNER]
    assert recipe_owner == username


def test_get_recipes_invalid():
    username = ''.join(random.choices(ascii_uppercase, k=6))
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}{ep.RECIPE_EP}')
    resp_json = resp.get_json()
    assert not resp_json[ep.USER_EXISTS]


def test_delete_user():
    username = 'cc6956'
    resp = TEST_CLIENT.delete(f'{ep.USERS_EP}/{username}')
    print(f'{resp=}')
    get_resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}')
    resp_json = get_resp.get_json()
    print(f'{resp_json=}')
    assert not resp_json[ep.USER_EXISTS]


def test_add_user():
    username = 'abc1234'
    name = 'Jane'
    data = {
        'username': username,
        'name': name
    }
    resp = TEST_CLIENT.post(f'{ep.USERS_EP}', json=data)
    print(f'{resp=}')
    get_resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{username}')
    resp_json = get_resp.get_json()
    print(f'{resp_json=}')
    assert resp_json[ep.USER_EXISTS]


def test_add_user_dup():
    username = 'gt2125'
    name = 'Jane'
    data = {
        'username': username,
        'name': name
    }
    resp = TEST_CLIENT.post(f'{ep.USERS_EP}', json=data)
    print(f'{resp=}')
    assert resp.status_code == 409

