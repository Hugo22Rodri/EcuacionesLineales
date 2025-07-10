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