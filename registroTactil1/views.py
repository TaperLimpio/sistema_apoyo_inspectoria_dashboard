from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import rut_form, razon_form
from .models import registro


def index(request):

    return render(request, "registroTactil1/index.html")


def rut(request):
    if request.method == "POST":
        rut = request.POST.get("rut")
        print(rut)
        return redirect("razon",rut)
    else:
        form = rut_form()
    return render(request, "registroTactil1/rut.html", {"form":form})


def razon(request,rut):
    if request.method == "POST":
        form = razon_form()
        razon = request.POST.get("razon")
        registro_nuevo = registro()
        registro_nuevo.rut = rut
        registro_nuevo.motivo = razon
        registro_nuevo.save()
        return redirect("registro_completo")
    else:
        form = razon_form()
    return render(request, "registroTactil1/razon.html", {"form":form})


def registroCom(request):
    return render(request, "registroTactil1/registro_completo.html")

