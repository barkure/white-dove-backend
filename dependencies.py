# dependencies.py 用来全局鉴权
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from services.auth_utils import is_token_valid
import re

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

async def verify_token(request: Request, token: str = Depends(oauth2_scheme)):
    whitelist = [r"^/articles/get_all_titles",
                 r"^/articles/get_article/.*",
                 r"^/users/github_oauth_url",
                 r"^/users/github_oauth",
                 r"^/users/login",
                 r"^/static/.*"]  # 使用正则表达式
    if any(re.match(path, str(request.url.path)) for path in whitelist):  # 使用 re.search
        print(str(request.url.path))
        return True
    elif token is not None and is_token_valid(token) == True:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="登录已过期！请重新登录！",
            headers={"WWW-Authenticate": "Bearer"},
        )