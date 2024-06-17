from django.shortcuts import render

import logging
logger = logging.getLogger("mylogger")
from django.conf import settings

# Create your views here.
 
def runoob(request):
    context          = {}
    context['hello'] = 'Hello World!'
    logger.info("info log")
    logger.info("defualt log")
    logger.info(settings.MY_HOST)
    logger.info(settings.MY_PORT)
    return render(request, 'runoob.html', context)

def page_not_found(request,exception):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})  #404.html html页面
    response.status_code = 404
    return response

def page_error(request,exception):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})  #404.html html页面
    response.status_code = 500
    return response
