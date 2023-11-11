import os
from fastapi import APIRouter, File, UploadFile
from services.articles import create_article, get_article, update_article, delete_article, get_all_titles
from services.import_export import export_articles, import_articles
from fastapi.responses import FileResponse

# 创建一个APIRouter实例
router = APIRouter()

# 创建文章
@router.post("/create_article")
async def create_article_endpoint(payload: dict):
    create_article(payload)
    return {"message": "Article created"}

# 查询文章
@router.get("/get_article/{article_id}")
async def get_article_endpoint(article_id: int):
    response = get_article(article_id)
    return response

# 更新文章
@router.post("/update_article")
async def update_article_endpoint(payload: dict):
    response = update_article(payload)
    return {"message": response}

# 删除文章
@router.post("/delete_article")
async def delete_article_endpoint(payload: dict):
    response = delete_article(payload)
    return {"message": response}

# 查询所有文章标题
@router.get("/get_all_titles")
async def get_all_titles_endpoint():
    response = get_all_titles()
    return response

# 分页查询文章标题
@router.get("/get_titles_by_page")
async def get_titles_by_page_endpoint(page: int, size: int):
    response = get_all_titles()
    return response

# Import 导入文章
@router.post("/import")
async def import_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    file_path = 'Import_Export/import_articles/'
    os.makedirs(file_path, exist_ok=True)
    with open(file_path+f'{file.filename}', 'wb') as f:
        f.write(contents)
    response = import_articles(file_path)
    return {"message": response}

# Export 导出文章为压缩包
@router.get("/export_zip")
async def export_zip_endpoint():
    file_path = export_articles()
    return FileResponse(file_path)

# Export 导出文章为 sqlite 数据库
@router.get("/export_sqlite")
async def export_sqlite_endpoint():
    file_path = 'data.db'
    return FileResponse(file_path)