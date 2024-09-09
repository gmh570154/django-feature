from django.urls import path

from . import views
from app01.rest_api import views as rest_view
from app01.common_api import views as common_view

urlpatterns = [
    path('runoob/', views.runoob, name="runoob"),

    path('function', rest_view.myView, name="function_view1"),
    path('class', rest_view.MyView.as_view(), name="view1"),
    # 登录start
    path('login', common_view.UserLogin.as_view(), name="login"),
    path('logout', common_view.UserLogout.as_view(), name="logout"),
    path('register', common_view.UserRegister.as_view(), name="register"),
    # 登录end
]
