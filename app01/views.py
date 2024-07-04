from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.core.cache import cache

import logging
logger = logging.getLogger("mylogger")
from django.conf import settings

# Create your views here.
 
@cache_page(60 * 15)
def runoob(request):
    context          = {}
    context['hello'] = 'Hello World!'
    logger.info("info log")
    logger.info("defualt log")
    logger.info(settings.MY_HOST)
    logger.info(settings.MY_PORT)
    
    res = cache.set("test", 1235)
    print(res)
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
