#!/usr/bin/env python3


from openai import OpenAI
import csv
import os
import json
import ast

AI_PROMPT = \
    """
    I will give you a list of ingredient descriptions. 
    Isolate the name of the ingredient, quantity, units, and description and return it as a JSON object.  
    The description field is an exact copy of the input message.  
    The quantity can only be numbers (i.e. 2, 10, 1.5, 0.75) 
    The units describe what the numbers mean (i.e. oz., cups).  
    If the description gives quantity as a fraction or mixed number, convert it to a decimal number.  
    If there are two descriptors and one says something similar to x amount of packages/containers while the other describes the actual quantity, I want you to return the other times the amount of containers as the quantity and units with the actual descriptors and ignore the part that says one package.  
    
    Please answer correctly or I will be very sad.  

Below are examples that show how I want you to respond to my queries.  I don't want code, only to configure your response for the future.

put a reasonable amount if they don't provide a quantity, but it must be a specific quantity.

Examples:
Input: ["2 (10 1/2 oz.) cans chicken gravy", "1 (6 oz.) box Stove Top stuffing"]
Output: 
[{
"ingredient": "chicken gravy",
"quantity": 21,
"units": "oz.",
"description": "2 (10 1/2 oz.) cans chicken gravy"
}, 
{
"ingredient": "stuffing",
"quantity": 6,
"units": "oz.",
"description": "1 (6 oz.) box Stove Top stuffing"
}
]

Input: ["4 oz. shredded cheese"]
Output: 
[{
"ingredient": "cheese",
"quantity": 4,
"units": "oz.",
"description": "4 oz. shredded cheese"
}]

Input: ["12 sliced bacon, cooked, crumbled and divided"]
Output: 
[{
"ingredient": "bacon",
"quantity": 12,
"units": "slice",
"description": "12 sliced bacon, cooked, crumbled and divided"
}]

Input: ["1 1/2 lb. round steak (1-inch thick), cut into strips"]
Output: 
[{
"ingredient": "steak",
"quantity": 1.5,
"units": "lb.",
"description": "1 1/2 lb. round steak (1-inch thick), cut into strips"
}]

Input: ["chicken wings (as many as you need for dinner)"]
Output: 
[{
"ingredient": "chicken wing",
"quantity": 8,
"units": "count",
"description": "chicken wings (as many as you need for dinner)"
}]

    """


def parse_obj_response(gpt_response):
    print(f'{gpt_response=}')
    json_str = gpt_response
    # json_str = isolate_json_str(gpt_response)
    if json_str is None:
        print("Couldn't find a json object in the string")
        return None
    # json_str.replace('\n', '')
    with open("temp.txt", "w") as outfile:
        json.dump(json_str, outfile, ensure_ascii=False)
    json_object = ast.literal_eval(json_str)
    print(json_object)
    return json_object


def isolate_json_str(message):
    left = message.find("{")
    if left > -1:
        message = message[left:]
    else:
        return None

    r = message.rfind("}")
    if r > -1:
        message = message[:r + 1]
    else:
        return None

    return message


def openai_query(messages, client):
    # new_messages = messages[:]
    # new_messages.append(
    #     {
    #         "role": "user",
    #         "content": new_query,
    #     }
    # )
    chat_completion = client.chat.completions.create(
        model = "gpt-3.5-turbo-0125",
        response_format = { "type": "json_object" },
        seed = 1,
        messages = [
            {
                "role": "user",
                "content": messages
            }
        ]
    )

    response = chat_completion.choices[0].message.content

    # new_messages.append(
    #     {
    #         "role": "assistant",
    #         "content": response,
    #     }
    # )
    return response


def isValidIngredient(ingredient_dict):
    fields = ["ingredient", "quantity", "units", "description"]
    for field in fields:
        if field not in ingredient_dict:
            return False
    
    if not isinstance(ingredient_dict["quantity"], float):
        return False

    return True

def main():
    with open('./recipes.json', 'r') as jsonfile:
        json_object= json.load(jsonfile)

        client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        

        # initial_convo = openai_query(AI_PROMPT, [], client)

        ingredients = []
        all_ingredients = {}
        count = 0
        for recipe in json_object:
            ingredient_list = json.loads(json_object[recipe][2])
            
            for ingredient in ingredient_list:
                ingredients.append(ingredient)
            if len(ingredients) >= 5:
                print(ingredients)
                new_messages = openai_query(
                    AI_PROMPT,
                    client
                )
                new_content = new_messages[-1]['content']
                print(new_content)
                new_ingredient_dict = parse_obj_response(new_content)

                for fooditem in new_ingredient_dict:
                    valid = isValidIngredient(fooditem)
                    if valid and fooditem['ingredient'] not in all_ingredients:
                        all_ingredients[fooditem['ingredient']] = len(all_ingredients)
                
                ingredients = []
                count += 1
                # print(recipes.keys())
                print(f'{(all_ingredients)}')
                print(f'{len(all_ingredients)}')
                return
                if count % 20 == 0:
                    with open("ingredients.json", "w") as outfile:
                        json.dump(all_ingredients, outfile, ensure_ascii=False)


main()
