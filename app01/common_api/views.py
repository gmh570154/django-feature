import json

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from django01.core.base_view import BaseView
from django01.utils.exceptions import BusinessException
from django01.utils.enums import StatusCodeEnum


class UserLogin(BaseView):
    """
    用户登陆
    """

    def get(self, request):
        '''登录页面'''
        return render(request, 'login.html')

    def post(self, request):
        '''用户登录'''
        json_str = request.body
        json_dict = json.loads(json_str)
        user_name = json_dict.get("user_name")
        password = json_dict.get("password")
        self.action = "user login"
        self.resource_id_name = json_dict.get("user_name", "")

        #  未登录的情况下，设置session会话
        if not request.user.is_authenticated:
            user_check = authenticate(username=user_name, password=password)
            if user_check is not None:
                login(request, user_check)
            else:
                self.result = "failed"
                self.save_operation_log(request, self.resource_id_name,
                                        self.action, self.result)
                raise BusinessException(StatusCodeEnum.PWD_ERR)
        self.result = "success"
        self.save_operation_log(
            request, self.resource_id_name, self.action, self.result)
        return {"success": True}


class UserLogout(BaseView):
    """
    用户登出
    """

    def get(self, request):
        response = HttpResponseRedirect('/web/login')
        logout(request)
        return response


class UserRegister(BaseView):
    """
    用户注册
    """

    def post(self, request):

        json_str = request.body
        json_dict = json.loads(json_str)
        user_name = json_dict.get("user_name")
        password = json_dict.get("password")
        email = json_dict.get("email")
        self.action = "user register"
        self.resource_id_name = json_dict.get("user_name", "")

        if user_name and password:
            # 保存用户信息

            exist_user = User.objects.filter(username=user_name).exists()
            if not exist_user:
                user = User.objects.create_user(
                    user_name, email, password)
                user.save()
            else:
                self.result = "failed"
                self.save_operation_log(request, self.resource_id_name,
                                        self.action, self.result)
                raise BusinessException(StatusCodeEnum.REGISTER_FAILED_ERR)

        self.result = "success"
        self.save_operation_log(request, self.resource_id_name,
                                self.action, self.result)
        return HttpResponseRedirect('/web/login')
