"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask, request
from flask_restx import Resource, Api
import data.users as users


app = Flask(__name__)
api = Api(app)

DEFAULT = 'Default'
MENU = 'menu'
MAIN_MENU_EP = '/MainMenu'
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


@api.route('/endpoints')
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
        return {"Available endpoints": endpoints}


@api.route(f'/{MAIN_MENU_EP}')
@api.route('/')
class MainMenu(Resource):
    """
    This will deliver our main menu.
    """
    def get(self) -> dict:
        """
        Gets the main game menu.
        """
        return {'Title': MAIN_MENU_NM,
                'Default': 2,
                'Choices': {
                    '1': {'url': '/', 'method': 'get',
                          'text': 'List Available Characters'},
                    '2': {'url': '/',
                          'method': 'get', 'text': 'List Active Games'},
                    '3': {'url': f'/{USERS_EP}',
                          'method': 'get', 'text': 'List Users'},
                    'X': {'text': 'Exit'},
                }}


@api.route(f'/{USERS_EP}')
class Users(Resource):
    """
    This class supports fetching a list of all users.
    """
    def get(self) -> dict:
        """
        This method returns all users.
        """
        return {
                    TYPE: DATA,
                    TITLE: USER_TITLE,
                    DATA: users.get_users(),
                    MENU: USER_MENU_EP,
                    RETURN: MAIN_MENU_EP,
                }

    def post(self):
        data = request.json['data']
        print(f'{data=}')

        users.create_user(data['username'], data['name'])


@api.route(f'/{USERS_EP}/<username>')
class UserById(Resource):
    def get(self, username: str) -> dict:
        """
        This method returns a user of username 'username'
        """
        return {
            TYPE: DATA,
            TITLE: USER_TITLE_SINGULAR,
            DATA: users.get_user(username),
            MENU: USER_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }


@api.route(f'/{USERS_EP}/<username>/{PANTRY_EP}')
class PantryById(Resource):
    def get(self, username: str) -> dict:
        """
        This method returns the pantry of user with name
        """
        return {
            TYPE: DATA,
            TITLE: PANTRY_TITLE,
            PANTRY_OWNER: username,
            DATA: users.get_pantry(username),
            MENU: USER_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }
