# import_export.py 用来导入导出数据
import os
import shutil
import zipfile
from db import SessionLocal
from models import Articles

def export_articles():
    # 创建一个新的数据库会话
    db = SessionLocal()
    try:
        articles = db.query(Articles).all()
        os.makedirs('Import_Export/export_articles/', exist_ok=True)
        # 写入数据
        for article in articles:
            with open(f'Import_Export/export_articles/{article.article_id}+{article.title}+{(article.create_date.replace(":", "-") if article.create_date else "None")}+{(article.update_date.replace(":", "-") if article.update_date else "None")}.md', 'w', encoding='utf-8') as f:
                # 写入文章的内容
                f.write(article.content)
    finally:
        db.close()
    
        # 创建压缩包
    zip_path = 'Import_Export/export_articles.zip'
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        # 遍历 export_articles 目录
        for foldername, subfolders, filenames in os.walk('Import_Export/export_articles/'):
            for filename in filenames:
                # 添加每个文件到压缩文件
                zipf.write(os.path.join(foldername, filename))
        # 删除 export_articles 目录
    shutil.rmtree('Import_Export/export_articles/')
    return zip_path


def import_articles(file_path: str):
    db = SessionLocal()
    try:
        # 遍历 import_articles 目录
        for filename in os.listdir(file_path):
            # 只处理 .md 文件
            if filename.endswith('.md'):
                # 从文件名中获取文章的信息
                article_id, title, create_date, update_date = filename[:-3].split('+')
                create_date = create_date.replace("-", ":") if create_date != "None" else None
                update_date = update_date.replace("-", ":") if update_date != "None" else None
                # 读取文件的内容
                with open(file_path+f'{filename}', 'r', encoding='utf-8') as f:
                    content = f.read()
                # 检查数据库中是否已经存在具有相同 article_id 的文章
                existing_article = db.query(Articles).filter(Articles.article_id == article_id).first()
                if existing_article is None:
                    # 如果不存在，创建一个新的文章对象并添加到数据库
                    article = Articles(article_id=article_id, title=title, create_date=create_date, update_date=update_date, content=content)
                    db.add(article)
                else:
                    # 如果存在，更新现有的文章
                    existing_article.title = title
                    existing_article.create_date = create_date
                    existing_article.update_date = update_date
                    existing_article.content = content
        # 提交数据库会话
        db.commit()
    finally:
        # 关闭数据库会话
        db.close()
        # 删除 import_articles 目录
    shutil.rmtree(file_path)