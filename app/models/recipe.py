import sqlite3
from app.db import get_db_connection

class Recipe:
    """操作 recipes 資料表的模型"""

    @staticmethod
    def create(author_id, title, description, ingredients, steps, image_url=None, category=None):
        """新增一筆食譜記錄"""
        try:
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
            return recipe_id
        except Exception as e:
            print(f"Database error in Recipe.create: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_id(recipe_id):
        """根據 ID 取得單筆食譜記錄"""
        try:
            conn = get_db_connection()
            recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
            return recipe
        except Exception as e:
            print(f"Database error in Recipe.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_all():
        """取得所有食譜記錄（依照建立時間降冪）"""
        try:
            conn = get_db_connection()
            recipes = conn.execute('SELECT * FROM recipes ORDER BY created_at DESC').fetchall()
            return recipes
        except Exception as e:
            print(f"Database error in Recipe.get_all: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update(recipe_id, data):
        """更新食譜記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # 手動更新 updated_at
            data['updated_at'] = 'CURRENT_TIMESTAMP'
            
            set_clause = []
            values = []
            for key, val in data.items():
                if val == 'CURRENT_TIMESTAMP':
                    set_clause.append(f"{key} = CURRENT_TIMESTAMP")
                else:
                    set_clause.append(f"{key} = ?")
                    values.append(val)
                    
            values.append(recipe_id)

            cursor.execute(
                f'UPDATE recipes SET {", ".join(set_clause)} WHERE id = ?',
                tuple(values)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Database error in Recipe.update: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def delete(recipe_id):
        """刪除食譜記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Database error in Recipe.delete: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def search_by_keyword(keyword):
        """依據標題或敘述模糊搜尋食譜"""
        try:
            conn = get_db_connection()
            recipes = conn.execute(
                'SELECT * FROM recipes WHERE title LIKE ? OR description LIKE ?', 
                (f'%{keyword}%', f'%{keyword}%')
            ).fetchall()
            return recipes
        except Exception as e:
            print(f"Database error in Recipe.search_by_keyword: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def search_by_ingredients(ingredients_list):
        """依據傳入的食材陣列，尋找具備特定食材組合的食譜"""
        try:
            conn = get_db_connection()
            query = 'SELECT * FROM recipes WHERE '
            conditions = []
            params = []
            for ingredient in ingredients_list:
                conditions.append('ingredients LIKE ?')
                params.append(f'%{ingredient}%')
                
            final_query = query + ' AND '.join(conditions)
            recipes = conn.execute(final_query, tuple(params)).fetchall()
            return recipes
        except Exception as e:
            print(f"Database error in Recipe.search_by_ingredients: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()
