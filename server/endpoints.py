"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask, request
from flask_restx import Resource, Api, fields
import data.users as users
import data.food as food
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
REFRESH_EP = '/refresh'
LOGIN_EP = '/login'
LOGOUT_EP = '/logout'
GOOGLE_EP = '/google'
REGISTER_EP = '/register'
REGISTER_TITLE = "Registered User Data"

user_fields = api.model('User', {
    "Authorization": fields.String
})

test_user_fields = api.model('Test_User', {
    "Authorization": fields.String
})

registered_user_fields = api.model('Registered_User', {
    "username": fields.String,
    "name": fields.String,
    "password": fields.String
})

login_fields = api.model('Login', {
    "username": fields.String,
    "password": fields.String
})

test_fields = api.model('Test_User', {
    "name": fields.String
})

recipe_fields = api.model('Recipe', {
    "recipe": fields.String,
})


ingredient_fields = api.model('Ingredient', {
    food.INGREDIENT: fields.String,
    food.QUANTITY: fields.Float,
    food.UNITS: fields.String
})

pantry_fields = api.model('Pantry', {
    "food": fields.List(fields.Nested(ingredient_fields)),
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

    @api.response(200, "Success")
    @api.response(409, "Conflict")
    @api.expect(registered_user_fields)
    def post(self):
        data = None
        try:
            data = request.json
            username = data['username']
            name = data['name']
            password = data['password']

            data = users.register_user(username, name, password)
            status = OK
        except ValueError:
            status = CONFLICT
        resp = {
                TYPE: DATA,
                TITLE: REGISTER_TITLE,
                DATA: data,
            }
        return resp, status


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


@api.route(f'{USERS_EP}{REFRESH_EP}')
class RefreshUser(Resource):
    @api.response(204, "No Content")
    @api.response(409, "Conflict")
    def patch(self) -> dict:
        """
        This method accepts a google id_token and updates the
        expiry date of the corresponding user
        """
        resp = None
        try:
            data = request.json
            refresh_token = data['refresh_token']
            resp = users.refresh_user_token(refresh_token)

            status = OK
        except ValueError as e:
            resp = str(e)
            status = CONFLICT
        except users.AuthTokenExpired as e:
            resp = str(e)
            status = UNAUTHORIZED
        except KeyError:
            resp = "Did not include refresh token in request body"

        return resp, status


@api.expect(login_fields)
@api.route(f'{USERS_EP}{LOGIN_EP}')
class LoginUser(Resource):
    @api.response(204, "No Content")
    @api.response(409, "Conflict")
    def patch(self) -> dict:
        """
        This method sets the exp of a user to 0
        """
        data = request.json
        try:
            username = data['username']
            password = data['password']
            users.login_user(username, password)
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


@api.route(f'{USERS_EP}{REGISTER_EP}{GOOGLE_EP}')
class RegisterUserGoogle(Resource):
    @api.expect(user_fields)
    @api.response(200, "Success")
    @api.response(403, "Unauthorized")
    @api.response(400, "Bad Request")
    def post(self):
        """
        This method creates a new user with an id_token
        in request body
        """
        # data = request.json
        # print(f'{data=}')

        try:
            token = request.headers.get('Authorization')
            print(f'{token=}')
            users.generate_google_user(token)

            status = OK
        except ValueError:
            status = CONFLICT
        except users.AuthTokenExpired:
            status = UNAUTHORIZED
        except KeyError:
            status = BAD_REQUEST

        return None, status


@api.route(f'{USERS_EP}/<username>{PANTRY_EP}')
class PantryById(Resource):
    @api.response(200, "Success")
    @api.response(409, "Conflict")
    @api.response(403, "Unauthorized")
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
        except users.AuthTokenExpired:
            status = UNAUTHORIZED

        return resp, status

    @api.expect(pantry_fields)
    @api.response(200, "Success")
    @api.response(409, "Conflict")
    @api.response(403, "Unauthorized")
    def patch(self, username):
        data = request.json
        print(f'{data=}')

        try:
            resp = users.add_to_pantry(username, data['food'])
            status = OK
        except ValueError:
            resp = None
            status = CONFLICT
        except users.AuthTokenExpired:
            status = UNAUTHORIZED

        return resp, status


@api.route(f'{USERS_EP}/<username>{RECIPE_EP}')
class RecipeById(Resource):
    @api.response(200, "Success")
    @api.response(409, "Conflict")
    @api.response(403, "Unauthorized")
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
        except users.AuthTokenExpired:
            status_code = UNAUTHORIZED

        return resp, status_code

    @api.expect(recipe_fields)
    @api.response(200, "Success")
    @api.response(409, "Conflict")
    @api.response(403, "Unauthorized")
    def patch(self, username):
        data = request.json
        print(f'{data=}')

        try:
            resp = users.add_to_recipes(username, data['recipe'])
            status = OK
        except ValueError:
            resp = None
            status = CONFLICT
        except users.AuthTokenExpired:
            status = UNAUTHORIZED

        return resp, status
