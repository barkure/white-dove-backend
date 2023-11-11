# models.py: 定义数据库表结构
from sqlalchemy import Column, Integer, String
from db import Base

# 定义Users模型类
class  Users(Base):
    __tablename__ = "Users"

    # fields
    user_id = Column(Integer,primary_key=True, index=True)
    userName = Column(String(20))
    password = Column(String(20))
    email = Column(String(20))
    GitHub_id = Column(String(20))

# 定义Articles模型类
class Articles(Base):
    __tablename__ = "Articles"

    # fields
    article_id = Column(Integer,primary_key=True, index=True)
    title = Column(String(100))
    content = Column(String(10000))
    author = Column(String(20))
    create_date = Column(String(20))
    update_date = Column(String(20))

# 定义博客设置项模型类
class BlogSettings(Base):
    __tablename__ = "BlogSettings"

    # fields
    setting_id = Column(Integer,primary_key=True, index=True)
    blogName = Column(String(100))
    faviconName = Column(String(100))

