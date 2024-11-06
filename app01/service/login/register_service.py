from app01.cliant.user.user_client import UserAction


def register_user(user):

    exist_user = UserAction.user_exits(user.username)
    if exist_user:
        return False
    # 新增用户
    UserAction.user_create(
        user.username, user.email, user.password)
    return True
