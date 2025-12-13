from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from .forms import rut_form, razon_form
from .models import registro
from dashboard.models import persona, TipoPersona
from .utils import generate_qr_id
import qrcode
from io import BytesIO
from django.http import HttpResponse


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
        # refresh to pick up auto-generated qr_id from post_save signal
        registro_nuevo.refresh_from_db()
        qr_id = registro_nuevo.qr_id
        if not qr_id:
            # fallback to ensure there's always a qr_id; can be rare
            qr_id = generate_qr_id(registro_nuevo.id, responsable.rut if responsable else "")
            registro_nuevo.qr_id = qr_id
            registro_nuevo.save()
        # Redirect to page that can show the QR id (optional: used by client to show QR)
        return redirect(f"/registro_completo?qr={qr_id}")
    else:
        form = razon_form()
    return render(request, "registroTactil1/razon.html", {"form":form})


def registroCom(request):
    qr = request.GET.get('qr')
    return render(request, "registroTactil1/registro_completo.html", {"qr": qr})


def qr_image(request, token: str):
    if not token:
        return HttpResponse(status=404)
    try:
        qr = qrcode.QRCode(box_size=6, border=2)
        qr.add_data(token)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        response = HttpResponse(buf.getvalue(), content_type="image/png")
        if request.GET.get('download') in ('1', 'true', 'yes'):
            filename = f"qr_{token[:8]}.png"
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
        else:
            response["Content-Disposition"] = 'inline'
        return response
    except Exception as e:
        return HttpResponse(status=500, content=str(e))


def escanear_qr(request):
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'status': 'error', 'mensaje': 'JSON inválido'}, status=400)

        qrobtenido = (data.get('qrobtenido') or '').strip()
        if not qrobtenido:
            return JsonResponse({'status': 'error', 'mensaje': 'No se obtuvo QR'}, status=400)

        # Try to resolve by persona.qrcode first, then by rut
        responsable = persona.objects.filter(qrcode=qrobtenido).first()
        if not responsable:
            responsable = persona.objects.filter(rut=qrobtenido).first()

        if not responsable:
            return JsonResponse({'status': 'not_found', 'mensaje': 'Persona no encontrada'}, status=404)

        # Create registro automatically with motivo 'ingreso por QR.'
        try:
            nuevo_reg = registro(motivo='ingreso por QR.', responsable=responsable)
            nuevo_reg.save()
            nuevo_reg.refresh_from_db()
            qr_url = reverse('qr_image', args=[nuevo_reg.qr_id]) if nuevo_reg.qr_id else None
            return JsonResponse({
                'status': 'success',
                'mensaje': 'Registro creado',
                'persona': responsable.nombre,
                'registro_id': nuevo_reg.id,
                'qr_id': nuevo_reg.qr_id,
                'qr_url': request.build_absolute_uri(qr_url) if qr_url else None,
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'mensaje': f'No se pudo crear el registro: {e}'}, status=500)

    # GET: renderizar la plantilla normal
    return render(request, "registroTactil1/escanear_qr.html")
