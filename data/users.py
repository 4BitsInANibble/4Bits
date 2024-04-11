"""
This module interfaces with user data.
"""

# import data.food
import os
import random
from string import ascii_uppercase
import data.db_connect as con
from PIL import Image
import pytesseract
import datetime
import openai
from google.oauth2 import id_token
from google.auth.transport import requests
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import data.food as fd
from bson import ObjectId

TEST_USERNAME_LENGTH = 6
TEST_NAME_LENGTH = 6

NAME = 'Name'
PANTRY = 'Pantry'
USERNAME = "Username"
SAVED_RECIPES = 'Saved_Recipes'
INSTACART_USR = 'Instacart_User_Info'
GROCERY_LIST = 'Grocery List'
ALLERGENS = 'Allergens'
AUTH_EXPIRES = "Auth_Exp"
AUTH_TYPE = "Auth_Type"
PASSWORD = "Password"
REFRESH_TOKEN = 'Refresh_Token'
STREAK = "Streakz"


class AuthTokenExpired(Exception):
    pass


# TEST SETUP
def generate_exp():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=1)


def user_exists(username):
    con.connect_db()
    try:
        con.fetch_one(con.USERS_COLLECTION, {USERNAME: username})
        res = True
    except ValueError:
        res = False
    return res


def _get_test_username():
    con.connect_db()
    username = ''.join(random.choices(ascii_uppercase, k=TEST_USERNAME_LENGTH))
    while user_exists(username):
        username = ''.join(random.choices(
            ascii_uppercase, k=TEST_USERNAME_LENGTH))
    return username


def _get_test_name():
    con.connect_db()
    name = ''.join(random.choices(ascii_uppercase, k=TEST_NAME_LENGTH))

    return name


def _get_test_auth_token(username="TESTING"):
    return {
        'email': username,
        'name': username,
        'exp': int(generate_exp().timestamp())
    }


def _create_test_google_user():
    username = _get_test_username()
    name = _get_test_name()
    exp = generate_exp()
    print(username, name, exp)
    test_user = create_user(username, name, exp)
    return test_user


def _create_test_user():
    username = _get_test_username()
    name = _get_test_name()
    password = "TEST_PASSWORD"
    register_user(username, name, password)
    return username


def _create_test_patch_user():
    username = "TEST"
    name = "TEST"
    auth_type = "Google"
    password = "password"
    new_user = {
        USERNAME: username,
        NAME: name,
        PANTRY: [],
        SAVED_RECIPES: [],
        INSTACART_USR: None,
        GROCERY_LIST: [],
        ALLERGENS: [],
        AUTH_TYPE: auth_type,
        AUTH_EXPIRES: 0,
        PASSWORD: password
    }
    return new_user


def convertObjectIds(obj):
    print(f"{obj=}")
    if isinstance(obj, dict):
        return convertObjectIdsDict(obj)
    elif isinstance(obj, list):
        return convertObjectIdsList(obj)
    else:
        return obj


def convertObjectIdsDict(obj: dict):
    for key in obj:
        if isinstance(obj[key], dict):
            obj[key] = convertObjectIdsDict(obj[key])
        elif isinstance(obj[key], list):
            obj[key] = convertObjectIdsList(obj[key])
        elif isinstance(obj[key], ObjectId):
            obj[key] = str(obj[key])
    return obj


def convertObjectIdsList(obj: list):
    for i in range(len(obj)):
        if isinstance(obj[i], dict):
            obj[i] = convertObjectIdsDict(obj[i])
        elif isinstance(obj[i], list):
            obj[i] = convertObjectIdsList(obj[i])
        elif isinstance(obj[i], ObjectId):
            obj[i] = str(obj[i])
    return obj


# USER METHODS
def get_users():
    con.connect_db()
    users = con.fetch_all(con.USERS_COLLECTION)
    return users


def get_user(username: str) -> str:
    con.connect_db()
    if auth_expired(username):
        raise AuthTokenExpired("User's Authentication Token is expired")
    try:
        res = con.fetch_one(con.USERS_COLLECTION, {USERNAME: username})
        res[con.MONGO_ID] = str(res[con.MONGO_ID])
    except ValueError:
        raise ValueError(f'User {username} does not exist')

    return res


