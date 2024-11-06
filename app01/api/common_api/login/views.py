from django.http import HttpResponseRedirect
from django.shortcuts import render

from app01.entity.user import User as EntityUser
from app01.entity.register_user import RegisterUser
from app01.util.transform import Transform
from app01.service.login import register_service, login_service
from django01.core.base_view import BaseView
from django01.utils.exception.exceptions import BusinessException
from django01.utils.enums.enums import StatusCodeEnum


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
        data = self.get_request_body(request)
        user = Transform.data_to_object(data, EntityUser)

        # 用户名密码登录操作
        login_result = login_service.loginByNameAndPwd(
            request, user.username, user.password)

        # 记录操作日志
        self.set_result(login_result)
        self.set_log_action_name("user login", user.username)
        self.save_operation_log(request)

        # 根据操作结果返回异常或者正常内容
        if login_result is False:
            raise BusinessException(StatusCodeEnum.PWD_ERR)

        return {"success": True}


class UserLogout(BaseView):
    """
    用户登出
    """

    def get(self, request):
        login_service.do_logout(request)
        return HttpResponseRedirect('/api/auth/login')


class UserRegister(BaseView):
    """
    用户注册
    """

    def post(self, request):
        data = self.get_request_body(request)
        user = Transform.data_to_object(data, RegisterUser)

        result = register_service.register_user(user)

        self.set_result(result)
        self.set_log_action_name("user register", user.username)
        self.save_operation_log(request)

        if result is False:
            raise BusinessException(StatusCodeEnum.REGISTER_FAILED_ERR)

        return HttpResponseRedirect('/api/auth/login')
