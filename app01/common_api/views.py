import json

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django01.core.base_view import BaseView


class UserLogin(BaseView):
    def get(self, request):
        '''登录页面'''
        return render(request, 'login.html')

    def post(self, request):
        '''用户登录'''
        json_str = request.body
        json_dict = json.loads(json_str)
        self.action = "user login"
        self.resource_id_name = json_dict.get("user_name", "")

        user_name = json_dict.get("user_name")
        password = json_dict.get("password")
        user = request.session.get("user", False)
        #  未登录的情况下，设置session会话
        if user_name and password and not user:
            user = {
                "username": user_name,
                "nickname": user_name
                # "is_authenticated": True
            }
            request.session["user"] = user
            request.user = user
        self.result = True
        self.save_operation_log(
            request, self.resource_id_name, self.action, self.result)
        return {"success": True}


class UserLogout(BaseView):
    def get(self, request):
        response = HttpResponseRedirect('/web/login')
        if hasattr(request.session, "user"):
            del request.session["user"]
        return response


class UserRegister(BaseView):
    def post(self, request):

        json_str = request.body
        json_dict = json.loads(json_str)
        self.action = "user register"
        self.resource_id_name = json_dict.get("user_name", "")

        user_name = json_dict.get("user_name")
        password = json_dict.get("password")

        response = HttpResponseRedirect('/web/login')
        if user_name and password:
            # todo save register data
            print("register ok")

        self.result = "success"
        self.save_operation_log(request, self.resource_id_name,
                                self.action, self.result)
        return response
