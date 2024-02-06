## Progress 
* Created 14 end points using flask
* Developed endpoints for user registry/login authentication
* Used an OCR to convert images of receipts to text
* Started to choose recipes from a recipe database using chatgpt to populate our database with
* API Endpoints
    * GET: '/users' (Returns list of all users)
    * POST: '/users' (Registers new user into system)
    * GET '/users/{username}' (Gets single user's information)
    * DELETE '/users/{username}' (Delete's user's account)
    * PATCH '/users/refresh' (Generates new access token using refresh token for user's session)
    * PATCH '/users/login' (Logs in a user)
    * PATCH '/users/logout' (Logs out a user)
    * GET '/users/{username}/pantry' (returns a user's pantry info)
    * PATCH '/users/{username}/pantry' (modify user's pantry item)
    * GET '/users/{username}/recipe' (get user's saved recipes)
    * PATCH '/users/{username}/recipe' (add recipes to saved recipes)
    * DELETE '/users/{username}/recipe' (delete recipe)

## Goals
* MVP: Meal Prep app with dynamically updating pantry
* Create more service based endpoints
* Provide Auto Generated Shopping Lists based off of desired recipes
    Expect to do this by storing a 'shopping list' per user with recipes and ingredients
* Integrate OCR model to pantry maintanence
* Use Instacart Recipe Generation to allow users to build carts
    * See if can use instacart's custom create recipe HTML button for web pages 
* Make a functional and aesthetically pleasing User Interface for our app
    * Fulfills React goal for semester
    * Have various carousels of recipe suggestions ie (user's favorites, aligned with pantry, random)
* Write proper documentation for code functionality
* Finish our MVP by the end of this semester