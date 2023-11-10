"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask, request
from flask_restx import Resource, Api
import data.users as users
from http.client import (
    OK,
    CONFLICT,
)

app = Flask(__name__)
api = Api(app)

DEFAULT = 'Default'
MENU = 'menu'
MAIN_MENU_EP = '/MainMenu'
ENDPOINTS_EP = '/endpoints'
AVAIL_ENDPOINTS = "Available endpoints"
MAIN_MENU_NM = "Welcome to Text Game!"
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
# USERS = 'users'
USERS_EP = '/users'
USER_MENU_EP = '/user_menu'
USER_MENU_NM = 'User Menu'
TYPE = 'Type'
DATA = 'Data'
TITLE = 'Title'
USER_TITLE = 'Current Users'
USER_TITLE_SINGULAR = 'Current User'
PANTRY_TITLE = 'Pantry'
RETURN = 'Return'
PANTRY_EP = '/pantry'
PANTRY_OWNER = 'User'
RECIPE_TITLE = 'Recipe'
RETURN = 'Return'
RECIPE_EP = '/recipe'
RECIPE_OWNER = 'User'
USER_EXISTS = 'User_Exists'


@api.route('/hello')
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self) -> dict:
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {'hello': 'world'}


@api.route(f'{ENDPOINTS_EP}')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self) -> dict:
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {AVAIL_ENDPOINTS: endpoints}


@api.route(f'{USERS_EP}')
class Users(Resource):
    """
    This class supports fetching a list of all users.
    """
    def get(self) -> dict:
        """
        This method returns all users.
        """
        data = users.get_users()
        resp = {
                TYPE: DATA,
                TITLE: USER_TITLE,
                DATA: data,
            }

        return resp

    def post(self):
        """
        This method creates a new user with a username & name
        in request body
        """
        data = request.json
        print(f'{data=}')

        try:
            resp = users.create_user(data['username'], data['name'])
            status = OK
        except ValueError:
            resp = None
            status = CONFLICT

        print(resp, status)
        return resp, status


@api.route(f'{USERS_EP}/<username>')
class UserById(Resource):
    def get(self, username: str) -> dict:
        """
        This method returns a user of username 'username'
        """
        try:
            data = users.get_user(username)
            resp = {
                TYPE: DATA,
                TITLE: USER_TITLE_SINGULAR,
                DATA: data,
                USER_EXISTS: data != {}
            }
            status = OK
        except ValueError:
            resp = None
            status = CONFLICT

        return resp, status

    def delete(self, username):
        """
        This method removes a user of username 'username'
        """

        users.remove_user(username)
        return None, 204


@api.route(f'{USERS_EP}/<username>{PANTRY_EP}')
class PantryById(Resource):
    def get(self, username: str) -> dict:
        """
        This method returns the pantry of user with name
        """
        data = users.get_pantry(username)
        return {
            TYPE: DATA,
            TITLE: PANTRY_TITLE,
            PANTRY_OWNER: username,
            DATA: {} if data is None else data,
            USER_EXISTS: data is not None,
        }

    def post(self, username):
        data = request.json
        print(f'{data=}')

        resp = users.add_to_pantry(username, data['food'])

        if resp == f'User {username} does not exist':
            status = OK
        else:
            status = CONFLICT

        return resp, status


@api.route(f'{USERS_EP}/<username>{RECIPE_EP}')
class RecipeById(Resource):
    def get(self, username):
        """
        This method returns the pantry of user with name
        """
        data = users.get_recipes(username)
        return {
            TYPE: DATA,
            TITLE: RECIPE_TITLE,
            RECIPE_OWNER: username,
            DATA: {} if data is None else data,
            USER_EXISTS: data is not None,
        }

    def post(self, username):
        data = request.json
        print(f'{data=}')

        resp = users.add_to_recipes(username, data['recipe'])

        if resp == f'User {username} does not exist':
            status = OK
        else:
            status = CONFLICT

        return resp, status
