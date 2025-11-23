from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='dashboard_index'),
    path('busqueda_filtro/', views.filtro, name="busqueda_filtro"),
    path('persona_ingreso/', views.persona_form, name="persona_ingreso")
]