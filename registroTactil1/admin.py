from django.contrib import admin

from .models import registro


class RegistroAdmin(admin.ModelAdmin):
    list_display = ("id", "responsable", "motivo", "fecha", "hora", "qr_id")
    search_fields = ("responsable__rut", "qr_id", "responsable__nombre")

# Register your models here.
admin.site.register(registro, RegistroAdmin)