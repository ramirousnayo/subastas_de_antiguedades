from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import Subasta, Oferta

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class SubastaForm(forms.ModelForm):
    class Meta:
        model = Subasta
        fields = ['titulo', 'descripcion', 'precio_base', 'fecha_cierre', 'categoria', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Reloj de bolsillo siglo XIX'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe el estado, año, historia...'}),
            'precio_base': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'fecha_cierre': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_fecha_cierre(self):
        fecha_cierre = self.cleaned_data.get('fecha_cierre')
        if fecha_cierre and fecha_cierre <= timezone.now():
            raise forms.ValidationError("La fecha de cierre no puede estar en el pasado.")
        return fecha_cierre


class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ['monto']
        widgets = {
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Monto de tu oferta',
                'step': '0.01'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.subasta = kwargs.pop('subasta', None)
        super().__init__(*args, **kwargs)

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if not self.subasta:
            return monto

        # 1. Validar que la subasta esté activa y no haya cerrado
        if self.subasta.estado != 'ACTIVA' or self.subasta.fecha_cierre <= timezone.now():
            raise forms.ValidationError("Esta subasta ya no acepta ofertas.")

        oferta_maxima = self.subasta.obtener_oferta_mas_alta()

        if oferta_maxima:
            # 2. Debe ser estrictamente mayor a la oferta más alta
            if monto <= oferta_maxima.monto:
                raise forms.ValidationError(f"Tu oferta debe ser mayor a la oferta actual (${oferta_maxima.monto}).")
        else:
            # 3. Si es la primera, debe ser igual o mayor al precio base
            if monto < self.subasta.precio_base:
                raise forms.ValidationError(f"Tu oferta debe ser al menos igual al precio base (${self.subasta.precio_base}).")

        return monto
