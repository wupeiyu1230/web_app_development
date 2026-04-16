from flask import render_template, request, session, redirect, url_for, flash
from app.routes import admin_bp
from app.models.recipe import Recipe
from app.models.user import User

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash("權限不足", "danger")
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/', methods=['GET'])
@admin_required
def admin_dashboard():
    """顯示後台管理員儀表板 (需具備 admin 權限)"""
    recipes = Recipe.get_all()
    users = User.get_all()
    return render_template('admin/dashboard.html', recipes=recipes, users=users)

@admin_bp.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@admin_required
def admin_delete_recipe(recipe_id):
    """管理員強制刪除違規食譜"""
    if Recipe.delete(recipe_id):
        flash("食譜已強制刪除", "success")
    else:
        flash("食譜刪除失敗", "danger")
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/user/<int:user_id>/ban', methods=['POST'])
@admin_required
def admin_ban_user(user_id):
    """管理員強制封鎖/刪除使用者帳號"""
    if User.delete(user_id):
        flash("帳號已封鎖/刪除", "success")
    else:
        flash("帳號封鎖/刪除失敗", "danger")
    return redirect(url_for('admin.admin_dashboard'))
