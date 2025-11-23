from django import forms
from .models import persona, TipoPersona

class PersonaForm(forms.ModelForm):
    class Meta:
        model = persona
        fields = ["nombre", "rut", "fono", "tipo_persona"]

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control text-center'
        # El queryset debe devolver instancias de TipoPersona, no diccionarios
        self.fields["tipo_persona"].queryset = TipoPersona.objects.all()
        # Mejorar apariencia del select
        self.fields["tipo_persona"].widget.attrs.update({'class': 'form-select text-center'})
        self.fields["fono"].required=False