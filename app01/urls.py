from django.urls import path
 
from . import views
from app01.rest_api import views as rest_view

urlpatterns = [
    path('runoob/', views.runoob, name="runoob"),

    path('function1', rest_view.myView, name="function_view1"),
    path('class1', rest_view.MyView.as_view(), name="view1"),
]
