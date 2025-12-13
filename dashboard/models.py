from django.db import models

class TipoPersona(models.Model):
    tipo_persona = models.CharField(max_length=15)

# Create your models here.
class persona(models.Model):
    nombre = models.CharField(max_length=40, null=False)
    fono = models.CharField(max_length=14, blank=True)
    rut = models.CharField(max_length=10,default="99999999-K")
    tipo_persona = models.ForeignKey(TipoPersona, on_delete=models.PROTECT, default=1)
    qrcode = models.CharField(max_length=50, default="0")

