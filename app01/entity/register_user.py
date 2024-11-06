# ! -*-conding: UTF-8 -*-
from pydantic import EmailStr
from .user import User


class RegisterUser(User):
    email: EmailStr
