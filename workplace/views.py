from django.shortcuts import render, redirect
from django.http import HttpResponse


# Create your views here.
def response(request):
    return HttpResponse('response')

def redir(request):
    return redirect('/workplace/red/')


def red(request):
    return HttpResponse('Привет, redirect!')
