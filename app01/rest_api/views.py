from django01.core.base_view import BaseView
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
class MyView(BaseView):
    def get(self, request):
        self.action = "get json"
        self.resource_id_name = "null"

        data = {
            "name": "Vaibhav",
            "age": 20,
            "hobbies": ["Coding", "Art", "Gaming", "Cricket", "Piano"],
        }

        self.result = "success"
        self.save_operation_log(request, self.resource_id_name,
                                self.action, self.result)
        return data
