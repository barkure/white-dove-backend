# main.py
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.user_router import router as user_router
from routers.article_router import router as article_router
from routers.blog_settings_router import router as blog_settings_router
from dependencies import verify_token  # 导入 verify_token
from config import FRONTEND_URL

app = FastAPI(dependencies=[Depends(verify_token)])

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # 允许的域名，可以根据需求更改为你的前端域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许的 HTTP 方法，这里允许所有
    allow_headers=["*"],  # 允许的 HTTP 请求头，这里允许所有
)

# 添加用户路由
app.include_router(user_router, prefix="/users", tags=["users"])
# 添加文章路由
app.include_router(article_router, prefix="/articles", tags=["articles"])
# 添加博客设置路由
app.include_router(blog_settings_router, prefix="/static", tags=["blog_settings"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)