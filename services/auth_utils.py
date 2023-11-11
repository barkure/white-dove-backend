from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import JWTError
import jwt
from models import Users
from db import SessionLocal
from config import SECRET_KEY, ALGORITHM




# 创建 JWT 令牌
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 验证 JWT 令牌
def is_token_valid(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_timestamp = payload.get("exp")
        current_time = datetime.utcnow()
        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        db = SessionLocal()
        userName = payload.get("sub")
        user = db.query(Users).filter(Users.userName == userName).first()
        if user:
            if exp_datetime < current_time:
                # 令牌已过期
                return False
            else:
                return True
        else:
            return False
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        return False
    except jwt.DecodeError:  # 添加这一行
        return False  # 和这一行