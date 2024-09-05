from django.views import View

from django01.utils.time_util import exec_time_util


# Create your views here.
# Function based view，使用装饰器功能处理返回json数据
@exec_time_util
def myView(request):
    data = {
        "name": "Vaibhav",
        "age": 20,
        "hobbies": ["Coding", "Art", "Gaming", "Cricket", "Piano"],
    }
    return data


# Class based view
class MyView(View):
    def get(self, request):
        data = {
            "name": "Vaibhav",
            "age": 20,
            "hobbies": ["Coding", "Art", "Gaming", "Cricket", "Piano"],
        }

        return data
