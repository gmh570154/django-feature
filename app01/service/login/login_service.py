from app01.cliant.auth.auth_client import AuthClient


def loginByNameAndPwd(request, user_name, password):

    #  未登录的情况下，设置session会话
    if not request.user.is_authenticated:
        user_check = AuthClient.check_username_password(user_name, password)

        if user_check is not None:
            AuthClient.login_user(request, user_check)
        else:
            return False
    return True


def do_logout(request):
    AuthClient.logout_user(request)
