from django.views import View

from django01.utils.response_util import json_util


# Create your views here.
# Function based view，使用装饰器功能处理返回json数据
@json_util
def myView(request):
    data = "test"
    # data = {
    #     "name": "Vaibhav",
    #     "age": 20,
    #     "hobbies": ["Coding", "Art", "Gaming", "Cricket", "Piano"],
    # }
    return data


# Class based view
class MyView(View):
    @json_util
    def get(self, request):
        data = {
            "name": "Vaibhav",
            "age": 20,
            "hobbies": ["Coding", "Art", "Gaming", "Cricket", "Piano"],
        }

        return data
