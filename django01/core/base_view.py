
import datetime
from django.views import View
import json


class BaseView(View):
    def __init__(self):
        self.resource_id_name = None
        self.action = None
        self.result = False
        self.username = "AnonymousUser"
        super().__init__()

    def get_request_body(self, request):
        return json.loads(request.body)

    def set_result(self, status):
        self.result = "success" if status else "failed"

    def set_log_action_name(self, action, resource_id_name, result=None):
        self.action = action
        self.resource_id_name = resource_id_name
        if result is not None:
            self.result = result

    def save_operation_log(self, request):
        if hasattr(request, "user") and not request.user.is_anonymous:
            self.username = request.user.username

        '''保存审计日志，后期可以保存到db中，或者kafka'''
        print("{},{},{},{},{}".format(self.username,
                                      self.action, self.resource_id_name,
                                      self.result, datetime.datetime.now()))
