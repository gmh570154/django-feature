from pydantic import ValidationError
from django01.utils.exceptions import BusinessException
from django01.utils.enums import StatusCodeEnum


def transform_data_to_object(data, obj):
    try:
        return obj(**data)
    except ValidationError as e:
        print(f"Validation error: {e.json()}")
        raise BusinessException(StatusCodeEnum.PARAM_ERR)
