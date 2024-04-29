"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask, request
from flask_restx import Resource, Api, fields, Namespace
import data.users as users
import data.food as food
from flask_cors import CORS
from http.client import (
    OK,
    CONFLICT,
    UNAUTHORIZED,
    NO_CONTENT,
    BAD_REQUEST
)

app = Flask(__name__)
CORS(app)
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
FAVORITE_EP = '/favorite'
RECOMMENDED_EP = '/rec'
RANDOM_EP = '/random'
USERS_NS = 'users'
RECIPES_NS = 'recipe'
PANTRY_NS = 'pantry'
DEV_NS = 'developers'
RECIPE_LINKS_EP = '/links'

users_ns = Namespace(USERS_NS, 'Users')
api.add_namespace(users_ns)

recipes = Namespace(RECIPES_NS, 'Recipes')
api.add_namespace(recipes)

pantry = Namespace(PANTRY_NS, 'Pantry')
api.add_namespace(pantry)

dev = Namespace(DEV_NS, 'developers')
api.add_namespace(dev)


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

refresh_fields = api.model('Refresh_User', {
    "refresh_token": fields.String
})

login_fields = api.model('Login', {
    "username": fields.String,
    "password": fields.String
})

test_fields = api.model('Test_User', {
    "name": fields.String
})

ingredient_fields = api.model('Ingredient', {
    food.INGREDIENT: fields.String,
    food.QUANTITY: fields.Float,
    food.UNITS: fields.String
})

