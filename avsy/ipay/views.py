from django.http.response import Http404, HttpResponseNotFound
from django.shortcuts import render

def login(request):
    return render(request, 'login.html')
