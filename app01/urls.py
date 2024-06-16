from django.urls import path
 
from . import views

urlpatterns = [
    path('runoob/', views.runoob, name="runoob"),
]