def create_user(username: str, name: str,
                expires: datetime.datetime, password=None,
                refresh_token=None) -> dict:
    con.connect_db()
    if len(username) < 5:
        raise ValueError(f'Username {username} is too short. Username should\
         be at least 5 characters.')

    if user_exists(username):
        raise ValueError(f'User {username} already exists')

    if len(username) > 25:
        raise ValueError(f'Username {username} is too long. Username should\
         be at most 25 characters.')
    auth_type = "Google" if password is None else "Self"

    new_user = {
        USERNAME: username,
        NAME: name,
        PANTRY: [],
        SAVED_RECIPES: [],
        INSTACART_USR: None,
        GROCERY_LIST: [],
        ALLERGENS: [],
        AUTH_TYPE: auth_type,
        AUTH_EXPIRES: int(expires.timestamp()),
        PASSWORD: password,
        REFRESH_TOKEN: refresh_token
    }

    add_ret = con.insert_one(con.USERS_COLLECTION, new_user)
    print(f'{add_ret}')
    return new_user


def remove_user(username):
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')
    if auth_expired(username):
        raise AuthTokenExpired("User's authentication token is expired")

    del_res = con.del_one(con.USERS_COLLECTION, {USERNAME: username})

    print(f'{del_res}')
    return f'Successfully deleted {username}'


def login_user(username, password):
    print(f'{username}')
    con.connect_db()
    if not user_exists(username):
        print('user_Exists')
        raise ValueError(f'User {username} does not exist')

    user_password_obj = con.fetch_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {PASSWORD: 1, con.MONGO_ID: 0}
    )
    user_password = user_password_obj[PASSWORD]

    if not check_password_hash(user_password, password):
        print("password")
        raise ValueError('Password does not match')

    exp = int(generate_exp().timestamp())
    print(exp)
    access_token = generate_jwt(username, exp)
    refresh_token = generate_refresh_token(username)

    print(access_token)

    con.update_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {"$set": {AUTH_EXPIRES: exp, REFRESH_TOKEN: refresh_token}}
    )
    print("JSDFKLSJD")
    return access_token, refresh_token


def logout_user(username):
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')
    if auth_expired(username):
        raise AuthTokenExpired("User's authentication token is expired")

    con.update_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {"$set": {AUTH_EXPIRES: 0}}
    )


def register_user(username, name, password):
    hashed_password = generate_password_hash(password, method='scrypt')
    exp = generate_exp()
    token = generate_jwt(username, exp.timestamp())
    refresh_token = generate_refresh_token(username)

    create_user(username, name, exp, hashed_password, refresh_token)

    return token, refresh_token


# AUTHENTICATION METHODS
def auth_expired(username: str) -> bool:
    exp = con.fetch_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {AUTH_EXPIRES: 1, con.MONGO_ID: 0}
    )

    return exp[AUTH_EXPIRES] <= datetime.datetime.utcnow().timestamp()


def valid_authentication(google_id_token):
    # Add check for CLIENT ID for app that accesses authentication
    # Maybe save valid CLIENT ID to check against in os.environ()
    idinfo = id_token.verify_oauth2_token(google_id_token, requests.Request())

    # aud = idinfo['aud']
    # if os.environ.get("GOOGLE_CLIENT_ID") != aud:
    #     raise ValueError("Invalid Token")

    exp = idinfo['exp']
    if exp < datetime.datetime.utcnow().timestamp():
        raise AuthTokenExpired("Expired token")
    return idinfo


def generate_refresh_token(username):
    # Set the expiration time, e.g., 30 days from now
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=30)

    refresh_token = generate_jwt(username, expiration_time.timestamp())

    return refresh_token


