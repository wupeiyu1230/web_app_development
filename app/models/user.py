import sqlite3
from app.db import get_db_connection

class User:
    """操作 users 資料表的模型"""

    @staticmethod
    def create(username, email, password_hash, role='user'):
        """新增一筆使用者記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)',
                (username, email, password_hash, role)
            )
            conn.commit()
            user_id = cursor.lastrowid
            return user_id
        except sqlite3.IntegrityError as e:
            # 處理 username 或 email 重複的問題
            print(f"User creation failed (IntegrityError): {e}")
            return None
        except Exception as e:
            print(f"Database error in User.create: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_id(user_id):
        """根據 ID 取得單筆使用者"""
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            return user
        except Exception as e:
            print(f"Database error in User.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_email(email):
        """根據 email 取得使用者（用於登入驗證）"""
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            return user
        except Exception as e:
            print(f"Database error in User.get_by_email: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_all():
        """取得所有使用者記錄"""
        try:
            conn = get_db_connection()
            users = conn.execute('SELECT * FROM users').fetchall()
            return users
        except Exception as e:
            print(f"Database error in User.get_all: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update(user_id, data):
        """更新使用者記錄 (例如更新 role)"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # 依據傳入的 dict 組合成參數與欄位
            set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
            values = list(data.values())
            values.append(user_id)

            cursor.execute(
                f'UPDATE users SET {set_clause} WHERE id = ?',
                tuple(values)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Database error in User.update: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def delete(user_id):
        """刪除一筆使用者記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Database error in User.delete: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
