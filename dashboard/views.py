from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from registroTactil1.models import registro


@login_required
def index(request):
	"""Muestra una lista simple de registros del módulo registroTactil1."""
	registros = registro.objects.all().order_by('-fecha', '-hora')
	return render(request, 'dashboard/index.html', {'registros': registros})
