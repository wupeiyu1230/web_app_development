from flask import render_template, request, session, redirect, url_for
from app.routes import main_bp

@main_bp.route('/')
def index():
    """
    HTTP GET
    顯示首頁，列出近期或是系統推薦的食譜清單。
    """
    pass

@main_bp.route('/profile')
def user_profile():
    """
    HTTP GET
    顯示用戶個人主頁，包含其自己建立的食譜與曾經收藏過的食譜。
    需登入才能查看。
    """
    pass
