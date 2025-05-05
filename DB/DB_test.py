# from DB_manager import get_connection
# from queries import find_recipes_all_match

# conn = get_connection()
# if conn:
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM Recipies")
#     print(cursor.fetchall())
#     conn.close()
# else:
#     print("ERROR DB_test.py: No connection to the database.")
#=======================================================================================================================
#PRINT ALL TABLES

# conn = get_connection()
# cursor = conn.cursor()
# with open('DB/initialDB.sql', 'r') as f:
#     script = f.read()
#     cursor.executescript(script)
    
# conn.commit()

# cursor.execute("SELECT * FROM Recipes")
# rows = cursor.fetchall()
# print("\nRecipes:\n")
# for row in rows:
#     print(row)

# cursor.execute("SELECT * FROM Ingredients")
# rows = cursor.fetchall()
# print("\nIngredients:\n")
# for row in rows:
#     print(row)

# cursor.execute("SELECT * FROM RecipeIngredients")
# rows = cursor.fetchall()
# print("\nRecipeIngredients:\n")
# for row in rows:
#     print(row)

# cursor.execute("SELECT * FROM Storage")
# rows = cursor.fetchall()
# print("\nStorage:\n")
# for row in rows:
#     print(row)

# conn.close()
#=======================================================================================================================
from .DB_manager import get_connection
from .queries import find_recipes_by_ingredient_id, get_ingredient_id_by_name, find_recipes_with_tolerance


with get_connection() as conn:
    cursor = conn.cursor()
    with open('DB/initialDB.sql', 'r') as f:
        script = f.read()
    cursor.executescript(script)
    conn.commit()

# Define ingredient IDs you want to test with (adjust to match your data)
# For example: ['baking potatoes', 'ground beef', 'milk']
in_name = 'graham cracker crumbs'
print(f"\n[INFO] User ingredient name: {in_name}")

user_ingredient_ids = get_ingredient_id_by_name(in_name)  # You must know or look these up in Ingredients
print(user_ingredient_ids)

#recipes = find_recipes_by_ingredient_id(user_ingredient_ids)

recipeT = find_recipes_with_tolerance(user_ingredient_ids, 1)

# print("\n[INFO] Recipes that match all user ingredients and are fully in storage:")
# for row in recipes:
#     print(row)
print("\n[INFO] Recipes that match all user ingredients and are fully in storage:")
for row in recipeT:
    print(row)
