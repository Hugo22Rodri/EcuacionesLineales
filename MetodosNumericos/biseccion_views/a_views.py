from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from MetodosNumericos.utils.calculations import biseccion  
from MetodosNumericos.serializers import BiseccionSerializer  

# Define una vista basada en clases para manejar solicitudes relacionadas con el método de bisección
class BiseccionAPI(APIView):
    # Maneja solicitudes POST
    def post(self, request):
        try:
            # Serializa y valida los datos de la solicitud
            serializer = BiseccionSerializer(data=request.data)
            if serializer.is_valid():
                # Llama a la función de bisección con los datos validados
                resultado = biseccion(serializer.validated_data)

                # Verifica si hubo un error en el cálculo
                if "error" in resultado:
                    # Devuelve una respuesta con el error y un código de estado 400
                    return Response({"error": resultado["error"]}, status=status.HTTP_400_BAD_REQUEST)

                # Extrae los pasos y la raíz del resultado
                pasos = resultado["pasos"]
                raiz = resultado["raiz"]

                # Devuelve una respuesta exitosa con la raíz y los pasos
                return Response({"raiz": raiz, "pasos": pasos}, status=status.HTTP_200_OK)

            # Si los datos no son válidos, devuelve los errores de validación
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Maneja excepciones inesperadas y devuelve un error 500
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)