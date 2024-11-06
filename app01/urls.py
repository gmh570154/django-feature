from django.urls import path

from . import views
from app01.api.rest_api import views as rest_view
from app01.api.common_api.login import views as login_view
from app01.api.common_api.token import jwt_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    # test api
    path('runoob/', views.runoob, name="runoob"),
    path('function', rest_view.myView, name="function_view1"),
    path('class', rest_view.MyView.as_view(), name="view1"),

    # login api
    path('auth/login', login_view.UserLogin.as_view(), name="login"),
    path('auth/logout', login_view.UserLogout.as_view(), name="logout"),
    path('auth/register', login_view.UserRegister.as_view(), name="register"),

    # jwt token api
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # jwt token test
    path('token/test/', jwt_token.JwtView.as_view(), name='jwt_view'),
]
