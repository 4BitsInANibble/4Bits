#!/usr/bin/env python3


from openai import OpenAI
import csv
import os
import json
import ast

SEED_CONSTANT = 1 #this can be any value, the constant allows the model to be more deterministic

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

    Here is an example of how the input should be evaluted and how the output should be structured:
        Input: 
            2 (10 1/2 oz.) cans chicken gravy
            1 (6 oz.) box Stove Top stuffing
        Output:
        {
            "ingredients": [
                {
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
        }
            

    Please take my input and return an output JSON object with the ingredient name, quantity, units, and description.
    Here is my input:

 """


def parse_obj_response(gpt_response):
    # print(f'{gpt_response=}', gpt_response)
    json_str = gpt_response
    # json_str = isolate_json_str(gpt_response)
    if json_str is None:
        print("Couldn't find a json object in the string")
        return None
    # json_str.replace('\n', '')
    # with open("temp.json", "w") as outfile:
    #     json.dump(json_str, outfile, ensure_ascii=False)
    json_object = ast.literal_eval(json_str)
    # print(json_object, "\n")
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
        seed = SEED_CONSTANT,
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


def isValidIngredient(ingredient_dict): #pick up debugging from here
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
            # print("loaded ingredient list:", ingredient_list)

            ingredient_list_str = ""
            for ingredient in ingredient_list:
                # print("ingredient: ", ingredient)
                # ingredients.append(ingredient)
                ingredient_list_str = ingredient_list_str + ingredient + "\n"
            
            print("ingredient list: \n", ingredient_list_str)

            if len(ingredient_list_str) >= 5:
                message_string = AI_PROMPT + ingredient_list_str
                json_resp_obj = openai_query(
                    message_string,
                    client
                )
                
                print("query response: \n", json_resp_obj)
                # json_resp_obj = json_resp_obj + ","
                with open("query_response.json", "a") as outfile:
                    # json.dump(json_resp_obj, outfile, ensure_ascii=True)
                    outfile.write(json_resp_obj)
                
                new_ingredient_dict = parse_obj_response(json_resp_obj)
                print("ingredient dictionary: \n", new_ingredient_dict)

                for fooditem in new_ingredient_dict['ingredients']:
                    print("fooditem: ", fooditem)
                    valid = isValidIngredient(fooditem)
                    if valid and fooditem['ingredient'] not in all_ingredients:
                        all_ingredients[fooditem['ingredient']] = len(all_ingredients)

                # print("after for loop")
                
                ingredients = []
                count += 1
                # print(recipes.keys())
                # print(f'{(all_ingredients)}')
                # print(f'{len(all_ingredients)}')
                # return
                if count % 20 == 0:
                    with open("ingredients.json", "w") as outfile:
                        json.dump(all_ingredients, outfile, ensure_ascii=False)

main()