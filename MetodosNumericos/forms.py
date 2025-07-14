from django import forms

class MetodoForm(forms.Form):
    ECUACIONES_CHOICES = (
        ('gauss', 'eliminacion_gaussiana'),
        ('gauss_jordan', 'gauss_jordan'),
    )
    
    ecuaciones = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
           help_text=
           "Ingrese una ecuación por línea. ""Ejemplo: 2 3 4 representa 2x + 3y = 4"
    )
    metodo = forms.ChoiceField(choices=ECUACIONES_CHOICES)


class BiseccionForm(forms.Form):
    ecuacion = forms.CharField(label="Ecuación", max_length=100)
    a = forms.FloatField(label=" a = Límite inferior")
    b = forms.FloatField(label=" b = Límite superior")
    tolerancia = forms.FloatField(label="e = Tolerancia", initial=0.0001)

#formulario para el métodos de interpolación
from django import forms
from django.core.exceptions import ValidationError

class PuntosForm(forms.Form):
    metodo = forms.ChoiceField(
        choices=[
            ('lagrange', 'Método de Lagrange'),
            ('newton', 'Método de Newton Divididas')
        ],
        label='Método de Interpolación',
        widget=forms.Select(attrs={'class': 'form-control'}))
    
    puntos = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5, 
            'cols': 40,
            'class': 'form-control',
            'placeholder': 'Ejemplo: 1,2 3,4 5,6'
        }),
        label='Puntos (x,y)',
        help_text='Ingrese 2 o más puntos separados por espacios. Formato: x,y')
    
    funcion_real = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ejemplo: sin(x), x**2, exp(x)'
        }),
        label='Función real (opcional)',
        help_text='Expresión matemática para comparación')
    
    rango_grafico = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ejemplo: 0,10'
        }),
        label='Rango para gráfico (opcional)',
        help_text='Valores mínimo,máximo para el gráfico')
    
    def clean_puntos(self):
        datos = self.cleaned_data['puntos']
        try:
            puntos = [tuple(map(float, p.split(','))) for p in datos.split()]
            if len(puntos) < 2:
                raise ValidationError("Se requieren al menos 2 puntos")
            return puntos
        except ValueError:
            raise ValidationError("Formato incorrecto. Use x,y separados por espacios")
    
    def clean_rango_grafico(self):
        rango = self.cleaned_data['rango_grafico']
        if rango:
            try:
                x_min, x_max = map(float, rango.split(','))
                if x_min >= x_max:
                    raise ValidationError("El primer valor debe ser menor que el segundo")
                return (x_min, x_max)
            except ValueError:
                raise ValidationError("Formato incorrecto. Use mínimo,máximo")
        return None