from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse('Главная страница')

def one(request):
    return HttpResponse('Cтраница №1')



