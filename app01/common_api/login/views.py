import json

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from app01.entity.user import User
from app01.util.transform import transform_data_to_object
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
        # 接收参数校验
        body = self.get_request_body(request)
        user = transform_data_to_object(body, User)
        # 用户名密码登录操作
        login_result = loginByNameAndPwd(request, user.username, user.password)

        # 记录操作日志
        result = "success" if login_result else "failed"
        self.set_log_action_name("user login", user.username, result)
        self.save_operation_log(request)

        # 根据操作结果返回异常或者正常内容
        if login_result is False:
            raise BusinessException(StatusCodeEnum.PWD_ERR)

        return {"success": True}


def loginByNameAndPwd(request, user_name, password):
    #  未登录的情况下，设置session会话
    if not request.user.is_authenticated:
        user_check = authenticate(username=user_name, password=password)
    if user_check is not None:
        login(request, user_check)
        return True
    else:
        return False


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
                self.save_operation_log(request)
                raise BusinessException(StatusCodeEnum.REGISTER_FAILED_ERR)

        self.result = "success"
        self.save_operation_log(request)
        return HttpResponseRedirect('/web/login')
