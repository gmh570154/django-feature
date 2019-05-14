from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers

from .models import ViewLog


def add_view_log(request):  #  调用接口记录访问日志
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
    ViewLog.objects.create(hostname=ip)

    return render(request, 'webAPI/index.html', {
        'hostname': ip,
        'count': ViewLog.objects.count()
    })

def get_all_view_logs(request):  # 获取所有的访问日志的记录，返回json数据格式
    result = ViewLog.objects.all()
    json_data = serializers.serialize("json", result, ensure_ascii=False)
    return HttpResponse(json_data, content_type='application/json; charset=utf-8')
