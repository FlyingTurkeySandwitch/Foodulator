DROP TABLE IF EXISTS Storage;
DROP TABLE IF EXISTS RecipeIngredients;
DROP TABLE IF EXISTS Recipes;
DROP TABLE IF EXISTS Ingredients;


CREATE TABLE Recipes (
    recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_name TEXT NOT NULL,
    recipe_directions TEXT,
    recipe_link TEXT,
    recipe_NER TEXT
);

CREATE TABLE Ingredients (
    ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_name TEXT NOT NULL UNIQUE
);

CREATE TABLE RecipeIngredients (
    recipe_id INTEGER,
    ingredient_id INTEGER,
    amount REAL NOT NULL,
    PRIMARY KEY (recipe_id, ingredient_id),
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id),
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id)
);

CREATE TABLE Storage (
    ingredient_id INTEGER PRIMARY KEY,
    storage_amount REAL NOT NULL,
    storage_location TEXT CHECK(storage_location IN ('fridge', 'freezer', 'pantry')),
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id)
);

-- test data

INSERT INTO Recipes ( recipe_name, recipe_directions, recipe_link, recipe_NER ) VALUES
('Cheeseburger Potato Soup',

"[""Wash potatoes; prick several times with a fork."", ""Microwave them with a wet paper towel covering the potatoes on high for 6-8 minutes."", ""The potatoes should be soft, ready to eat."", ""Let them cool enough to handle."", ""Cut in half lengthwise; scoop out pulp and reserve."", ""Discard shells."", ""Brown ground beef until done."", ""Drain any grease from the meat."",""Set aside when done."", ""Meat will be added later."", ""Melt butter in a large kettle over low heat; add flour, stirring until smooth."",""Cook 1 minute, stirring constantly. Gradually add milk; cook over medium heat, stirring constantly, until thickened and bubbly."", ""Stir in potato, ground beef, salt, pepper, 1 cup of cheese, 2 tablespoons of green onion and 1/2 cup of bacon."",""Cook until heated (do not boil)."", ""Stir in sour cream if desired; cook until heated (do not boil)."", ""Sprinkle with remaining cheese, bacon and green onions.""]",

'www.cookbooks.com/Recipe-Details.aspx?id=20115',

'[""sour cream"", ""bacon"", ""pepper"", ""extra lean ground beef"", ""cheddar cheese"", ""green onion"", ""baking potatoes"", ""milk"", ""butter"", ""salt""]'
),

('Rhubarb Coffee Cake',

"[""Cream sugar and butter."", ""Add egg and beat well."", ""To creamed butter, sugar and egg, add alternately buttermilk with mixture of flour, salt and soda."", ""Mix well."", ""Add rhubarb and vanilla."", ""Pour into greased 9 x 13-inch pan and add Topping.""]",

'www.cookbooks.com/Recipe-Details.aspx?id=210288',

"[""buttermilk"", ""egg"", ""sugar"", ""vanilla"", ""soda"", ""flour"", ""rhubarb"", ""butter"", ""salt""]"
),

('Reeses Cups(Candy)',

"[""Combine first four ingredients and press in 13 x 9-inch ungreased pan."", ""Melt chocolate chips and spread over mixture. Refrigerate for about 20 minutes and cut into pieces before chocolate gets hard."", ""Keep in refrigerator.""]",

'www.cookbooks.com/Recipe-Details.aspx?id=659239',

"[""graham cracker crumbs"", ""powdered sugar"", ""peanut butter"", ""chocolate chips"", ""butter""]"
);

INSERT INTO Ingredients (ingredient_name ) VALUES
('graham cracker crumbs'),
('powdered sugar'),
('peanut butter'),
('chocolate chips'),
('butter'),
('sour cream'),
('bacon'),
('pepper'),
('ground beef'),
('cheddar cheese'),
('green onion'),
('baking potatoes'),
('milk'),
('salt'),
('buttermilk'),
('egg'),
('sugar'),
('vanilla'),
('soda'),
('flour'),
('rhubarb');




INSERT INTO RecipeIngredients ( recipe_id, ingredient_id, amount ) VALUES
--"[[baking potato, 900], [ground beef, 454], [butter, 151], [milk, 1440], [salt, 4], [black pepper, 1], [cheddar cheese, 170], [bacon, 340], [green onion, 50], [sour cream, 227]]"
(1, 12,900),
(1, 9,454),
(1, 5,151),
(1, 13,1440),
(1, 14,4),
(1, 8,1),
(1, 10,170),
(1, 7,340),
(1, 11,50),
(1, 6,227),
--"[['buttermilk', 480.0], ['egg', 50.0], ['sugar', 300.0], ['vanilla', 4.0], ['soda', 4.0], ['flour', 250.0], ['rhubarb', 120.0], ['butter', 113.0], ['salt', 3.0]]"
(2, 15,480),
(2, 16,50),
(2, 17,300),
(2, 18,4),
(2,19 ,4),
(2,20 ,250),
(2, 21,120),
(2, 5,113),
(2, 14,3),
--[["graham cracker crumbs", 85.26], ["powdered sugar", 454], ["peanut butter", 256], ["chocolate chips", 340], ["butter", 226.8]]"
(3, 1,85),
(3, 2,454),
(3, 3,256),
(3, 4,340),
(3, 5,227);




INSERT INTO Storage ( ingredient_id, storage_amount, storage_location ) VALUES
(1, 10000, 'fridge'),
(2, 10000, 'fridge'),
(3, 10000, 'fridge'),
(4, 10000, 'fridge'),
(5, 10000, 'fridge'),
(6, 10000, 'fridge'),
(7, 10000, 'fridge'),
(8, 10000, 'fridge'),
(9, 10000, 'fridge'),
(10, 10000, 'fridge'),
(11, 10000, 'fridge'),
(12, 10000, 'fridge'),
(13, 10000, 'fridge'),
(14, 10000, 'fridge'),
(15, 10000, 'fridge'),
(16, 10000, 'fridge'),
(17, 10000, 'fridge'),
(18, 10000, 'fridge'),
(19, 10000, 'fridge'),
(20, 10000, 'fridge'),
(21, 10000, 'fridge');