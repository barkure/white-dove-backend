from fastapi import APIRouter
from services.auth_utils import is_token_valid
from services.users import create_user, get_user, update_user, delete_user, get_all_users, login, github_oauth, unbind_github_oauth, update_blogName
from config import GITHUB_OAUTH_URL

# 创建一个APIRouter实例
router = APIRouter()

# 创建用户
@router.post("/create_user")
async def create_user_endpoint(payload: dict):
    response = create_user(payload)
    return response

# 获取用户
@router.post("/get_user")
async def get_user_endpoint(payload: dict):
    response = get_user(payload)
    return response

# 更新用户
@router.post("/update_user")
async def update_user_endpoint(payload: dict):
    response = update_user(payload)
    return response

# 删除用户
@router.post("/delete_user")
async def delete_user_endpoint(payload: dict):
    response = delete_user(payload)
    return {"message": response}

# 获取所有用户
@router.get("/get_all_users")
async def get_all_users_endpoint():
    response = get_all_users()
    return response

# 登陆验证
@router.post("/login")
async def login_endpoint(payload: dict):
    response = login(payload)
    return response

# 验证 JWT 令牌
@router.post("/is_token_valid")
async def is_token_valid_endpoint(token: str):
    response = is_token_valid(token)
    return response

# Github OAuth 登陆/绑定
@router.post("/github_oauth")
async def github_oauth_endpoint(payload: dict):
    response = github_oauth(payload)
    return response

# 解绑 Github OAuth
@router.post("/unbind_github_oauth")
async def unbind_github_oauth_endpoint(payload: dict):
    response = unbind_github_oauth(payload)
    return response

# Github OAuth URL
@router.get("/github_oauth_url")
async def github_oauth_url_endpoint():
    return {"GITHUB_OAUTH_URL": GITHUB_OAUTH_URL}

# 修改站点名称
@router.post("/update_blogName")
async def update_blogName_endpoint(payload: dict):
    response = update_blogName(payload)
    return response