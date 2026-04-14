from typing import Optional
from models import AsyncSession
from models.user import User, EmailCode
from sqlalchemy import select, update, delete, exists
from datetime import datetime, timedelta

from models.user import User
from schemas.user import UserCreateSchema
class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        async with self.session.begin():
            return await self.session.scalar(select(User).where(User.email==email))

    async def email_is_exist(self, email: str) -> bool:
        async with self.session.begin():
            stmt = select(exists().where(User.email==email))
            return await self.session.scalar(stmt)

    async def create(self, user_schema: UserCreateSchema) -> User:
        async with self.session.begin():
            user = User(**user_schema.model_dump())
            self.session.add(user)
            return user


class EmailCodeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, email: str, code: str) -> EmailCode:
        async with self.session.begin():
            email_code = EmailCode(email=email, code=code)
            self.session.add(email_code)
            return email_code

    async def check_email_code(self, email: str, code: str) -> bool:
        async with self.session.begin():
            stmt = select(EmailCode).where(
                EmailCode.email == email,
                EmailCode.code == code
            ).order_by(EmailCode.create_time.desc()).limit(1)
            email_code: Optional[EmailCode] = await self.session.scalar(stmt)
            if not email_code:
                return False
            if (datetime.now() - email_code.create_time) > timedelta(minutes=10):
                return False
            return True