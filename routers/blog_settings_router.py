import os
import shutil
from fastapi import APIRouter, File, HTTPException, UploadFile
from db import SessionLocal
from services.articles import create_article, get_article, update_article, delete_article, get_all_titles
from services.import_export import export_articles, import_articles
from fastapi.responses import FileResponse
from models import BlogSettings
from PIL import Image


# 创建一个APIRouter实例
router = APIRouter()

# 转换图片为 favicon
def convert_to_favicon(image_path, output_path, size, format):
    # 打开并加载图片
    img = Image.open(image_path)
    # 转换图片为 RGBA 模式
    img = img.convert("RGBA")
    # 调整图片大小
    img = img.resize((size, size))
    # 保存图片为 .ico 格式
    img.save(output_path, format=format)

@router.post("/upload_favicon")
async def upload_favicon_endpoint(file: UploadFile = File(...)):
    icon = await file.read()
    file_path = 'static/'
    os.makedirs(file_path, exist_ok=True)
    # 获取文件的扩展名
    with open(file_path + file.filename, 'wb') as f:
        f.write(icon)
    # 转换图片为 favicon
    convert_to_favicon(file_path + file.filename, 'static/favicon.ico', 32, 'ICO')
    # 转换图片为 apple-icon
    convert_to_favicon(file_path + file.filename, 'static/logo192.png', 192, 'PNG')
    os.remove(file_path + file.filename)
    return {"message": "favicon uploaded successfully"}

# 获取 favicon/apple-icon
@router.get("/icon/{filename}")
async def get_favicon_endpoint(filename: str):
    print(filename)
    if os.path.exists(f"static/{filename}"):
        return FileResponse(f"static/{filename}")
    else:
        raise HTTPException(status_code=404, detail="File not found")

# 获取 blogName
@router.get("/get_blogName")
async def get_blogName_endpoint():
    db = SessionLocal()
    try:
        blogName = db.query(BlogSettings).first().blogName
        return {"blogName": blogName}
    finally:
        db.close()