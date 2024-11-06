from django.contrib.auth import authenticate, login, logout


def loginByNameAndPwd(request, user_name, password):
    #  未登录的情况下，设置session会话

    if not request.user.is_authenticated:
        user_check = authenticate(username=user_name, password=password)
        if user_check is not None:
            login(request, user_check)
            return True
        else:
            return False
    return True


def do_logout(request):
    logout(request)
