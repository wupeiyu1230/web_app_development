from app.db import get_db_connection

class Recipe:
    @staticmethod
    def create(author_id, title, description, ingredients, steps, image_url=None, category=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO recipes 
               (author_id, title, description, ingredients, steps, image_url, category) 
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (author_id, title, description, ingredients, steps, image_url, category)
        )
        conn.commit()
        recipe_id = cursor.lastrowid
        conn.close()
        return recipe_id

    @staticmethod
    def get_by_id(recipe_id):
        conn = get_db_connection()
        recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
        conn.close()
        return recipe

    @staticmethod
    def get_all():
        conn = get_db_connection()
        recipes = conn.execute('SELECT * FROM recipes ORDER BY created_at DESC').fetchall()
        conn.close()
        return recipes

    @staticmethod
    def search_by_keyword(keyword):
        conn = get_db_connection()
        recipes = conn.execute(
            'SELECT * FROM recipes WHERE title LIKE ? OR description LIKE ?', 
            (f'%{keyword}%', f'%{keyword}%')
        ).fetchall()
        conn.close()
        return recipes

    @staticmethod
    def search_by_ingredients(ingredients_list):
        # 尋找具備特定食材組合的食譜
        conn = get_db_connection()
        query = 'SELECT * FROM recipes WHERE '
        conditions = []
        params = []
        for ingredient in ingredients_list:
            conditions.append('ingredients LIKE ?')
            params.append(f'%{ingredient}%')
            
        final_query = query + ' AND '.join(conditions)
        recipes = conn.execute(final_query, tuple(params)).fetchall()
        conn.close()
        return recipes
