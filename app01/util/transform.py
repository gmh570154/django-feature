from pydantic import ValidationError
from django01.utils.exception.exceptions import BusinessException
from django01.utils.enums.enums import StatusCodeEnum


class Transform:

    @classmethod
    def data_to_object(data, obj):
        try:
            return obj(**data)
        except ValidationError as e:
            print(f"Validation error: {e.json()}")
            raise BusinessException(StatusCodeEnum.PARAM_ERR)
