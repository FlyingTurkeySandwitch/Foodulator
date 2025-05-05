from DB.DB_manager import get_connection

def get_ingredient_id_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT ingredient_id FROM Ingredients WHERE ingredient_name = ?"
    cursor.execute(query, (name,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def find_recipes_by_ingredient_id(ingredient_id):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    WITH valid_recipes AS (
        SELECT ri.recipe_id
        FROM RecipeIngredients ri
        JOIN Storage s ON ri.ingredient_id = s.ingredient_id
        WHERE s.storage_amount >= ri.amount
        GROUP BY ri.recipe_id
        HAVING COUNT(*) = (
            SELECT COUNT(*) FROM RecipeIngredients ri2 WHERE ri2.recipe_id = ri.recipe_id
        )
    ),
    recipes_with_ingredient AS (
        SELECT recipe_id
        FROM RecipeIngredients
        WHERE ingredient_id = ?
    )
    SELECT r.*
    FROM Recipes r
    WHERE r.recipe_id IN (
        SELECT recipe_id FROM valid_recipes
        INTERSECT
        SELECT recipe_id FROM recipes_with_ingredient
    );
    """

    cursor.execute(sql, (ingredient_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def find_recipes_with_tolerance(ingredient_id, tolerance):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    WITH ingredients_in_storage AS (
        SELECT ingredient_id FROM Storage WHERE storage_amount > 0
    ),
    valid_recipes AS (
        SELECT ri.recipe_id
        FROM RecipeIngredients ri
        JOIN ingredients_in_storage s ON ri.ingredient_id = s.ingredient_id
        GROUP BY ri.recipe_id
        HAVING COUNT(*) >= (
            SELECT COUNT(*) FROM RecipeIngredients ri2 WHERE ri2.recipe_id = ri.recipe_id
        ) - ?
    ),
    recipes_with_user_ingredient AS (
        SELECT recipe_id
        FROM RecipeIngredients
        WHERE ingredient_id = ?
    )
    SELECT r.*
    FROM Recipes r
    WHERE r.recipe_id IN (
        SELECT recipe_id FROM valid_recipes
        INTERSECT
        SELECT recipe_id FROM recipes_with_user_ingredient
    );
    """

    cursor.execute(sql, (tolerance, ingredient_id))
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_ingredient_amount(ingredient_id, new_amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Storage SET storage_amount = ? WHERE ingredient_id = ?",
        (new_amount, ingredient_id)
    )
    conn.commit()
    conn.close()



