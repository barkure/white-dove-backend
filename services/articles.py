from db import SessionLocal
from models import Articles
from datetime import datetime
from sqlalchemy import desc


# 创建文章
def create_article(payload: dict):
    title = payload.get("title")
    content = payload.get("content")
    author = payload.get("author")
    # 创建数据库会话
    db = SessionLocal()
    # 获取当前时间
    create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 创建文章对象
    article = Articles(title=title, content=content, author=author, create_date=create_date)
    # 添加到数据库
    db.add(article)
    db.commit()
    db.refresh(article)
    # 关闭数据库会话
    db.close()
    return "Article created"
 
# 查询文章
def get_article(article_id: int):
    # 创建数据库会话
    db = SessionLocal()
    # 查询文章
    article = db.query(Articles).filter(Articles.article_id == article_id).first()
    # 关闭数据库会话
    db.close()
    if article:
        return {
            "article_id": article.article_id,
            "title": article.title,
            "content": article.content,
            "author": article.author,
            "create_date": article.create_date,
            "update_date": article.update_date
        }
    else:
        return ["Article not found"]
    
# 更新文章
def update_article(payload: dict):
    article_id = payload.get("article_id")
    title = payload.get("title")
    content = payload.get("content")
    # 创建数据库会话
    db = SessionLocal()
    update_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 查询文章
    article = db.query(Articles).filter(Articles.article_id == article_id).first()
    if article:
        if title is not None:
            article.title = title
        if content is not None:
            article.content = content
        if update_date is not None:
            article.update_date = update_date
        db.commit()
        db.close()
        return "Article updated"
    else:
        db.close()
        return "Article not found"
    
# 删除文章
def delete_article(payload: dict):
    article_id = payload.get("article_id")
    # 创建数据库会话
    db = SessionLocal()
    # 查询文章
    article = db.query(Articles).filter(Articles.article_id == article_id).first()
    if article:
        db.delete(article)
        db.commit()
        db.close()
        return "Article deleted"
    else:
        db.close()
        return "Article not found"
    
# 查询所有文章标题
def get_all_titles():
    # 创建数据库会话
    db = SessionLocal()
    # 查询所有文章
    articles = db.query(Articles).all()
    # 关闭数据库会话
    db.close()
    all_titles = []
    for article in articles:
        # 创建包含标题和ID的字典
        article_dict = {"title": article.title, "article_id": article.article_id, "create_date": article.create_date, "update_date": article.update_date}
        all_titles.append(article_dict)
    all_titles.reverse()
    return all_titles

# 根据分页查询文章标题
def get_titles_by_page(payload: dict):
    page = payload.get("page")
    per_page = payload.get("per_page")
    # page: 页码, per_page: 每页数量
    db = SessionLocal()
    articles = db.query(Articles).order_by(desc(Articles.create_date)).offset((page - 1) * per_page).limit(per_page).all()
    db.close()
    titles_list = []
    for article in articles:
        titles_list.append(article.title)
    return titles_list
