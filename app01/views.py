from django.shortcuts import render

import logging
logger = logging.getLogger("mylogger")
# Create your views here.
 
def runoob(request):
    context          = {}
    context['hello'] = 'Hello World!'
    logger.info("info log")
    logging.info("defualt log")
    return render(request, 'runoob.html', context)