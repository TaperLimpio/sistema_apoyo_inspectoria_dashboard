from django.contrib import admin
from .models import registro

class RegistroAdmin(admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(registro, RegistroAdmin)