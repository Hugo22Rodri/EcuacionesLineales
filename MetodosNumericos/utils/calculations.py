import sympy as sp

def biseccion(datos):
    try:
        x = sp.Symbol("x")
        f_simbolica = sp.sympify(datos["ecuacion"])
        f = sp.lambdify(x, f_simbolica, "numpy")  # Función numérica
        a = float(datos["a"])
        b = float(datos["b"])
        tol = float(datos["tolerancia"])

        # Verificar si a o b son raíces
        fa, fb = f(a), f(b)
        if abs(fa) < tol:
            return {"raiz": a, "pasos": []}
        if abs(fb) < tol:
            return {"raiz": b, "pasos": []}
        if fa * fb > 0:
            return {"error": "Intervalo inválido: no hay cambio de signo."}

        pasos = []
        while abs(b - a) > tol:
            c = (a + b) / 2
            fc = f(c)
            pasos.append((a, b, c, fc))

            # Verificar si c es raíz
            if abs(fc) < tol:
                return {"raiz": c, "pasos": pasos}

            # Actualizar intervalo
            if fa * fc < 0:
                b, fb = c, fc
            else:
                a, fa = c, fc

        return {"raiz": (a + b) / 2, "pasos": pasos}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}