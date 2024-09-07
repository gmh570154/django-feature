import json
from urllib import response
import uuid

from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from django01.core.base_view import BaseView

# Class based view


class UserLogin(View):
    def post(self, request):
        json_str = request.body
        json_dict = json.loads(json_str)
        self.action = "user login"
        self.resource_id_name = json_dict.get("user_name", "")

        user_name = json_dict.get("user_name")
        password = json_dict.get("password")
        # 要设置cookie和session，所以要处理request和response对象
        response = JsonResponse({"success": True})
        user = request.session.get("user", False)
        if user_name and password and not user:
            session_id = uuid.uuid1()
            user = {
                "username": user_name,
                "nickname": "test",
                "sessionid": session_id
            }
            request.user.username = user_name
            # request.user.is_authenticated = True

            print(session_id)
            response.set_cookie("sessionid",
                                session_id, max_age=60)  # domain="www.ganmh.com",
            request.session[settings.SESSION_KEY_PREFIX + user_name] = user
            request.session["user"] = user

            # 语法格式
            request.session.set_expiry(120)

        return response


class UserLogout(BaseView):
    def get(self, request):
        response.session.clear()
        response = HttpResponseRedirect('/web/login/')
        response.delete_cookie('sessionid')
        return response


class UserRegister(BaseView):
    def post(self, request):
        self.action = "user register"
        self.resource_id_name = request.DATA.get("user_name", "")

        user_name = request.DATA.get("user_name")
        password = request.DATA.get("password")
        if user_name and password:
            print("register ok")

        self.result = "success"
        self.save_operation_log(request, self.resource_id_name,
                                self.action, self.result)
        return response
