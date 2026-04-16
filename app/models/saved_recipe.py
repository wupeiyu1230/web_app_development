import sqlite3
from app.db import get_db_connection

class SavedRecipe:
    @staticmethod
    def save(user_id, recipe_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO saved_recipes (user_id, recipe_id) VALUES (?, ?)',
                (user_id, recipe_id)
            )
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            # 發生錯誤表示可能已經收藏過了
            success = False
        conn.close()
        return success

    @staticmethod
    def unsave(user_id, recipe_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM saved_recipes WHERE user_id = ? AND recipe_id = ?',
            (user_id, recipe_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_user_saved_recipes(user_id):
        conn = get_db_connection()
        recipes = conn.execute(
            '''SELECT r.*, s.saved_at 
               FROM recipes r
               JOIN saved_recipes s ON r.id = s.recipe_id
               WHERE s.user_id = ?
               ORDER BY s.saved_at DESC''',
            (user_id,)
        ).fetchall()
        conn.close()
        return recipes