def refresh_user_token(refresh_token):
    con.connect_db()
    try:

        payload = jwt.decode(
            refresh_token,
            key=os.environ.get("JWT_SECRET_KEY"),
            algorithms='HS256',
            verify=True
        )
        print(payload)
        if datetime.datetime.utcnow().timestamp() > payload[AUTH_EXPIRES]:
            raise ValueError("Refresh Token Expired")
        print("HIIII")

        stored_refresh_token = con.fetch_one(
            con.USERS_COLLECTION,
            {USERNAME: payload[USERNAME]},
            {REFRESH_TOKEN: 1, con.MONGO_ID: 0}
        )[REFRESH_TOKEN]
        print(f'TOKENS: {refresh_token}: {stored_refresh_token}')

        if refresh_token != stored_refresh_token:
            raise ValueError("Invalid Refresh Token")

        exp = generate_exp().timestamp()
        con.update_one(
            con.USERS_COLLECTION,
            {USERNAME: payload[USERNAME]},
            {"$set": {AUTH_EXPIRES: exp}}
        )
        return generate_jwt(payload[USERNAME], exp)
    except jwt.ExpiredSignatureError:
        raise ValueError("Refresh Token Expired")
    except jwt.InvalidTokenError as e:
        print(str(e))
        raise ValueError("Invalid Refresh Token")


def auth_user(token):
    auth_user_google(token)


def auth_user_google(google_id_token):
    con.connect_db()
    try:
        id_info = valid_authentication(google_id_token)
        username = id_info['email']
        if not user_exists(username):
            raise ValueError("User associated with token does not exist")

        exp = int(id_info['exp'])

        con.update_one(
            con.USERS_COLLECTION,
            {USERNAME: username},
            {"$set": {AUTH_EXPIRES: exp}}
        )

    except ValueError as ex:
        # Invalid token
        raise ex
    except AuthTokenExpired as ex:
        raise ex


def generate_google_user(google_id_token):
    id_info = valid_authentication(google_id_token)

    username = id_info['email']
    name = id_info['name']
    exp = int(id_info['exp'])
    print(username, name, exp)
    create_user(username, name, exp)


def generate_jwt(username, exp):

    # Create the JWT payload
    payload = {
        USERNAME: username,
        AUTH_EXPIRES: exp
    }

    # Encode the JWT
    # Run openssl rand -base64 12 to generate password
    token = jwt.encode(
        payload,
        os.environ.get("JWT_SECRET_KEY"),
        algorithm='HS256'
    )

    return token


# PANTRY METHODS
def get_pantry(username):
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')
    if auth_expired(username):
        raise AuthTokenExpired("User's authentication token is expired")

    pantry = con.fetch_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {PANTRY: 1}
    )

    return pantry[PANTRY]


def add_to_pantry(username: str, food):
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')
    if auth_expired(username):
        raise AuthTokenExpired("User's authentication token is expired")
    print(food)

    new_pantry_entries = [create_ingredient(fd.get_food(
        ingredient[fd.INGREDIENT],
        ingredient[fd.QUANTITY],
        ingredient[fd.UNITS]
        )) for ingredient in food]

    con.update_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {"$push": {PANTRY: {"$each": new_pantry_entries}}}
    )
    return new_pantry_entries


def create_ingredient(ingredient):
    ingredient[fd.INGREDIENT] = add_to_foods(ingredient[fd.INGREDIENT])
    return ingredient


def add_to_foods(food):
    con.connect_db()
    ingr_id = None
    try:
        ingr_obj = con.fetch_one(
            con.FOOD_COLLECTION,
            {"name": food}
        )
        ingr_id = ObjectId(ingr_obj['_id'])
    except ValueError:
        ingr_obj = con.insert_one(
            con.FOOD_COLLECTION,
            {"name": food}
        )
        ingr_id = ingr_obj.inserted_id
    return ingr_id


def check_low_stock_pantry(username):
    # of pantry items with their quantities for a given user
    pantry_items = get_pantry(username)
    low_stock_items = []

    # Define a threshold for low stock
    low_stock_threshold = 2  # Example threshold, adjust as needed

    for item in pantry_items:
        if (item['quantity'] <= low_stock_threshold):
            low_stock_items.append(item)

    return low_stock_items


