from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("rut/", views.rut, name="rut"),
    path("escanear_qr/", views.escanear_qr, name="escanear_qr"),
    path("razon/<str:rut>", views.razon, name="razon"),
    path("registro_completo/", views.registroCom, name="registro_completo"),
    path("qr/<str:token>/", views.qr_image, name="qr_image"),
]
