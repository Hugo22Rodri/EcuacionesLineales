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