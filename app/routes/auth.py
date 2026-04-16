from flask import render_template, request, session, redirect, url_for, flash
from app.routes import auth_bp

@auth_bp.route('/register', methods=['GET'])
def register_form():
    """
    HTTP GET
    顯示註冊表單頁面。
    """
    pass

@auth_bp.route('/register', methods=['POST'])
def register_submit():
    """
    HTTP POST
    接收表單資料，建立新使用者帳號並寫入 DB。
    """
    pass

@auth_bp.route('/login', methods=['GET'])
def login_form():
    """
    HTTP GET
    顯示登入表單頁面。
    """
    pass

@auth_bp.route('/login', methods=['POST'])
def login_submit():
    """
    HTTP POST
    檢驗會員帳號密碼，驗證成功後寫入 session。
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    HTTP GET
    清除 session 表明登出狀態，並重導向至首頁。
    """
    pass
