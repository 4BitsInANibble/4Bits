"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask, request
from flask_restx import Resource, Api, fields
import data.users as users
from http.client import (
    OK,
    CONFLICT,
    UNAUTHORIZED,
    NO_CONTENT,
    BAD_REQUEST
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
AUTH_EP = '/auth'
LOGOUT_EP = '/logout'

user_fields = api.model('User', {
    "id_token": fields.String
})

test_fields = api.model('Test_User', {
    "name": fields.String
})

recipe_fields = api.model('Recipe', {
    "Recipe": fields.String,
})

pantry_fields = api.model('Pantry', {
    "Food": fields.String,
})


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
    @api.response(200, "Success")
    def get(self) -> dict:
        """
        This method returns all users.
        """
        data = users.get_users()
        print(f'{data=}')
        resp = {
                TYPE: DATA,
                TITLE: USER_TITLE,
                DATA: data,
            }
        print(f'{resp=}')

        return resp

    @api.expect(user_fields)
    @api.response(200, "Success")
    @api.response(403, "Unauthorized")
    @api.response(400, "Bad Request")
    def post(self):
        """
        This method creates a new user with an id_token
        in request body
        """
        data = request.json
        print(f'{data=}')

        try:
            id_token = data['id_token']
            users.generate_google_user(id_token)

            status = OK
        except ValueError:
            status = CONFLICT
        except users.AuthTokenExpired:
            status = UNAUTHORIZED
        except KeyError:
            status = BAD_REQUEST

        return None, status


@api.route(f'{USERS_EP}/<username>')
class UserById(Resource):
    @api.response(200, "Success")
    @api.response(409, "Conflict")
    @api.response(403, "Unauthorized")
    def get(self, username: str) -> dict:
        """
        This method returns a user of username 'username'
        """
        try:
            data = users.get_user(username)
            print(f"{data=}")
            resp = {
                TYPE: DATA,
                TITLE: USER_TITLE_SINGULAR,
                DATA: data,
            }
            status = OK
        except ValueError:
            resp = None
            status = CONFLICT
        except users.AuthTokenExpired:
            resp = None
            status = UNAUTHORIZED

        return resp, status

    @api.response(204, "No Content")
    @api.response(409, "Conflict")
    @api.response(403, "Unauthorized")
    def delete(self, username):
        """
        This method removes a user of username 'username'
        """
        try:
            users.remove_user(username)
            status = NO_CONTENT
        except ValueError:
            status = CONFLICT
        except users.AuthTokenExpired:
            status = UNAUTHORIZED

        return None, status

    @api.expect(user_fields)
    @api.response(204, "No Content")
    @api.response(409, "Conflict")
    def post(self, username):
        """
        Endpoint to test putting in users into db
        This method adds a user of username 'username' with a name field
        in the request body
        Eventually use this ep for self-implemented authentication/login system
        """
        try:
            data = request.json
            expiry = users._get_test_exp()
            users.create_user(username, data['name'], expiry)
            status = NO_CONTENT
        except ValueError:
            status = CONFLICT
        return None, status


@api.route(f'{USERS_EP}{AUTH_EP}')
class AuthUser(Resource):
    @api.response(204, "No Content")
    @api.response(409, "Conflict")
    def patch(self) -> dict:
        """
        This method accepts a google id_token and updates the
        expiry date of the corresponding user
        """
        data = request.json
        try:
            users.auth_user(data['id_token'])

            status = NO_CONTENT
        except ValueError:
            status = CONFLICT

        return None, status


@api.route(f'{USERS_EP}/<username>{LOGOUT_EP}')
class LogoutUser(Resource):
    @api.response(204, "No Content")
    @api.response(409, "Conflict")
    @api.response(403, "Unauthorized")
    def patch(self, username) -> dict:
        """
        This method sets the exp of a user to 0
        """
        try:
            users.logout_user(username)
            status = NO_CONTENT
        except ValueError:
            status = CONFLICT
        except users.AuthTokenExpired:
            status = UNAUTHORIZED

        return None, status


@api.route(f'{USERS_EP}/<username>{PANTRY_EP}')
class PantryById(Resource):
    @api.response(200, "Success")
    @api.response(409, "Conflict")
    def get(self, username: str) -> dict:
        """
        This method returns the pantry of user with name
        """
        try:
            data = users.get_pantry(username)
            resp = {
                TYPE: DATA,
                TITLE: PANTRY_TITLE,
                PANTRY_OWNER: username,
                DATA: data,
            }
            status = OK
        except ValueError:
            resp = None
            status = CONFLICT

        return resp, status

    @api.expect(pantry_fields)
    @api.response(200, "Success")
    @api.response(409, "Conflict")
    def post(self, username):
        data = request.json
        print(f'{data=}')

        try:
            resp = users.add_to_pantry(username, data['food'])
            status = OK
        except ValueError:
            resp = None
            status = CONFLICT

        return resp, status


@api.route(f'{USERS_EP}/<username>{RECIPE_EP}')
class RecipeById(Resource):
    @api.response(200, "Success")
    @api.response(409, "Conflict")
    def get(self, username):
        """
        This method returns the pantry of user with name
        """
        try:
            data = users.get_recipes(username)
            resp = {
                TYPE: DATA,
                TITLE: RECIPE_TITLE,
                RECIPE_OWNER: username,
                DATA: data,
            }
            status_code = OK
        except ValueError:
            resp = None
            status_code = CONFLICT

        return resp, status_code

    @api.expect(recipe_fields)
    @api.response(200, "Success")
    @api.response(409, "Conflict")
    def post(self, username):
        data = request.json
        print(f'{data=}')

        try:
            resp = users.add_to_recipes(username, data['recipe'])
            status = OK
        except ValueError:
            resp = None
            status = CONFLICT

        return resp, status
