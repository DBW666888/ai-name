from datetime import timedelta

DB_URI = "mysql+aiomysql://root:2b2b123123@127.0.0.1:3306/ai-name?charset=utf8mb4"



# 邮箱相关配置
MAIL_USERNAME="3506185106@qq.com"
MAIL_PASSWORD="xfzqikmjociaciga"
MAIL_FROM="3506185106@qq.com"
MAIL_PORT=587
MAIL_SERVER="smtp.qq.com"
MAIL_FROM_NAME="dbw"
MAIL_STARTTLS=True
MAIL_SSL_TLS=False


JWT_SECRET_KEY = "sfsadadafsj32w"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=15)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)