Recipe - Food - Nutrition
- can save recipes, track food, identify/collect food products
- 365000 recipes
- 86000 food product

api-ninjas
- 200000 recipes
- recipes from variious cuisines

random recipes 
- randomly generates with title, image, link
- could be good for a "surprise me" feature?

zestful recipe and ingredient analysis
- input is plain text string ("x tbspns ground cumin") and output is quantity, unit, food product, prep steps
- super helpful for parsing ingredients from recipe to the db

recipe generator api
- generates recipe based on ist of ingredients
- takes as a comma separates string, uses a ai model
- max 20 ingredients, string <200 char long

recipe database
- https://openrecip.es/
- https://github.com/fictivekin/openrecipes
- NoSQL database with name, ingredients, url, cookTime, recipeYield, datePublished, prepTime, description fields
- does not actually contain recipe, have to scrape website of `url` for recipe
- 