from datetime import timedelta
from db import SessionLocal
from models import Users, BlogSettings
from services.auth_utils import create_access_token
from config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, ACCESS_TOKEN_EXPIRE_MINUTES
import requests

# 添加用户
def create_user(payload: dict):
    userName = payload.get("userName")
    password = payload.get("password")
    email = payload.get("email")
    db = SessionLocal()
    new_user = Users(userName=userName, password=password, email=email)
    db.add(new_user)
    db.commit()
    db.close()
    return "User created"

# 查询用户
def get_user(payload: dict):
    user_id = payload.get("user_id")
    db = SessionLocal()
    user = db.query(Users).filter(Users.user_id == user_id).first()
    db.close()
    if user:
        return {
            "user_id": user.user_id,
            "userName": user.userName,
            "email": user.email,
            "GitHub_id": user.GitHub_id
        }
    else:
        return ["User not found"]
    
# 更新用户
def update_user(payload: dict):
    user_id = payload.get("user_id")
    userName = payload.get("userName")
    password = payload.get("password")
    email = payload.get("email")
    GitHub_id = payload.get("GitHub_id")
    db = SessionLocal()
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user:
        if userName is not None:
            user.userName = userName
        if password is not None:
            user.password = password
        if email is not None:
            user.email = email
        if GitHub_id is not None:
            user.GitHub_id = GitHub_id
        db.commit()
        db.close()
        return {
            "update_yes": True,
        }
    else:
        db.close()
        return {
            "update_yes": False,
        }
    
# 删除用户
def delete_user(payload: dict):
    user_id = payload.get("user_id")
    db = SessionLocal()
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        db.close()
        return "User deleted"
    else:
        db.close()
        return "User not found"

# 查询所有用户
def get_all_users():
    db = SessionLocal()
    all_users = db.query(Users).all()
    db.close()
    user_list = []
    for user in all_users:
        user_dict = {
            "user_id": user.user_id,
            "userName": user.userName,
            "email": user.email,
            "GitHub_id": user.GitHub_id
        }
        user_list.append(user_dict)
    return user_list

# 登录验证
def login(payload: dict):
    userNameOrEmail = payload.get("userNameOrEmail")
    password = payload.get("password")
    db = SessionLocal()
    user = db.query(Users).filter((Users.userName == userNameOrEmail) | (Users.email == userNameOrEmail)).first()
    db.close()
    if user:
        if user.password == password:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"sub": user.userName}, expires_delta=access_token_expires)
            return {
                "login_yes": True,
                "token": access_token,
                "userName": user.userName,
                "email": user.email,
                "user_id": user.user_id,
                "GitHub_id": user.GitHub_id
            }
        else:
            return {
                "login_yes": False,
                "token": None,
            }
    else:
        return {
            "login_yes": False,
            "token": None,
        }
    
    
# 绑定 GitHub 账号
def bind_github(GitHub_id: str, user_id: int):
    db = SessionLocal()
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user:
        user.GitHub_id = GitHub_id
        db.commit()
        db.close()
        return {
            "bind_yes": True,
            "GitHub_id": GitHub_id,
        }
    else:
        db.close()
        return {
            "bind_yes": False,
            }

# Github OAuth
def github_oauth(payload: dict):
    code = payload.get("code")
    user_id = payload.get("user_id")
    operation = payload.get("operation") # 根据 operation 判断是登录还是绑定
    print('Code:', code, 'Operation:', operation)
    resp1 = requests.post("https://github.com/login/oauth/access_token?"+"client_id="+GITHUB_CLIENT_ID+"&client_secret="+GITHUB_CLIENT_SECRET+"&code="+code, headers={"Accept": "application/json"})
    if resp1.status_code == 200:
        print('Status code:', resp1.status_code)
        access_token = resp1.json().get("access_token")
        print('Access token:', access_token)
        # 设置请求标头，包括授权令牌
        headers = {
            'Authorization': f'token {access_token}',
        }
        resp2 = requests.get("https://api.github.com/user", headers=headers)
        if resp2.status_code == 200:
            GitHub_id = resp2.json().get("id")
            print('GitHub_id啦啦啦啦啦啦啦啦啦啦啦:', GitHub_id)
            if operation =="login":
                print('GitHub_id:', GitHub_id)
                return github_login(GitHub_id)
            elif operation == "bind":
                return bind_github(GitHub_id, user_id)
            
        else:
            return {
                "message": "获取GitHub用户信息失败",
                "token": None,
            }
    else:
        return {
            "message": "code无效",
            "token": None,
        }

# GitHub 登录
def github_login(GitHub_id: str):
    print('GitHub_id:', GitHub_id)
    db = SessionLocal()
    user = db.query(Users).filter(Users.GitHub_id == GitHub_id).first()
    if user:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.userName}, expires_delta=access_token_expires)
        db.close()
        return {
            "login_yes": True,
            "token": access_token,
            "userName": user.userName,
            "email": user.email,
            "user_id": user.user_id,
            "GitHub_id": user.GitHub_id
        }
    else:
        db.close()
        return {
            "login_yes": False,
            "token": None,
        }
    
# 解绑 GitHub 账号
def unbind_github_oauth(payload: dict):
    user_id = payload.get("user_id")
    db = SessionLocal()
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user:
        user.GitHub_id = None
        db.commit()
        db.close()
        return {
            "unbind_yes": True,
        }
    else:
        db.close()
        return {
            "unbind_yes": False,
            }
    
# 创建博客设置项  
def create_blog_settings():
    db = SessionLocal()
    blog_settings = db.query(BlogSettings).first()
    if not blog_settings:
        blog_settings = BlogSettings(blogName="Default Blog Name")
        db.add(blog_settings)
        db.commit()
    db.close()

# 更改站点名称
def update_blogName(payload: dict):
    print('payload:', payload)
    blogName = payload.get("blogName")
    create_blog_settings()
    print('blogName:', blogName)
    db = SessionLocal()
    blog_settings = db.query(BlogSettings).first()
    print('blog_settings:', blog_settings)
    if blog_settings:
        blog_settings.blogName = blogName
        db.commit()
        db.close()
        return {
            "update_yes": True,
        }
    else:
        db.close()
        return {
            "update_yes": False,
        }