# # 定义 GitHub OAuth 配置
# GITHUB_CLIENT_ID = "your-github-client-id"
# GITHUB_CLIENT_SECRET = "your-github-client-secret"
# # 前端地址
# FRONTEND_URL = "http://localhost:8080"
# # 配置 JWT 密钥
# SECRET_KEY = "your-secret-key"
# # 配置TOKEN过期时间
# ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # 默认24小时

# 如果你要自己前后端分离部署，那么你需要取消上面的注释，按需修改配置项，且应该注释掉下面的配置项。
# 从环境变量中获取配置项
import os
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
# 前端地址
FRONTEND_URL = os.getenv("FRONTEND_URL")
# 配置 JWT 密钥
SECRET_KEY = os.getenv("SECRET_KEY")
# 配置TOKEN过期时间
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))  # 默认24小时


# 以下是公共配置，无需修改
# GitHub授权链接，此项不用修改
GITHUB_OAUTH_URL = f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={REDIRECT_URI}"
# GitHub回调地址
REDIRECT_URI = f"{FRONTEND_URL}/github-oauth-redirect"
# JWT 算法
ALGORITHM = "HS256" 