def modify_pantry_ingredient_amount(username, ingredient_name, new_amount):
    # Assume a function connect_db() that connects to the database
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')

    # Find the user's pantry
    pantry = con.fetch_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {PANTRY: 1}
    )
    print(pantry)

    # Check if ingredient exists in the pantry, then update its amount
    for ingredient in pantry[PANTRY]:
        try:
            food = con.fetch_one(
                con.FOOD_COLLECTION,
                {
                    con.MONGO_ID: ingredient[fd.INGREDIENT]
                }
            )
            print(f'{ingredient=}')
            # # Update the amount for the ingredient
            # ingredient['quantity'] = new_amount

            # Save the updated pantry
            if food['name'] == ingredient_name:
                con.update_one(
                    con.USERS_COLLECTION,
                    {
                        # USERNAME: username,
                        # f'{PANTRY}.{fd.INGREDIENT}': food_id,
                        f'{PANTRY}.{con.MONGO_ID}': ingredient[con.MONGO_ID]
                    },
                    {"$set": {f"{PANTRY}.$.{fd.QUANTITY}": new_amount}}
                )
                return f'Updated {ingredient_name} \
                    to {new_amount} in {username}\'s pantry'
        except ValueError:
            pass
    raise ValueError(f'Ingredient {ingredient_name} not found in pantry')


# RECIPE METHODS
def get_saved_recipes(username, returnObjectId=True):

    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')
    if auth_expired(username):
        raise AuthTokenExpired("User's authentication token is expired")

    recipes = con.fetch_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {SAVED_RECIPES: 1, con.MONGO_ID: 0}
    )
    recipe_ids = [ObjectId(rec) for rec in recipes[SAVED_RECIPES]]
    print(f'{recipe_ids=}')

    recipe_objs = []
    for recipe_id in recipe_ids:
        print(f'{type(recipe_id)}')
        try:
            print("JFSDKLF")
            recipe_obj = con.fetch_one(
                con.RECIPE_COLLECTION,
                {con.MONGO_ID: recipe_id}
            )
            print("JFSDKLF")
            recipe_objs.append(
                recipe_obj
            )
            if returnObjectId:
                recipe_objs[-1][con.MONGO_ID] = \
                    ObjectId(recipe_objs[-1][con.MONGO_ID])
            for i in range(len(recipe_objs[-1]["ingredients"])):
                ingr = recipe_objs[-1]["ingredients"][i]
                print(f'{ingr=}')
                recipe_objs[-1]["ingredients"][i][fd.INGREDIENT] = \
                    con.fetch_one(
                        con.FOOD_COLLECTION,
                        {con.MONGO_ID: ingr[fd.INGREDIENT]},
                        {con.MONGO_ID: returnObjectId}
                    )
        except Exception as e:
            print("COULDNT FIND SHIT")
            print(e)

    print(f'{recipe_objs=}')
    return recipe_objs


def generate_recipe(username, query):
    app_key = '274c6a9381c49bc303a30cebb49c84d4'
    app_id = '29bf3511'
    query_string = 'https://api.edamam.com/api/recipes\
        /v2?type=public&q=' + query + '&app_id=' + app_id +\
        '&app_key=' + app_key
    x = requests.get(query_string)
    return x  # return full recipe response body


def add_to_saved_recipes(username, recipe):
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')
    if auth_expired(username):
        raise AuthTokenExpired("User's authentication token is expired")

    check_recipe_schema(recipe)

    recipe_id = None
    existing_recipe = None
    try:
        existing_recipe = con.fetch_one(
            con.RECIPE_COLLECTION,
            {"name": recipe['name']}
        )
        print(f"EXISTING RECIPE: {existing_recipe=}")
        recipe_id = existing_recipe["_id"]
    except ValueError:
        print("NEW RECIPE")
        recipe_id = add_to_recipes(recipe)
        print(f"{recipe=}")
        print(f"{recipe['ingredients']=}")
    print(f"{recipe_id=}")

    current_saved_recipes = con.fetch_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {SAVED_RECIPES: 1, con.MONGO_ID: 0}
    )
    for rec in current_saved_recipes[SAVED_RECIPES]:
        print(f"{rec=}")
        if rec == recipe_id:
            raise ValueError("User already has recipe saved")

    con.update_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {"$push": {SAVED_RECIPES: recipe_id}}
    )

    if existing_recipe is None:
        existing_recipe = con.fetch_one(
            con.RECIPE_COLLECTION,
            {"name": recipe['name']}
        )

    con.update_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {"$push": {GROCERY_LIST: {"$each": existing_recipe['ingredients']}}}
    )

    return f'Successfully added {recipe} and updated grocery list'


