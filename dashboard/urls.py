from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='dashboard_index'),
    path('busqueda_filtro/', views.filtro, name="busqueda_filtro"),
    path('personas/', views.persona_view, name='personas_view'),
    path('persona_ingreso/', views.persona_form, name="persona_ingreso"),
    path('persona/<int:pk>/edit/', views.persona_edit, name='persona_edit'),
]