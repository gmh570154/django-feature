from django.http import HttpResponse


def hello(request):
    print("atest")
    return HttpResponse("Hello world !")
