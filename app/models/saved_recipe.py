import sqlite3
from app.db import get_db_connection

class SavedRecipe:
    """操作 saved_recipes 資料表的模型"""

    @staticmethod
    def save(user_id, recipe_id):
        """新增一筆食譜收藏記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO saved_recipes (user_id, recipe_id) VALUES (?, ?)',
                (user_id, recipe_id)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("IntegrityError: This recipe is already saved or user/recipe does not exist.")
            return False
        except Exception as e:
            print(f"Database error in SavedRecipe.save: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def unsave(user_id, recipe_id):
        """刪除（移除）收藏記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM saved_recipes WHERE user_id = ? AND recipe_id = ?',
                (user_id, recipe_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Database error in SavedRecipe.unsave: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_user_saved_recipes(user_id):
        """取得特定使用者的所有收藏記錄"""
        try:
            conn = get_db_connection()
            recipes = conn.execute(
                '''SELECT r.*, s.saved_at 
                   FROM recipes r
                   JOIN saved_recipes s ON r.id = s.recipe_id
                   WHERE s.user_id = ?
                   ORDER BY s.saved_at DESC''',
                (user_id,)
            ).fetchall()
            return recipes
        except Exception as e:
            print(f"Database error in SavedRecipe.get_user_saved_recipes: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()
