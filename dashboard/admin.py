from django.contrib import admin
from .models import persona, TipoPersona

class PersonaAdmin(admin.ModelAdmin):
    pass

class TipoPersonaAdmin(admin.ModelAdmin):
    pass

admin.site.register(persona, PersonaAdmin)
admin.site.register(TipoPersona, TipoPersonaAdmin)