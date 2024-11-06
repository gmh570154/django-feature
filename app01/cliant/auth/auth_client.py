from django.contrib.auth import authenticate, login, logout


class AuthClient:

    @staticmethod
    def check_username_password(user_name, password):
        return authenticate(username=user_name, password=password)

    @staticmethod
    def login_user(request, user_check):
        login(request, user_check)

    @staticmethod
    def logout_user(request):
        logout(request)