def add_to_recipes(recipe):
    con.connect_db()

    check_recipe_schema(recipe)
    add_ret = None
    existing_recipe = None
    try:
        existing_recipe = con.fetch_one(
            con.RECIPE_COLLECTION,
            {'name': recipe['name']}
        )

    except ValueError:
        ingredients = [create_ingredient(fd.get_food(
            ingredient[fd.INGREDIENT],
            ingredient[fd.QUANTITY],
            ingredient[fd.UNITS])
        ) for ingredient in recipe['ingredients']]

        # ingredient_ids = []
        # for ingr in ingredients:
        #     ingredient_ids.append(ingr)
        # print(f"{ingredient_ids=}")

        recipe["ingredients"] = ingredients
        print(f"{recipe=}")

        add_ret = con.insert_one(
            con.RECIPE_COLLECTION,
            recipe
        )

    if add_ret is not None:
        recipe_id = add_ret.inserted_id
        # Update grocery list with ingredients from the recipe
    elif existing_recipe is not None:
        recipe_id = existing_recipe[con.MONGO_ID]
    else:
        recipe_id = None

    return recipe_id


def remove_from_saved_recipes(username, recipe):
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')
    if auth_expired(username):
        raise AuthTokenExpired("User's authentication token is expired")

    recipe_obj = con.fetch_one(
        con.RECIPE_COLLECTION,
        {
            "name": recipe
        }
    )
    con.update_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {"$pull": {SAVED_RECIPES: recipe_obj[con.MONGO_ID]}}
    )

    return f'Successfully deleted {recipe}'


def generate_recipe_gpt(username, query):   # generate recipe with AI
    openai.api_key = os.environ.get("OPENAI_KEY")
    pantry_items = get_pantry(username)  # Retrieve the user's pantry items

    # Format the pantry items into a string
    pantry_string = ', '.join(pantry_items)

    # Include the pantry items in the prompt
    prompt = f"""Given the following pantry items:
        {pantry_string}, and based on the following requirements,
        {query}, please recommend a recipe:\n\nRecipe:"""

    # Make the API call
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=200  # Adjust as needed
    )

    # Extract the recommended recipe from the response
    recommended_recipe = response.choices[0].text.strip()
    return recommended_recipe


def check_recipe_schema(recipe):
    fields = ["name", "ingredients"]
    optional_fields = ["url"]
    for field in fields:
        if field not in recipe:
            raise ValueError(f"{field} not included in recipe")

    num_optional = 0
    for field in optional_fields:
        if field in recipe:
            num_optional += 1

    if len(recipe.keys()) != len(fields) + num_optional:
        raise ValueError("Unnecessary fields included in recipe")


# GROCERY LIST METHODS
def get_grocery_list(username):
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')
    if auth_expired(username):
        raise AuthTokenExpired("User's authentication token is expired")

    grocery_list_res = con.fetch_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {GROCERY_LIST: 1, con.MONGO_ID: 0}
    )

    return grocery_list_res[GROCERY_LIST]


def add_to_grocery_list(username: str, food) -> str:
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')
    if auth_expired(username):
        raise AuthTokenExpired("User's authentication token is expired")
    print(food)

    new_list_entries = [create_ingredient(fd.get_food(
        ingredient[fd.INGREDIENT],
        ingredient[fd.QUANTITY],
        ingredient[fd.UNITS]
        )) for ingredient in food]

    con.update_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {"$push": {GROCERY_LIST: {"$each": new_list_entries}}}
    )
    return f'Successfully added {food}'


def recommend_recipes(username):
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')
    if auth_expired(username):
        raise AuthTokenExpired("User's authentication token is expired")

    pantry = get_pantry(username)
    pantry_ids = [ingr["ingredient"] for ingr in pantry]
    print(f'{pantry_ids=}')

    pipeline = [
        {"$unwind": "$ingredients"},
        {"$project": {
            "_id": 1,
            "ingredient": "$ingredients.ingredient"
        }},
        {"$match": {"ingredient": {"$in": pantry_ids}}},
        {"$group": {
            "_id": '$_id',
            "count": {"$sum": 1}
        }},
        {"$project": {
            "_id": 1,
            "count": 1,
            "score": {"$divide": [
                "$count", len(pantry_ids)
            ]}
        }},
        {"$sort": {
            "score": -1
        }},
        {"$limit": 20}
    ]

    res = con.aggregate(
        con.RECIPE_COLLECTION,
        pipeline
    )
    print(f'{res=}')
    res_list = []
    for e in res:
        try:
            recipe_obj = con.fetch_one(
                con.RECIPE_COLLECTION,
                {con.MONGO_ID: e['_id']}
            )
            res_list.append(recipe_obj)
            for i in range(len(res_list[-1]["ingredients"])):
                ingr = res_list[-1]["ingredients"][i]
                print(f'{ingr=}')
                res_list[-1]["ingredients"][i][fd.INGREDIENT] = con.fetch_one(
                    con.FOOD_COLLECTION,
                    {con.MONGO_ID: ingr[fd.INGREDIENT]},
                    {con.MONGO_ID: 0}
                )
        except ValueError as e:
            print("couldn't find the obtained recipe")
            print(e)

    print(f'{res_list=}')
    return res_list


