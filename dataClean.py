
import pandas as pd
import os
from dotenv import load_dotenv
import time

#================================================================================================
import google.generativeai as genai 

load_dotenv()
API_KEY = os.getenv("API_KEY")



print("Loaded API Key:", API_KEY)  

genai.configure(api_key=API_KEY)

client = genai.GenerativeModel("gemini-2.0-flash")
#================================================================================================

def extract_first_100_rows(input_file: str,):
    df = pd.read_csv(input_file, nrows=30)
    temp = df.values.tolist()
    real = []
    model = genai.GenerativeModel("gemini-2.0-flash")
    count = 0
    for i in range(len(temp)):
        if count == 15:
            print("Sleeping for 60 seconds")
            time.sleep(60)
            print("Resuming")
            count = 0
        unCleanedPrompt = ["Given two lists L1 and L2 in the form L1,L2. L1 contains common names of ingredients and L2 contains ingredient names and amounts. Please standardize the list of ingredients in L2 into this format: [[ingredient1, amount], [ingredient2, amount], ...]. The ingredient names should be from L1 the and ingredient amount should be in grams in a floatig point format. your response should only be the list of ingredients in that format. Do not include any other text or explanation.  The output should be an arrays with the format [[ingredient1, amount], [ingredient2, amount], ...]. Please do not include any other text or explanation or code in your response.",  
     [temp[i][1],temp[i][2]]]
        
        response = model.generate_content( str(unCleanedPrompt))
        response = response.text.replace('\n', '').replace('json', '').replace(' ', '').replace('```', '')
        temp2 = [temp[i][0],response,temp[i][3], temp[i][5]]
        real.append(temp2) 
        count += 1
    return real

#print(extract_first_100_rows("recipes_data.csv"))

#================================================================================================

def extract_recipes_from_csv(csv_path: str, max_rows):
    df = pd.read_csv(csv_path, nrows=max_rows)

    #['title', 'ingredients', 'directions', 'link', 'NER']
    recipes = []
    for _, row in df.iterrows():
        recipe = [
            row['title'],
            row['ingredients'],
            row['directions'],
            row['link'],
            row['NER']
        ]
        recipes.append(recipe)

    return recipes

print(extract_recipes_from_csv("recipes_data.csv", 10))
#================================================================================================
# testUncleanedPrompt ='Given the following two lists, standardize the two list into one using the words from the second list. Follow this format: [[ingredient1, amount], [ingredient2, amount], …]. The amounts should be floating point values in grams. DO NOT include any other text or explanation or code in your response.'
# # NER,Ingredients

# #Cheeseburger Potato Soup
# unCleanedIngredients1 = "[""sour cream"", ""bacon"", ""pepper"", ""extra lean ground beef"", ""cheddar cheese"", ""green onion"", ""baking potatoes"", ""milk"", ""butter"", ""salt""],[""6 baking potatoes"", ""1 lb. of extra lean ground beef"", ""2/3 c. butter or margarine"", ""6 c. milk"", ""3/4 tsp. salt"", ""1/2 tsp. pepper"", ""1 1/2 c (6 oz.) shredded Cheddar cheese, divided"", ""12 sliced bacon, cooked, crumbled and divided"", ""4 green onion, chopped and divided"", ""1 (8 oz.) carton sour cream (optional)""]"

# # Reeses Cups(Candy)  
# unCleanedIngredients2 = "[“”graham cracker crumbs"", ""powdered sugar"", ""peanut butter"", ""chocolate chips"", ""butter””],[“”1 c. peanut butter"", ""3/4 c. graham cracker crumbs"", ""1 c. melted butter"", ""1 lb. (3 1/2 c.) powdered sugar"", ""1 large pkg. chocolate chips""]"

# # Rhubarb Coffee Cake
# unCleanedIngredients3 = "[""buttermilk"", ""egg"", ""sugar"", ""vanilla"", ""soda"", ""flour"", ""rhubarb"", ""butter"", ""salt""],[""1 1/2 c. sugar"", ""1/2 c. butter"", ""1 egg"", ""1 c. buttermilk"", ""2 c. flour"", ""1/2 tsp. salt"", ""1 tsp. soda"", ""1 c. buttermilk"", ""2 c. rhubarb, finely cut"", ""1 tsp. vanilla""]"
# cleaningPrompt = testUncleanedPrompt + unCleanedIngredients1



#================================================================================================
# print("START")
# model = genai.GenerativeModel("gemini-2.0-flash")  
# response = model.generate_content(cleaningPrompt)  
# print(response.text.strip(' `\n'))
# #print(response.text)
# print("END")

