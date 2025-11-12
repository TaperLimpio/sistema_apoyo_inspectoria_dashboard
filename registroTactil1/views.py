from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "registroTactil1/index.html")


def rut(request):
    return render(request, "registroTactil1/rut.html")


def razon(request):
    return render(request, "registroTactil1/razon.html")


def registroCom(request):
    return render(request, "registroTactil1/registro_completo.html")


# Create your views here.