def random_recipes():
    con.connect_db()

    pipeline = [
        {"$sample": {
            "size": 20
        }}
    ]

    res = con.aggregate(
        con.RECIPE_COLLECTION,
        pipeline
    )
    print(res)
    res_list = []
    for e in res:
        try:
            recipe_obj = con.fetch_one(
                con.RECIPE_COLLECTION,
                {con.MONGO_ID: e['_id']}
            )
            res_list.append(recipe_obj)
            for i in range(len(res_list[-1]["ingredients"])):
                ingr = res_list[-1]["ingredients"][i]
                print(f'{ingr=}')
                res_list[-1]["ingredients"][i][fd.INGREDIENT] = con.fetch_one(
                    con.FOOD_COLLECTION,
                    {con.MONGO_ID: ingr[fd.INGREDIENT]},
                    {con.MONGO_ID: 0}
                )
        except ValueError as e:
            print("couldn't find the obtained recipe")
            print(e)

    return res_list


def validate_access_token(username, token):
    con.connect_db()
    token_list = token.split(' ')
    if "Bearer" == token_list[0]:
        token = token_list[1]
    print(token)
    print(token_list)
    payload = jwt.decode(
        token,
        key=os.environ.get("JWT_SECRET_KEY"),
        algorithms='HS256',
        verify=True
    )
    exp = con.fetch_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {AUTH_EXPIRES: 1, con.MONGO_ID: 0}
    )
    if AUTH_EXPIRES not in exp:
        raise ValueError("Db schema error")

    exp = exp[AUTH_EXPIRES]

    if payload[USERNAME] != username:
        raise ValueError("Invalid Auth Token")
    if datetime.datetime.utcnow().timestamp() > payload[AUTH_EXPIRES]:
        raise AuthTokenExpired("Authentication Token Expired")


def get_streak(username):
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')
    if auth_expired(username):
        raise AuthTokenExpired("User's authentication token is expired")

    recipes_res = con.fetch_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {STREAK: 1, con.MONGO_ID: 0}
    )

    return recipes_res[STREAK]


def inc_streak(username):
    con.connect_db()
    if not user_exists(username):
        raise ValueError(f'User {username} does not exist')
    if auth_expired(username):
        raise AuthTokenExpired("User's authentication token is expired")

    con.update_one(
        con.USERS_COLLECTION,
        {USERNAME: username},
        {"$inc": {STREAK: 1}}
    )

    return 'Successfully incremented streak counter'


def recognize_receipt(username: str, image_path=None, image=None):
    openai.api_key = os.environ.get("OPENAI_KEY")
    if (image_path and not image):
        # Load the image from the specified path
        image = Image.open(image_path)
    elif (not image):  # neither the path nor image is provided
        return None
    # Perform OCR using pytesseract
    ocr_text = pytesseract.image_to_string(image)
    # Print or save the extracted text
    print(ocr_text)
    prompt = f"Extract pantry items from the following text: {ocr_text}"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=200
    )
    # Extract the generated text from ChatGPT's response
    generated_text = response.choices[0].text.strip()
    # Split the generated text into individual pantry items
    pantry_items = generated_text.split('\n')
    return pantry_items
    # # Remove any empty or whitespace-only items
    # pantry_items = [item.strip() for item in pantry_items if item.strip()]
    # for food in pantry_items:
    #     add_to_pantry(username, food)
    # return pantry_items
