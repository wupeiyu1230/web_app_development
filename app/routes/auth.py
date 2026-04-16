import bcrypt
from flask import render_template, request, session, redirect, url_for, flash
from app.routes import auth_bp
from app.models.user import User

@auth_bp.route('/register', methods=['GET'])
def register_form():
    """顯示註冊表單頁面"""
    return render_template('auth/register.html')

@auth_bp.route('/register', methods=['POST'])
def register_submit():
    """接收表單資料，建立新使用者帳號並寫入 DB"""
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    if not username or not email or not password:
        flash("請填寫所有欄位！", "danger")
        return redirect(url_for('auth.register_form'))

    # 加密密碼
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    user_id = User.create(username, email, password_hash)
    if user_id:
        flash("註冊成功，請登入！", "success")
        return redirect(url_for('auth.login_form'))
    else:
        flash("註冊失敗，信箱或使用者名稱可能已被註冊。", "danger")
        return redirect(url_for('auth.register_form'))

@auth_bp.route('/login', methods=['GET'])
def login_form():
    """顯示登入表單頁面"""
    return render_template('auth/login.html')

@auth_bp.route('/login', methods=['POST'])
def login_submit():
    """檢驗會員帳號密碼，驗證成功後寫入 session"""
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    user = User.get_by_email(email)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        flash(f"登入成功！歡迎回來，{user['username']}", "success")
        return redirect(url_for('main.index'))
    else:
        flash("登入失敗，信箱或密碼錯誤。", "danger")
        return redirect(url_for('auth.login_form'))

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """清除 session 表明登出狀態"""
    session.clear()
    flash("您已登出。", "info")
    return redirect(url_for('main.index'))
