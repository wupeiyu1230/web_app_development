from flask import render_template, request, session, redirect, url_for, flash
from app.routes import recipes_bp
from app.models.recipe import Recipe
from app.models.saved_recipe import SavedRecipe

# --- 登入驗證 Helper ---
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("請先登入即可繼續操作", "warning")
            return redirect(url_for('auth.login_form'))
        return f(*args, **kwargs)
    return decorated_function
# ----------------------

@recipes_bp.route('/search', methods=['GET'])
def search_recipes():
    """進行一般關鍵字搜尋食譜"""
    keyword = request.args.get('q', '').strip()
    if keyword:
        recipes = Recipe.search_by_keyword(keyword)
    else:
        recipes = Recipe.get_all()
    return render_template('recipes/search_results.html', recipes=recipes, keyword=keyword)

@recipes_bp.route('/search_by_ingredients', methods=['GET'])
def search_by_ingredients():
    """進行多食材組合搜尋"""
    ingredients_str = request.args.get('ingredients', '').strip()
    if ingredients_str:
        # 將食材字串轉換成陣列（根據全形或半形逗號切割）
        ingredients_list = [i.strip() for i in ingredients_str.replace('，', ',').split(',')]
        ingredients_list = [i for i in ingredients_list if i] # 移除空字串
        recipes = Recipe.search_by_ingredients(ingredients_list)
    else:
        recipes = Recipe.get_all()
    return render_template('recipes/search_results.html', recipes=recipes, ingredients=ingredients_str)

@recipes_bp.route('/<int:recipe_id>', methods=['GET'])
def view_recipe(recipe_id):
    """根據食譜 ID，顯示單筆食譜詳細內容"""
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        flash("找不到此食譜", "danger")
        return redirect(url_for('main.index'))
    return render_template('recipes/view.html', recipe=recipe)

@recipes_bp.route('/create', methods=['GET'])
@login_required
def create_recipe_form():
    """顯示建立新食譜的表單頁面"""
    return render_template('recipes/create.html')

@recipes_bp.route('/create', methods=['POST'])
@login_required
def create_recipe_submit():
    """接收建立食譜的表單資料並儲存至資料庫"""
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    ingredients = request.form.get('ingredients', '').strip()
    steps = request.form.get('steps', '').strip()
    category = request.form.get('category', '').strip()
    image_url = request.form.get('image_url', '').strip()

    if not title or not ingredients or not steps:
        flash("標題、食材與步驟為必填欄位", "danger")
        return redirect(url_for('recipes.create_recipe_form'))

    recipe_id = Recipe.create(
        author_id=session['user_id'],
        title=title,
        description=description,
        ingredients=ingredients,
        steps=steps,
        image_url=image_url if image_url else None,
        category=category if category else None
    )

    if recipe_id:
        flash("食譜新增成功！", "success")
        return redirect(url_for('recipes.view_recipe', recipe_id=recipe_id))
    else:
        flash("新增失敗，發生資料庫錯誤", "danger")
        return redirect(url_for('recipes.create_recipe_form'))

@recipes_bp.route('/<int:recipe_id>/edit', methods=['GET'])
@login_required
def edit_recipe_form(recipe_id):
    """顯示編輯食譜的表單頁面"""
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        flash("找不到該食譜", "danger")
        return redirect(url_for('main.index'))
    
    # 權限檢查
    if recipe['author_id'] != session['user_id']:
        flash("您沒有權限編輯此食譜", "danger")
        return redirect(url_for('recipes.view_recipe', recipe_id=recipe_id))
        
    return render_template('recipes/edit.html', recipe=recipe)

@recipes_bp.route('/<int:recipe_id>/edit', methods=['POST'])
@login_required
def edit_recipe_submit(recipe_id):
    """接收編輯食譜的修改內容並更新"""
    recipe = Recipe.get_by_id(recipe_id)
    if recipe['author_id'] != session['user_id']:
        flash("您沒有權限編輯此食譜", "danger")
        return redirect(url_for('recipes.view_recipe', recipe_id=recipe_id))

    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    ingredients = request.form.get('ingredients', '').strip()
    steps = request.form.get('steps', '').strip()
    category = request.form.get('category', '').strip()
    image_url = request.form.get('image_url', '').strip()

    if not title or not ingredients or not steps:
        flash("標題、食材與步驟為必填欄位", "danger")
        return redirect(url_for('recipes.edit_recipe_form', recipe_id=recipe_id))

    data = {
        'title': title,
        'description': description,
        'ingredients': ingredients,
        'steps': steps,
        'category': category if category else None,
        'image_url': image_url if image_url else None
    }
    
    result = Recipe.update(recipe_id, data)
    if result:
        flash("食譜更新成功！", "success")
    else:
        flash("食譜更新失敗", "danger")
        
    return redirect(url_for('recipes.view_recipe', recipe_id=recipe_id))

@recipes_bp.route('/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    """刪除特定食譜"""
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        flash("食譜不存在", "danger")
        return redirect(url_for('main.index'))
        
    if recipe['author_id'] != session['user_id']:
        flash("您沒有權限刪除此食譜", "danger")
        return redirect(url_for('recipes.view_recipe', recipe_id=recipe_id))

    if Recipe.delete(recipe_id):
        flash("食譜已刪除", "success")
    else:
        flash("刪除失敗", "danger")
        
    return redirect(url_for('main.index'))

@recipes_bp.route('/<int:recipe_id>/save', methods=['POST'])
@login_required
def save_recipe(recipe_id):
    """將特定食譜加入收藏清單"""
    if SavedRecipe.save(session['user_id'], recipe_id):
        flash("已加入收藏！", "success")
    else:
        flash("您已收藏過此食譜或發生錯誤", "warning")
    return redirect(url_for('recipes.view_recipe', recipe_id=recipe_id))

@recipes_bp.route('/<int:recipe_id>/unsave', methods=['POST'])
@login_required
def unsave_recipe(recipe_id):
    """將特定食譜從收藏清單移除"""
    if SavedRecipe.unsave(session['user_id'], recipe_id):
        flash("已從收藏移除！", "info")
    else:
        flash("移除失敗", "danger")
    # request.referrer 返回使用者上一頁網址，如果是書籤則返回 profile
    return redirect(request.referrer or url_for('main.user_profile'))
