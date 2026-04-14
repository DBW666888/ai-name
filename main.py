from fastapi import FastAPI
from fastapi_mail import FastMail,MessageSchema,MessageType
from fastapi import Depends
from routers.auth_router import router as auth_router
from dependencies import get_mail
from aiosmtplib import SMTPResponseException
from routers.name_router import router as name_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(name_router)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/mail/test")
async def smail_test(
        email: str,
        mail: FastMail = Depends(get_mail),
):
    message = MessageSchema(
        subject="测试邮件",
        recipients=[email],
        body=f"这是一封来自 FastAPI 的测试邮件，发送给：{email}",
        subtype=MessageType.plain,
    )
    try:
        await mail.send_message(message)
        return {"message": "邮件发送成功！"}
    except Exception as e:
        return {"message": f"邮件发送失败：{str(e)}"}
