# 路由設計文件 (ROUTES.md)

根據系統流程圖與架構設計，本系統主要使用 Flask Blueprint 將路由切分為四大模組：`main_bp`, `auth_bp`, `recipes_bp`, `admin_bp`。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應 Blueprint | 對應模板 | 說明 |
| --- | --- | --- | --- | --- | --- |
| 首頁 | GET | `/` | `main_bp` | `main/index.html` | 顯示近期或推薦食譜 |
| 個人主頁 | GET | `/profile` | `main_bp` | `main/profile.html` | 顯示自己建立或收藏的食譜 |
| 註冊頁面 | GET | `/auth/register` | `auth_bp` | `auth/register.html` | 顯示註冊表單 |
| 送出註冊 | POST | `/auth/register` | `auth_bp` | — | 接收並寫入 DB，成功後重導向登入頁 |
| 登入頁面 | GET | `/auth/login` | `auth_bp` | `auth/login.html` | 顯示登入表單 |
| 送出登入 | POST | `/auth/login` | `auth_bp` | — | 驗證帳密並寫入 session |
| 登出 | GET | `/auth/logout` | `auth_bp` | — | 清除 session 並重導向首頁 |
| 一般搜尋 | GET | `/recipes/search` | `recipes_bp` | `recipes/search_results.html` | 透過一般關鍵字搜尋並顯示清單 |
| 食材搜尋 | GET | `/recipes/search_by_ingredients`| `recipes_bp` | `recipes/search_results.html` | 透過逗號分隔的食材查詢食譜 |
| 食譜詳情 | GET | `/recipes/<id>` | `recipes_bp` | `recipes/view.html` | 顯示食譜詳細內容與步驟 |
| 新增食譜頁 | GET | `/recipes/create` | `recipes_bp` | `recipes/create.html` | 顯示填寫食譜表單 |
| 送出食譜 | POST | `/recipes/create` | `recipes_bp` | — | 寫入食譜表單資料至 DB |
| 編輯食譜頁 | GET | `/recipes/<id>/edit`| `recipes_bp` | `recipes/edit.html` | 顯示已填寫的舊資料表單 |
| 送出編輯 | POST | `/recipes/<id>/edit`| `recipes_bp` | — | 寫入修改資料 |
| 刪除食譜 | POST | `/recipes/<id>/delete`| `recipes_bp` | — | 將食譜狀態設定為刪除或移出 DB |
| 加入收藏 | POST | `/recipes/<id>/save` | `recipes_bp` | — | 加入收藏清單 (saved_recipes) |
| 移除收藏 | POST | `/recipes/<id>/unsave`| `recipes_bp` | — | 移除收藏 |
| 後台儀表板 | GET | `/admin` | `admin_bp` | `admin/dashboard.html` | 管理員能看到的數據與清單 |
| 刪除食譜 | POST | `/admin/recipe/<id>/delete`| `admin_bp` | — | 強制刪除不當食譜 |
| 封鎖帳號 | POST | `/admin/user/<id>/ban` | `admin_bp` | — | 強制封鎖特定使用者 |

## 2. 每個路由詳細說明 (範例)

- **GET `/recipes/create`**
  - **輸入**：無
  - **處理邏輯**：檢查 session 是否包含 user_id (是否登入)
  - **輸出**：若已登入則回傳 `recipes/create.html`；若未登入則導向 `/auth/login`
  - **錯誤處理**：無

- **POST `/recipes/create`**
  - **輸入**：表單參數 `title`, `description`, `ingredients`, `steps`, `category`, `image_url`
  - **處理邏輯**：呼叫 `Recipe.create(...)` 存入 SQLite
  - **輸出**：重導向至 `GET /recipes/<id>`
  - **錯誤處理**：若必填為空，flash 警告訊息並重新顯示 create.html

*(其他路由依此類推)*

## 3. Jinja2 模板清單

所有模板都會繼承 `base.html`，統一處理 Header (選單) 與 Footer。

1. **`base.html`**：共用外觀
2. **`main/index.html`**：首頁食譜列表
3. **`main/profile.html`**：個人中心
4. **`auth/register.html`**：註冊表單
5. **`auth/login.html`**：登入表單
6. **`recipes/search_results.html`**：搜尋結果列表
7. **`recipes/view.html`**：單筆食譜詳細頁面
8. **`recipes/create.html`**：建立食譜表單頁
9. **`recipes/edit.html`**：編輯食譜表單頁
10. **`admin/dashboard.html`**：後台管理介面
