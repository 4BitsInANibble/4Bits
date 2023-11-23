import pytest

import data.db_connect as dbc

TEST_DB = dbc.RECIPE_DB
TEST_COLLECT = dbc.USERS_COLLECTION
# can be used for field and value:
TEST_NAME = 'test123'


@pytest.fixture(scope='function')
def temp_rec():
    dbc.connect_db()
    dbc.insert_one(TEST_COLLECT, {TEST_NAME: TEST_NAME})
    # yield to our test function
    yield
    dbc.del_one(TEST_COLLECT, {TEST_NAME: TEST_NAME})


def test_fetch_one(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: TEST_NAME})
    assert ret is not None


def test_fetch_one_not_there(temp_rec):
    try:
        ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: 'not a field value in db!'})
        assert False
    except ValueError:
        assert True