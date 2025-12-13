
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from registroTactil1.models import registro
from .forms import PersonaForm
from registroTactil1.utils import generate_qr_id
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import persona


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

def persona_view(request,pk):
    data = get_object_or_404(persona,pk = pk)
    return render(request, "dashboard/persona_view.html", {"data": data})

@login_required
def persona_form(request):
    if request.method == "POST":
        form = PersonaForm(request.POST)
        if form.is_valid():
            persona_obj = form.save()
            # If this persona is internal (tipo_persona.id == 2) and no qrcode assigned, assign a deterministic qrcode
            try:
                tipo_id = persona_obj.tipo_persona.id if persona_obj.tipo_persona else None
            except Exception:
                tipo_id = None
            if tipo_id == 2:
                current_qr = getattr(persona_obj, 'qrcode', None)
                if not current_qr or current_qr == "0":
                    token = generate_qr_id(persona_obj.id, persona_obj.rut or "", deterministic=True)
                    persona_obj.qrcode = token
                    persona_obj.save()
            return redirect('dashboard_index')
    else:
        rut_prefill = request.GET.get('rut')
        if rut_prefill:
            form = PersonaForm(initial={'rut': rut_prefill})
        else:
            form = PersonaForm()
    return render(request, "dashboard/persona_form.html", {"form": form})


@login_required
def persona_edit(request, pk):
    p = get_object_or_404(persona, pk=pk)
    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=p)
        if form.is_valid():
            persona_obj = form.save()
            # If persona is internal and missing qrcode, add deterministic qrcode
            try:
                tipo_id = persona_obj.tipo_persona.id if persona_obj.tipo_persona else None
            except Exception:
                tipo_id = None
            if tipo_id == 2:
                current_qr = getattr(persona_obj, 'qrcode', None)
                if not current_qr or current_qr == "0":
                    token = generate_qr_id(persona_obj.id, persona_obj.rut or "", deterministic=True)
                    persona_obj.qrcode = token
                    persona_obj.save()
            return redirect('personas_view')
    else:
        form = PersonaForm(instance=p)
    return render(request, 'dashboard/persona_edit.html', {'form': form, 'persona': p})

@login_required
def persona_view(request):
    registros = registro.objects.select_related('responsable').all().order_by('-fecha', '-hora')
    personas_recientes = []
    seen = set()
    limit = 6
    for r in registros:
        resp = r.responsable
        if resp and resp.id not in seen:
            personas_recientes.append(resp)
            seen.add(resp.id)
        if len(personas_recientes) >= limit:
            break
    personas_internos = persona.objects.filter(tipo_persona = 2)
    personas_externas = persona.objects.filter(tipo_persona = 1)
    return render(request, "dashboard/personas.html", {
        "personas_recientes": personas_recientes,
        "personas_internos": personas_internos,
        "personas_externas": personas_externas,
    })
