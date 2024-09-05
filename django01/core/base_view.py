
import datetime
from django.views import View


class BaseView(View):
    def __init__(self):
        self.resource_id_name = None
        self.action = None
        self.result = None
        super().__init__()

    def save_operation_log(self, request, resource_id_name, action, result):
        '''保存审计日志，后期可以保存到db中，或者kafka'''
        print("{},{},{},{},{}".format(resource_id_name,
              action, result, "anyone", datetime.datetime.now()))
