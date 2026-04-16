from flask import render_template, request, session, redirect, url_for, flash
from app.routes import recipes_bp

@recipes_bp.route('/search', methods=['GET'])
def search_recipes():
    """
    HTTP GET
    接收 q 查詢參數，進行一般關鍵字搜尋食譜。
    """
    pass

@recipes_bp.route('/search_by_ingredients', methods=['GET'])
def search_by_ingredients():
    """
    HTTP GET
    接收 ingredients 查詢參數，進行多食材組合搜尋。
    """
    pass

@recipes_bp.route('/<int:recipe_id>', methods=['GET'])
def view_recipe(recipe_id):
    """
    HTTP GET
    根據食譜 ID，顯示單筆食譜詳細內容。
    """
    pass

@recipes_bp.route('/create', methods=['GET'])
def create_recipe_form():
    """
    HTTP GET
    顯示建立新食譜的表單頁面 (需登入)。
    """
    pass

@recipes_bp.route('/create', methods=['POST'])
def create_recipe_submit():
    """
    HTTP POST
    接收建立食譜的表單資料並儲存至資料庫。
    """
    pass

@recipes_bp.route('/<int:recipe_id>/edit', methods=['GET'])
def edit_recipe_form(recipe_id):
    """
    HTTP GET
    顯示編輯食譜的表單頁面，需確認為作者本人。
    """
    pass

@recipes_bp.route('/<int:recipe_id>/edit', methods=['POST'])
def edit_recipe_submit(recipe_id):
    """
    HTTP POST
    接收編輯食譜的修改內容並更新。
    """
    pass

@recipes_bp.route('/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """
    HTTP POST
    刪除特定食譜，需確認為作者本人。
    """
    pass

@recipes_bp.route('/<int:recipe_id>/save', methods=['POST'])
def save_recipe(recipe_id):
    """
    HTTP POST
    將指定食譜加入目前登入用戶的收藏清單。
    """
    pass

@recipes_bp.route('/<int:recipe_id>/unsave', methods=['POST'])
def unsave_recipe(recipe_id):
    """
    HTTP POST
    將指定食譜從目前登入用戶的收藏清單移除。
    """
    pass