recipe_fields = api.model('Recipe', {
    "name": fields.String,
    "ingredients": fields.Nested(ingredient_fields),
    "link": fields.Url,
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


@users_ns.route('')
class Users(Resource):
    """
    This class supports fetching a list of all users.
    """
    @api.response(200, "Success")
    def get(self) -> dict:
        """
        This method returns all users.
        """
        resp = users.get_users()
        resp = users.convertObjectIds(resp)
        print(f'{resp=}')

        return resp

    @api.response(200, "Success")
    @api.response(409, "Conflict")
    @api.expect(registered_user_fields)
    def post(self):
        resp = None
        try:
            data = request.json
            username = data['username']
            name = data['name']
            password = data['password']

            token, refresh_token = users.register_user(
                username, name, password)

            resp = {
                "access_token": token,
                "refresh_token": refresh_token,
            }
            status = OK
        except ValueError as e:
            resp = str(e)
            status = CONFLICT
        return resp, status


@users_ns.route('/<username>')
class UserById(Resource):
    @api.response(200, "Success")
    @api.response(409, "Conflict")
    @api.response(403, "Unauthorized")
    def get(self, username: str) -> dict:
        """
        This method returns a user of username 'username'
        """
        access_token = request.headers.get('Authorization')
        try:
            users.validate_access_token(username, access_token)
            resp = users.get_user(username)
            resp = users.convertObjectIds(resp)
            status = OK
        except ValueError as e:
            resp = str(e)
            status = CONFLICT
        except users.AuthTokenExpired as e:
            resp = str(e)
            status = UNAUTHORIZED

        return resp, status

    @api.response(204, "No Content")
    @api.response(409, "Conflict")
    @api.response(403, "Unauthorized")
    def delete(self, username):
        """
        This method removes a user of username 'username'
        """
        resp = None
        access_token = request.headers.get('Authorization')
        try:
            users.validate_access_token(username, access_token)
            users.remove_user(username)
            status = NO_CONTENT
        except ValueError as e:
            resp = str(e)
            status = CONFLICT
        except users.AuthTokenExpired as e:
            resp = str(e)
            status = UNAUTHORIZED

        return resp, status


@users_ns.route(f'{REFRESH_EP}')
class RefreshUser(Resource):
    @api.expect(refresh_fields)
    @api.response(200, "OK")
    @api.response(409, "Conflict")
    def patch(self) -> dict:
        resp = None
        try:
            data = request.json
            refresh_token = data['refresh_token']
            print(f"ENDPOINT: {refresh_token}")
            token = users.refresh_user_token(refresh_token)

            resp = {
                "access_token": token,
            }
            print(f'{resp=}')
            status = OK
        except ValueError as e:
            resp = str(e)
            status = CONFLICT
        except KeyError:
            resp = "Did not include refresh token in request body"
            status = BAD_REQUEST

        return resp, status


@api.expect(login_fields)
@users_ns.route(f'{LOGIN_EP}')
class LoginUser(Resource):
    @api.response(200, "OK")
    @api.response(409, "Conflict")
    def patch(self) -> dict:
        """
        This method sets the exp of a user to 0
        """
        data = request.json
        try:
            username = data['username']
            password = data['password']
            token, refresh_token = users.login_user(username, password)
            resp = {
                "access_token": token,
                "refresh_token": refresh_token,
            }
            status = OK
        except ValueError as e:
            resp = str(e)
            status = CONFLICT

        return resp, status


@users_ns.route(f'/<username>{LOGOUT_EP}')
class LogoutUser(Resource):
    @api.response(200, "OK")
    @api.response(409, "Conflict")
    @api.response(403, "Unauthorized")
    def patch(self, username) -> dict:
        """
        This method sets the exp of a user to 0
        """
        resp = None
        access_token = request.headers.get('Authorization')
        try:
            users.validate_access_token(username, access_token)
            users.logout_user(username)
            resp = f"Successfully logged out {username}"
            status = OK
        except ValueError as e:
            resp = str(e)
            status = CONFLICT
        except users.AuthTokenExpired as e:
            resp = str(e)
            status = UNAUTHORIZED

        return resp, status


@users_ns.route(f'{REGISTER_EP}{GOOGLE_EP}')
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
        resp = None
        try:
            token = request.headers.get('Authorization')
            print(f'{token=}')
            users.generate_google_user(token)

            status = NO_CONTENT
        except ValueError as e:
            resp = str(e)
            status = CONFLICT
        except users.AuthTokenExpired as e:
            resp = str(e)
            status = UNAUTHORIZED
        except KeyError as e:
            resp = str(e)
            status = BAD_REQUEST

        return resp, status


@pantry.route('/<username>')
class PantryById(Resource):
    @api.response(200, "Success")
    @api.response(409, "Conflict")
    @api.response(403, "Unauthorized")
    def get(self, username: str) -> dict:
        """
        This method returns the pantry of user with name
        """
        access_token = request.headers.get('Authorization')
        try:
            users.validate_access_token(username, access_token)
            resp = users.get_pantry(username)
            resp = users.convertObjectIds(resp)
            status = OK
        except ValueError as e:
            resp = str(e)
            status = CONFLICT
        except users.AuthTokenExpired as e:
            resp = str(e)
            status = UNAUTHORIZED

        return resp, status

    @api.expect(pantry_fields)
    @api.response(200, "Success")
    @api.response(409, "Conflict")
    @api.response(403, "Unauthorized")
    def patch(self, username):
        data = request.json
        print(f'{data=}')
        access_token = request.headers.get('Authorization')
        try:
            users.validate_access_token(username, access_token)
            resp = users.add_to_pantry(username, data['food'])
            resp = users.convertObjectIds(resp)
            status = OK
        except ValueError as e:
            resp = str(e)
            status = CONFLICT
        except users.AuthTokenExpired as e:
            resp = str(e)
            status = UNAUTHORIZED

        return resp, status

    @api.response(200, "Success")
    @api.response(409, "Conflict")
    @api.response(403, "Unauthorized")
    def recognize_receipt(self, pic) -> dict:
        resp = users.recognize_receipt(pic)
        return resp


@recipes.route(f'{RECIPE_LINKS_EP}/<username>')
class RecipeLinks(Resource):
    @api.response(200, "Success")
    def get(self, username):
        resp = [
            {
                "name": "favorites",
                "href": f'{RECIPE_EP}{FAVORITE_EP}/{username}',
                "buttonLabel": "Favorites",
                "order": 0
            },
            {
                "name": "recommended",
                "href": f'{RECIPE_EP}{RECOMMENDED_EP}/{username}',
                "buttonLabel": "Best Matched",
                "order": 1
            },
            {
                "name": "random",
                "href": f'{RECIPE_EP}{RANDOM_EP}',
                "buttonLabel": "Random",
                "order": 2
            },
        ]
        status_code = OK
        return resp, status_code


@recipes.route(f'{FAVORITE_EP}/<username>')
class FavoriteRecipeById(Resource):
    @api.response(200, "Success")
    @api.response(409, "Conflict")
    @api.response(403, "Unauthorized")
    def get(self, username):
        """
        This method returns the saved recipes of user with name
        """
        access_token = request.headers.get('Authorization')
        try:
            users.validate_access_token(username, access_token)
            resp = users.get_saved_recipes(username, returnObjectId=False)
            resp = users.convertObjectIds(resp)
            status_code = OK
        except ValueError as e:
            resp = str(e)
            status_code = CONFLICT
        except users.AuthTokenExpired as e:
            resp = str(e)
            status_code = UNAUTHORIZED

        return resp, status_code

    @api.expect(recipe_fields)
    @api.response(200, "Success")
    @api.response(409, "Conflict")
    @api.response(403, "Unauthorized")
    def patch(self, username):
        data = request.json
        print(f'{data=}')
        access_token = request.headers.get('Authorization')
        try:
            users.validate_access_token(username, access_token)
            resp = users.add_to_saved_recipes(username, data['recipe'])
            resp = users.convertObjectIds(resp)
            status = OK
        except ValueError as e:
            resp = str(e)
            status = CONFLICT
        except users.AuthTokenExpired as e:
            resp = str(e)
            status = UNAUTHORIZED

        return resp, status

    @api.expect(recipe_fields)
    @api.response(200, "Success")
    @api.response(409, "Conflict")
    @api.response(403, "Unauthorized")
    def delete(self, username):
        data = request.json
        print(f'{data=}')
        access_token = request.headers.get('Authorization')
        try:
            users.validate_access_token(username, access_token)
            resp = users.remove_from_saved_recipes(username, data['recipe'])
            status = OK
        except ValueError as e:
            resp = str(e)
            status = CONFLICT
        except users.AuthTokenExpired as e:
            resp = str(e)
            status = UNAUTHORIZED

        return resp, status


@recipes.route(f'{RECOMMENDED_EP}/<username>')
class RecommendedRecipeById(Resource):
    @api.response(200, "Success")
    @api.response(409, "Conflict")
    @api.response(403, "Unauthorized")
    def get(self, username):
        """
        This method returns the pantry of user with name 'name'
        """
        access_token = request.headers.get('Authorization')
        try:
            users.validate_access_token(username, access_token)
            resp = users.recommend_recipes(username)
            resp = users.convertObjectIds(resp)
            status_code = OK
        except ValueError as e:
            resp = str(e)
            status_code = CONFLICT
        except users.AuthTokenExpired as e:
            resp = str(e)
            status_code = UNAUTHORIZED

        return resp, status_code


@recipes.route(f'{RANDOM_EP}')
class RandomRecipeById(Resource):
    @api.response(200, "Success")
    @api.response(409, "Conflict")
    @api.response(403, "Unauthorized")
    def get(self):
        """
        This method returns the pantry of user with name
        """
        try:
            resp = users.random_recipes()
            resp = users.convertObjectIds(resp)
            status_code = OK
        except ValueError as e:
            resp = str(e)
            status_code = CONFLICT
        except users.AuthTokenExpired as e:
            resp = str(e)
            status_code = UNAUTHORIZED

        return resp, status_code


@dev.route('/FetchAllUsers')
class FetchUsers(Resource):
    """
    This class supports fetching a list of all users.
    """
    @api.response(200, "Success")
    def get(self) -> dict:
        """
        This method returns all users.
        """
        resp = users.get_users()
        resp = users.convertObjectIds(resp)
        print(f'{resp=}')

        return resp

    @api.response(200, "Success")
    @api.response(409, "Conflict")
    @api.expect(registered_user_fields)
    def post(self):
        resp = None
        try:
            data = request.json
            username = data['username']
            name = data['name']
            password = data['password']

            token, refresh_token = users.register_user(
                username, name, password)

            resp = {
                "access_token": token,
                "refresh_token": refresh_token,
            }
            status = OK
        except ValueError as e:
            resp = str(e)
            status = CONFLICT
        return resp, status
