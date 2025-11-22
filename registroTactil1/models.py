from django.db import models
from dashboard.models import persona

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
    ]
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    motivo = models.CharField(max_length=100, choices=motivos)
    responsable = models.ForeignKey(persona, on_delete=models.PROTECT, default=1)