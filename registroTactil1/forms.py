from django import forms 

class rut_form (forms.Form):
    def __init__(self, *args, **kwargs):
        super(rut_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control rut_input text-center'

    rut = forms.CharField(max_length=10,min_length=10,required=True,label='',
                          widget=forms.TextInput(attrs={'placeholder': "Ingrese su RUT"}))
    
class razon_form (forms.Form):
    motivos = [
        ("respuesta de emergencia.","respuesta de emergencia."),
        ("respuesta a solicitud.","respuesta a solicitud."),
        ("visita administrativa.","visita administrativa."),
        ("entrega programada.","entrega programada."),
        ("servicio tecnico.","servicio tecnico."),
        ("representar organizacion.","representar organizacion."),
        ("consulta casual.","consulta casual."),
    ]
    razon = forms.ChoiceField(choices=motivos,
                              widget=forms.RadioSelect(attrs={"class":"form-check"}),
                              required=True,
                              label="")