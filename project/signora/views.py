from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    html = "<html><body></body></html>"
    return HttpResponse(html)

