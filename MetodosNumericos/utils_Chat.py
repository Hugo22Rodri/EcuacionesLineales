# utils_Chat.py
from django.conf import settings
from openai import OpenAI

# Inicializa el cliente de OpenAI usando la clave API definida en la configuración de Django
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# =====================
# Formateo de pasos para IA
# =====================
def formatear_steps_para_ia(pasos):
    """
    Convierte una lista de matrices aumentadas (pasos de resolución) en un formato
    de texto legible para humanos y para IA.
    Parámetros:
        pasos: Lista de matrices (listas de listas) donde cada matriz representa
               un paso en la resolución de un sistema de ecuaciones.
    Retorna:
        Lista de strings formateados, uno por cada paso de la resolución.
    """
    pasos_legibles = []
    for idx, paso in enumerate(pasos):
        matriz_texto = []
        for fila in paso:
            # Formatea los coeficientes y el término independiente de cada fila
            coeficientes = [f"{round(num, 2):7.2f}" for num in fila[:-1]]
            independiente = f"{round(fila[-1], 2):7.2f}"
            fila_texto = "[ " + " ".join(coeficientes) + " |" + independiente + " ]"
            matriz_texto.append(fila_texto)
        # Construye el texto para cada paso, incluyendo el número de paso y la matriz
        paso_texto = f"🔹 Paso {idx + 1}\n\nMatriz aumentada:\n" + "\n".join(matriz_texto)
        pasos_legibles.append(paso_texto)
    return pasos_legibles

# =====================
# Solicitud de explicación a OpenAI
# =====================
def get_explanation_from_openai(method_name, steps_list):
    """
    Llama a OpenAI para obtener una explicación en lenguaje natural de los pasos dados.
    - method_name: nombre del método ("Gauss", "Gauss-Jordan", etc.)
    - steps_list: lista de strings ya formateadas (una por paso)
    """
    # Une todos los pasos en un solo bloque de texto
    steps_text = "\n\n".join(steps_list)

    # Prompt adaptado con formato amigable para estudiantes
    prompt = (
        f"Eres un tutor de matemáticas para estudiantes de secundaria. "
        f"Explica paso a paso, en lenguaje sencillo, cómo se resolvió el sistema de ecuaciones "
        f"usando el método de {method_name}. No uses notación LaTeX ni símbolos técnicos complicados. "
        f"Para cada paso muestra primero la matriz aumentada en formato visual, como en este ejemplo:\n\n"
        f"🔹 Paso 1\n\n"
        f"Matriz aumentada:\n"
        f"[   2.00   3.00  -1.00 |   5.00 ]\n"
        f"[   0.00   1.00   4.00 |   2.00 ]\n"
        f"[   0.00   0.00   1.00 |   3.00 ]\n\n"
        f"Luego de mostrar la matriz, explica con palabras simples qué se hizo en ese paso.\n\n"
        f"Aquí están los pasos de la matriz aumentada:\n\n{steps_text}"
    )

    try:
        # Realiza la solicitud a la API de OpenAI para obtener la explicación
        # Solicita a la API de OpenAI una explicación paso a paso usando el modelo GPT-3.5 Turbo.
        # Se envía un mensaje de sistema para definir el rol de la IA y un mensaje de usuario con el prompt generado.
        # 'temperature' controla la creatividad de la respuesta (0.7 es moderado).
        # 'max_tokens' limita la longitud máxima de la respuesta generada.
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "Eres un tutor de álgebra lineal paciente y didáctico."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        # Devuelve la explicación generada por la IA
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Manejo de errores en caso de problemas de conexión o respuesta
        return f"❌ Error al conectar con OpenAI: {str(e)}"
