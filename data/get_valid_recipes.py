from openai import OpenAI
import csv
import os
import json
import ast

AI_PROMPT = \
    """
    You are a intelligent assistant.  
    I will give you an array of dishes, and return an json object of either 'yes', 'no' for whether this dish is an entree with a key of the dish name.  
    If it is unknown, use 'no'.  
    Please be very strict about classifying a dish as an entree and the formatting.
    I will be very sad if there is something wrong and I don't know how I would cope with wrongly categorized dishes and formatted responses.
    Do not give any explanation in your output, no context, I only want a JSON object that I can parse.
    The following is an example of an input and an output
    
    Input:
    ['Banana Cream Pie', 'Steak Frites', 'Strawberry Jam']
    
    Output:
    {
        'Banana Cream Pie': 'yes',
        'Steak Frites': 'no',
        'Strawberry Jam': 'no'
    }
    """

def parse_obj_response(gpt_response):
    json_str = isolate_json_str(gpt_response)
    if json_str is None:
        print("Couldn't find a json object in the string")
        return None
    print(json_str)
    json_object = ast.literal_eval(json_str)
    return json_object


def isolate_json_str(message):
    l = message.find("{")
    if l > -1:
        message = message[l:]
    else:
        return None
    
    r = message.rfind("}")
    if r > -1:
        message = message[:r + 1]
    else:
        return None
    
    return message

def openai_query(new_query, messages, client):
    new_messages = messages[:]
    new_messages.append(
        {
            "role": "user",
            "content": new_query,
        }
    )
    chat_completion = client.chat.completions.create(
        messages=new_messages,
        model="gpt-3.5-turbo",
    )
    
    response = chat_completion.choices[0].message.content

    new_messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )
    return new_messages


def main():
    with open('../../Downloads/dataset/dataset/full_dataset.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)

        client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

        initial_convo = openai_query(AI_PROMPT, [], client)

        rows = []
        recipes = {}
        count = 0
        for row in csvreader:

            rows.append(row)
            if len(rows) == 50:
                new_recipe_dict = None
                new_recipes = [r[1] for r in rows] 
                new_messages = openai_query(str(new_recipes), initial_convo, client)
                # print(new_messages[-1]['content'])
                new_recipe_dict = parse_obj_response(new_messages[-1]['content'])

                for recipe in rows:
                    if recipe[1] in new_recipe_dict and new_recipe_dict[recipe[1]].lower() == "yes":
                        recipes[recipe[1]] = recipe
                rows = []
                count += 1
                # print(recipes.keys())
                print(f'{len(recipes)}/{count*50}')
                if len(recipes) >= 5100:
                    break
        
                if count % 20 == 0:
                    with open("recipes.json", "w") as outfile:
                        json.dump(recipes, outfile, ensure_ascii=False)
        

main()