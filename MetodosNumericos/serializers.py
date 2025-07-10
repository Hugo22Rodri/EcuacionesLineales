from rest_framework import serializers

class BiseccionSerializer(serializers.Serializer):
    ecuacion = serializers.CharField(max_length=100)
    a = serializers.FloatField()
    b = serializers.FloatField()
    tolerancia = serializers.FloatField(default=0.0001)

    def validate(self, data):
        """ Validaciones adicionales para evitar errores en la API """
        if data["a"] >= data["b"]:
            raise serializers.ValidationError("El límite inferior 'a' debe ser menor que el superior 'b'.")
        
        if data["tolerancia"] <= 0:
            raise serializers.ValidationError("La tolerancia debe ser un número positivo.")
        
        return data