from flask import render_template, request, session, redirect, url_for, flash
from app.routes import admin_bp

@admin_bp.route('/', methods=['GET'])
def admin_dashboard():
    """
    HTTP GET
    顯示後台管理員儀表板 (需具備 admin 權限)。
    """
    pass

@admin_bp.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
def admin_delete_recipe(recipe_id):
    """
    HTTP POST
    管理員強制刪除違規食譜。
    """
    pass

@admin_bp.route('/user/<int:user_id>/ban', methods=['POST'])
def admin_ban_user(user_id):
    """
    HTTP POST
    管理員強制封鎖使用者帳號。
    """
    pass
