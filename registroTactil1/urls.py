from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("rut/", views.rut, name="rut"),
    path("razon/", views.razon, name="razon"),
    path("registro_completo/", views.registroCom, name="registro_completo"),
]
