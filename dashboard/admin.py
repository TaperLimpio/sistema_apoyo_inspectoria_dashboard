from django.contrib import admin
from .models import persona, TipoPersona

class PersonaAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','rut','tipo_persona','qrcode')
    search_fields = ('rut','nombre','qrcode')

class TipoPersonaAdmin(admin.ModelAdmin):
    pass

admin.site.register(persona, PersonaAdmin)
admin.site.register(TipoPersona, TipoPersonaAdmin)