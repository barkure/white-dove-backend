# white-dove-backend
 博客系统 White Dove 的后端，使用 FastAPI，如果你还没部署前端，请访问 [white-dove-frontend](https://github.com/barkure/white-dove-frontend).
# 后端部署方法
## 创建 Docker Compose 文件
你可以为后端新建一个目录，比如名为`white-dove-backend`，然后新建一个`docker-compose.yml`文件，内容如下：
```yaml
version: '3'
services:
  white-dove-backend:
    image: barkure/white-dove-backend:0.1.0
    ports:
      - "1234:8000"
#      - 此处可修改为你要的端口
    environment:
      - GITHUB_CLIENT_ID=XXXXXXXXXX
      # 将 GitHub 申请到的 GITHUB_CLIENT_ID 粘贴到这里
      - GITHUB_CLIENT_SECRET=XXXXXXXXXX
      # 将 GitHub 申请到的 GITHUB_CLIENT_SECRET 粘贴到这里
      - FRONTEND_URL=https://blog.barku.re
      # 前端基本URL，即就是博客地址
      - SECRET_KEY=XXXXXXXXXX
      # 用来生成鉴权的令牌，可以键入随机字符串
      - ACCESS_TOKEN_EXPIRE_MINUTES=1440
      # 密钥有效期，此处是1440分钟，即一天
```
**GITHUB_CLIENT_ID**和**GITHUB_CLIENT_SECRET**需自己申请，指路如下： `GitHUb主页`--->`Settings`--->`Developer Settings`--->`GitHub Apps`--->`New GitHub App`.


Callback URL 为前端地址 + `/github-oauth-redirect`， 如`http://blog.barku.re/github-oauth-redirect`， 其他配置项可按需更改.
## 运行
在**docker-compose.yml**所在目录下，使用命令 `docker-compose up` 运行
## 其他
你可能还需要设置 SSL证书 和 Nginx反向代理，请自行完成.
