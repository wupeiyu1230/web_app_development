from flask import render_template, request, session, redirect, url_for
from app.routes import main_bp
from app.models.recipe import Recipe
from app.models.saved_recipe import SavedRecipe

# --- 登入驗證 helper ---
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login_form'))
        return f(*args, **kwargs)
    return decorated_function
# -----------------------

@main_bp.route('/')
def index():
    """
    HTTP GET
    顯示首頁，列出近期或是系統推薦的食譜清單。
    """
    recipes = Recipe.get_all()[:12] # 首頁預設顯示最新 12 個
    return render_template('main/index.html', recipes=recipes)

@main_bp.route('/profile')
@login_required
def user_profile():
    """
    HTTP GET
    顯示用戶個人主頁，包含其自己建立的食譜與曾經收藏過的食譜。
    """
    user_id = session['user_id']
    
    all_recipes = Recipe.get_all()
    my_recipes = [r for r in all_recipes if r['author_id'] == user_id]
    
    saved_recipes = SavedRecipe.get_user_saved_recipes(user_id)
    
    return render_template('main/profile.html', my_recipes=my_recipes, saved_recipes=saved_recipes)
