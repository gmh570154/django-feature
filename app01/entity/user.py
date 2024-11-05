# ! -*-conding: UTF-8 -*-
from typing import Optional
from pydantic import BaseModel, field_validator


def check_name(v: str) -> str:
    """Validator to be used throughout"""
    if len(v) < 2 or len(v) > 12:
        raise ValueError("must be range 2~12")
    return v


class User(BaseModel):
    username: str
    password: str

    validate_fields = field_validator("username")(check_name)

    @field_validator("password")
    @classmethod
    def check_password(cls, password):
        if len(password) > 18:
            raise ValueError("用户密码长度必须小于18")
        return password
