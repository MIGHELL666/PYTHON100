"""
Proyecto 45: Resolver sistema de ecuaciones lineales
"""

def resolver_2x2(a, b, c, d, e, f):
    """
    Resuelve sistema 2x2:
    ax + by = e
    cx + dy = f
    """
    # Calcular determinante principal
    det_principal = a * d - b * c
    
    if det_principal == 0:
        return None, "Sistema sin solución única (determinante = 0)"
    
    # Regla de Cramer
    det_x = e * d - b * f
    det_y = a * f - e * c
    
    x = det_x / det_principal
    y = det_y / det_principal
    
    pasos = [
        f"Sistema: {a}x + {b}y = {e}",
        f"         {c}x + {d}y = {f}",
        f"",
        f"Determinante principal: |{a} {b}| = {a}×{d} - {b}×{c} = {det_principal}",
        f"                        |{c} {d}|",
        f"",
        f"Determinante x: |{e} {b}| = {e}×{d} - {b}×{f} = {det_x}",
        f"                |{f} {d}|",
        f"",
        f"Determinante y: |{a} {e}| = {a}×{f} - {e}×{c} = {det_y}",
        f"                |{c} {f}|",
        f"",
        f"Solución: x = {det_x}/{det_principal} = {x}",
        f"          y = {det_y}/{det_principal} = {y}"
    ]
    
    return (x, y), pasos

def resolver_3x3(coeficientes, terminos):
    """
    Resuelve sistema 3x3 usando regla de Cramer
    coeficientes: matriz 3x3 de coeficientes
    terminos: vector de términos independientes
    """
    # Calcular determinante principal
    det_principal = determinante_3x3_simple(coeficientes)
    
    if abs(det_principal) < 1e-
