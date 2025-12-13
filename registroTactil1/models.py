from django.db import models
from dashboard.models import persona
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import generate_qr_id
from dashboard.models import persona as PersonaModel

# Create your models here.
class registro(models.Model):
    motivos = [
        ("respuesta de emergencia.", "respuesta de emergencia."),
        ("respuesta a solucitud.", "respuesta a solucitud."),
        ("visita administrativa.", "visita administrativa."),
        ("entrega programada.", "entrega programada."),
        ("servicio tecnico.", "servicio tecnico."),
        ("representar organizacion.", "representar organizacion."),
        ("consulta casual.", "consulta casual."),
        ("ingreso por QR.", "ingreso por QR."),
    ]
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    motivo = models.CharField(max_length=100, choices=motivos)
    responsable = models.ForeignKey(persona, on_delete=models.PROTECT, default=1)
    qr_id = models.CharField(max_length=50, unique=True, null=True, blank=True)


@receiver(post_save, sender=registro)
def ensure_qr_id(sender, instance, created, **kwargs):
    """Ensure that a registro has a qr_id after it's saved.

    We use update(...) to avoid recursion on save() in the signal.
    """
    if instance.qr_id:
        return
    # If the responsible is an 'interno' (type id == 2), ensure persona has persistent qrcode
    responsable = instance.responsable
    try:
        tipo_id = responsable.tipo_persona.id if responsable and responsable.tipo_persona else None
    except Exception:
        tipo_id = None
    # For internal personas (tipo_persona.id == 2), use/assign persona.qrcode
    if tipo_id == 2 and responsable:
        # if persona qrcode is default or empty, create deterministic token for the person
        current_person_qr = getattr(responsable, 'qrcode', None)
        if not current_person_qr or current_person_qr == "0":
            person_token = generate_qr_id(responsable.id, responsable.rut or "", deterministic=True)
            # save persona with token
            PersonaModel.objects.filter(pk=responsable.pk).update(qrcode=person_token)
            # set registro qr to same token
            registro.objects.filter(pk=instance.pk).update(qr_id=person_token)
        else:
            # persona already has qrcode -> set registro qr to persona's qr
            registro.objects.filter(pk=instance.pk).update(qr_id=current_person_qr)
        return
    # else: generate unique token per registro
    try:
        rut = instance.responsable.rut if instance.responsable else ""
    except Exception:
        rut = ""
    token = generate_qr_id(instance.id, rut)
    registro.objects.filter(pk=instance.pk).update(qr_id=token)