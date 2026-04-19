# 博闻智能取名助手 (ai-name)

一个基于 FastAPI 和 DeepSeek AI 的智能化命名系统，旨在结合中国传统文化与现代 AI 技术，为用户提供兼具音律美感与文化内涵的命名方案。

## 🌟 项目特点

- **AI 智能命名**：集成 DeepSeek 大语言模型，精通《诗经》、《楚辞》等经典文献，提供专业起名建议。
- **文化底蕴**：每个名字均附带出处说明、寓意解析及字义拆解，确保“名以载道”。
- **全栈实现**：包含基于 FastAPI 的异步后端接口和基于 Uni-app 的多端前端应用。
- **完善的账号体系**：支持邮箱验证码注册、JWT 身份认证，确保用户信息安全。
- **异步架构**：后端采用异步编程（AsyncIO），支持高并发请求处理。

## 🛠️ 技术栈

### 后端 (Backend)
- **框架**: [FastAPI](https://fastapi.tiangolo.com/)
- **AI 引擎**: [DeepSeek](https://www.deepseek.com/) (通过 LangChain 集成)
- **数据库 ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (异步驱动)
- **数据库迁移**: [Alembic](https://alembic.sqlalchemy.org/)
- **邮件服务**: [FastAPI-Mail](https://sabuhish.github.io/fastapi-mail/)
- **认证**: PyJWT + pwdlib (Argon2)
- **数据验证**: Pydantic v2

### 前端 (Frontend)
- **框架**: [Uni-app](https://uniapp.dcloud.net.cn/) (Vue.js 3)
- **网络请求**: 封装的异步请求拦截器

## 📂 项目结构

```text
ai-name/
├── alembic/                # 数据库迁移脚本
├── core/                   # 核心逻辑 (AI Agent, Auth, Mail)
├── models/                 # SQLAlchemy 数据库模型
├── repository/             # 数据库操作逻辑 (Repository Pattern)
├── routers/                # API 路由 (Auth, Name)
├── schemas/                # Pydantic 数据验证模型
├── settings/               # 全局配置管理
├── take-name-app/          # Uni-app 前端项目代码
├── main.py                 # 程序入口
├── requirements.txt        # 依赖清单
└── alembic.ini             # Alembic 配置文件
```

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/your-username/ai-name.git
cd ai-name
```

### 2. 后端配置

1. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

2. **修改关键配置**:
   为了使项目正常运行，您**必须**修改以下文件中的个人配置信息：

   #### 📧 邮箱配置 ([settings/__init__.py](file:///e:/AI%20development/ai_project/ai-name/settings/__init__.py))
   - `MAIL_USERNAME`: 您的发件人邮箱地址（如 QQ 邮箱）。
   - `MAIL_PASSWORD`: 您的邮箱 SMTP 授权码（非登录密码）。
   - `MAIL_FROM`: 发件人邮箱地址。
   - `MAIL_FROM_NAME`: 发件人显示名称。

   #### 🗄️ 数据库配置 ([settings/__init__.py](file:///e:/AI%20development/ai_project/ai-name/settings/__init__.py))
   - `DB_URI`: 按照格式 `mysql+aiomysql://用户名:密码@地址:端口/数据库名` 修改为您的数据库连接。

   #### 🔑 安全与 AI 配置
   - **JWT 密钥** ([settings/__init__.py](file:///e:/AI%20development/ai_project/ai-name/settings/__init__.py)): 修改 `JWT_SECRET_KEY` 为一个随机的长字符串以确保 Token 安全。
   - **DeepSeek API Key** ([core/agent.py](file:///e:/AI%20development/ai_project/ai-name/core/agent.py)): 在初始化 `ChatDeepSeek` 时填入您从 DeepSeek 官网获取的 `api_key`。

3. **数据库迁移**:
   ```bash
   alembic upgrade head
   ```

4. **启动服务**:
   ```bash
   uvicorn main:app --reload
   ```

### 3. 前端配置
1. 使用 **HBuilderX** 打开 `take-name-app` 目录。
2. 修改 `http/http.js` 中的 `baseURL` 为您的后端地址。
3. 点击“运行” -> “运行到浏览器”或“运行到手机模拟器”。

## 📖 API 文档

服务启动后，可以通过以下地址查看自动生成的交互式 API 文档：
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 许可。
