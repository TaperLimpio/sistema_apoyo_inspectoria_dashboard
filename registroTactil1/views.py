from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import rut_form, razon_form
from .models import registro
from dashboard.models import persona, TipoPersona


def index(request):

    return render(request, "registroTactil1/index.html")


def home_choice(request):
    """Interfaz simple en la raíz para elegir entre Registro Táctil y Dashboard."""
    return render(request, "registroTactil1/home.html")


def rut(request):
    if request.method == "POST":
        rut_valid = rut_form(request.POST)
        
        if rut_valid.is_valid():
            rut = request.POST.get("rut")
            return redirect("razon",rut)
        else:
            form = rut_form()
    else:
        form = rut_form()
    return render(request, "registroTactil1/rut.html", {"form":form})


def razon(request,rut):
    if request.method == "POST":
        form = razon_form()
        razon = request.POST.get("razon")
        registro_nuevo = registro()
        responsable, nuevo = persona.objects.get_or_create(rut=rut)
        if nuevo:
            responsable.nombre = "NO-REGISTRADO"
            responsable.tipo_persona = TipoPersona.objects.get(id=1)
            responsable.save()
        registro_nuevo.motivo = razon
        registro_nuevo.responsable = responsable
        registro_nuevo.save()
        return redirect("registro_completo")
    else:
        form = razon_form()
    return render(request, "registroTactil1/razon.html", {"form":form})


def registroCom(request):
    return render(request, "registroTactil1/registro_completo.html")

