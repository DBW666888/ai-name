from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import EmailStr
from typing import Annotated, Optional
from dependencies import get_mail,get_session
from models import AsyncSession
import string
import random
from fastapi_mail import FastMail, MessageSchema, MessageType
from aiosmtplib import SMTPResponseException

from models.user import User
from repository.user_repo import EmailCodeRepository,UserRepository
from schemas import ResponseOut
from schemas.user import RegisterIn,UserCreateSchema,LoginIn,LoginOut
from core.auth import AuthHandler
router = APIRouter(prefix="/auth", tags=["auth"])

auth_handler=AuthHandler()
@router.get("/code",response_model=ResponseOut)
async def get_email_code(
        email: Annotated[EmailStr, Query(...)],
        mail: FastMail = Depends(get_mail),
        session: AsyncSession = Depends(get_session),
):
    # 生成验证码
    source = string.digits * 4
    code = "".join(random.sample(source, 4))
    message = MessageSchema(
        subject="【博闻智能取名助手】注册验证码",
        recipients=[email],
        body=f"【博闻智能取名助手】您的注册验证码为：{code}，10分钟有效。",
        subtype=MessageType.plain
    )
    try:
        print(f"验证码：{code}")
        await mail.send_message(message)
    except SMTPResponseException as e:
        # 检查是否是 QQ 特有的二进制响应错误
        if not (e.code == -1 and b"\x00\x00\x00" in str(e).encode()):
             raise HTTPException(500, f"邮件发送失败！{str(e)}")
        print("⚠️ 忽略 QQ 邮箱 SMTP 关闭阶段的非标准响应（邮件已成功发送）")

    # 无论成功发送还是遇到可忽略的错误，都保存验证码
    email_code_repo = EmailCodeRepository(session=session)
    await email_code_repo.create(email=str(email), code=code)
    return ResponseOut()


@router.post('/register', response_model=ResponseOut)
async def register(
        data: RegisterIn,
        session: AsyncSession = Depends(get_session)
):
    user_repo = UserRepository(session=session)
    #1.判断邮箱是否存在
    if await user_repo.email_is_exist(email=str(data.email)):
        raise HTTPException(status_code=400, detail="邮箱已经存在！")
    #2.校验验证码是否正确
    email_code_repo = EmailCodeRepository(session=session)
    if not await email_code_repo.check_email_code(email=str(data.email), code=data.code):
        raise HTTPException(status_code=400, detail="邮箱验证码错误！")
    try:
        await user_repo.create(UserCreateSchema(email=data.email, username=data.username, password=data.password))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return ResponseOut()



@router.post('/login', response_model=LoginOut)
async def login(
    data: LoginIn,
    session: AsyncSession = Depends(get_session),
):
    # 1. 创建user_repo对象
    user_repo = UserRepository(session=session)
    # 2. 根据邮箱查找用户
    user: Optional[User] = await user_repo.get_by_email(str(data.email))
    if not user:
        raise HTTPException(400, detail="该用户不存在！")
    if not user.check_password(data.password):
        raise HTTPException(400, detail="邮箱或密码错误！")
    # 3. 生成JWToken
    tokens = auth_handler.encode_login_token(user.id)
    return {
        "user": user,
        "token": tokens['access_token']
    }