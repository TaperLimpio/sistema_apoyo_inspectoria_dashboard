
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from registroTactil1.models import registro
from datetime import datetime


@login_required
def index(request):
    registros = registro.objects.select_related('responsable').all().order_by('-fecha', '-hora')
    return render(request, 'dashboard/index.html', {'registros': registros})

@login_required
def filtro(request):
    # Construir filtros de búsqueda a partir de parámetros GET.
    rut_buscado = (request.GET.get("rut") or request.GET.get('q') or '').strip()
    # aceptar tanto 'desde'/'hasta' como 'from'/'to' por compatibilidad
    desde = (request.GET.get("desde") or request.GET.get('from') or '').strip()
    hasta = (request.GET.get("hasta") or request.GET.get('to') or '').strip()
    motivo = (request.GET.get('motivo') or '').strip()

    registros = registro.objects.select_related('responsable').all()

    # Filtrar por rut o nombre del responsable si se proporcionó
    if rut_buscado:
        registros = registros.filter(
            Q(responsable__rut__icontains=rut_buscado) | Q(responsable__nombre__icontains=rut_buscado)
        )

    # Intentar parsear fechas (esperamos 'YYYY-MM-DD') y aplicar filtros según lo recibido
    fecha_desde = None
    fecha_hasta = None
    try:
        if desde:
            fecha_desde = datetime.strptime(desde, '%Y-%m-%d').date()
        if hasta:
            fecha_hasta = datetime.strptime(hasta, '%Y-%m-%d').date()
    except Exception:
        # Si el formato es inválido, ignoramos el filtro de fecha
        fecha_desde = None
        fecha_hasta = None

    if fecha_desde and fecha_hasta:
        registros = registros.filter(fecha__range=(fecha_desde, fecha_hasta))
    elif fecha_desde:
        registros = registros.filter(fecha__gte=fecha_desde)
    elif fecha_hasta:
        registros = registros.filter(fecha__lte=fecha_hasta)

    # Filtrar por motivo si se pasó
    if motivo:
        registros = registros.filter(motivo__icontains=motivo)

    registros = registros.order_by('-fecha', '-hora')
    return render(request, "dashboard/filtro.html", {"registros": registros})

@login_required
def persona_form(request):
	return render(request, "dashboard/persona_form.html")
