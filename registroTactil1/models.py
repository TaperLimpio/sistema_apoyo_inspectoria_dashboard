from django.db import models


# Create your models here.
class registro_externo(models.Model):
    motivos = [
        ("respuesta de emergencia.", "1"),
        ("respuesta a solucitud.", "2"),
        ("visita administrativa.", "3"),
        ("entrega programada.", "4"),
        ("servicio tecnico.", "5"),
        ("representar organizacion.", "6"),
        ("consulta casual.", "7"),
    ]
    fecha = models.DateField()
    hora = models.TimeField()
    rut = models.CharField(max_length=10)
    motivo = models.CharField(max_length=100, choices=motivos)
