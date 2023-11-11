# 定义 GitHub OAuth 配置
GITHUB_CLIENT_ID = "Iv1.d6ebdcdaf104ba3c"
GITHUB_CLIENT_SECRET = "016d84685685b129b10fced1d687e07e9c2581ae"
# GitHub回调地址
REDIRECT_URI = "http://localhost:3000/github-oauth-redirect" # 此项根据前端地址修改
# GitHub授权链接，此项不用修改
GITHUB_OAUTH_URL = f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={REDIRECT_URI}"

# 前端地址，此项根据前端地址修改
FRONTEND_URL = "http://localhost:3000" # 此项根据前端地址修改
# 配置 JWT 密钥和算法
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256" # 默认是 HS256 算法

# 配置TOKEN过期时间
ACCESS_TOKEN_EXPIRE_MINUTES = 30

