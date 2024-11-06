# ! -*-conding: UTF-8 -*-
from pydantic import EmailStr
from typing import Optional
from .user import User


class RegisterUser(User):
    email: EmailStr
    signup_ts: Optional[str] = None  # 可选参数验证
