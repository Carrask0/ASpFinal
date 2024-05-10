from django import forms
from .models import Libro, Biblioteca

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = '__all__'  # Include all fields from the Libro model

# forms.py
from django import forms
from .models import Biblioteca

class BibliotecaForm(forms.ModelForm):
    # Define custom form fields for hours and date
    horario_apertura = forms.TimeField(input_formats=['%H:%M'], widget=forms.TimeInput(attrs={'type': 'time'}))
    horario_cierre = forms.TimeField(input_formats=['%H:%M'], widget=forms.TimeInput(attrs={'type': 'time'}))
    fecha_fundacion = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Biblioteca
        fields = ['nombre', 'direccion', 'ciudad', 'horario_apertura', 'horario_cierre', 'fecha_fundacion', 'normas']

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if not direccion.endswith('0') and not direccion.endswith('1') and not direccion.endswith('2') and not direccion.endswith('3') and not direccion.endswith('4') and not direccion.endswith('5') and not direccion.endswith('6') and not direccion.endswith('7') and not direccion.endswith('8') and not direccion.endswith('9'):
            raise forms.ValidationError("La dirección debe contener un número al final.")
        return direccion

