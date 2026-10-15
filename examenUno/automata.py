# ==========================================
# AUTOMATA FINITO DETERMINISTA (AFD)
# ==========================================

# Pares autorizados según la matriz de compatibilidad (Sección 3.4)
PARES_MATRIZ_VALIDOS = {
    ("gmail", "com"), ("gmail", "mx"),
    ("outlook", "com"), ("outlook", "net"),
    ("yahoo", "com"), ("yahoo", "mx"),
    ("hotmail", "com"),
    ("proton", "com"), ("proton", "net"), ("proton", "io"),
    ("icloud", "com"),
    ("unam", "mx"), ("unam", "edu"),
    ("ipn", "mx"), ("ipn", "edu"),
    ("educacion", "mx"), ("educacion", "org"), ("educacion", "edu"), ("educacion", "gov"),
    ("empresa", "com"), ("empresa", "org"), ("empresa", "net"), ("empresa", "info")
}

LETRAS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
DIGITOS = set("0123456789")
ALFANUMERICO = LETRAS | DIGITOS

def evaluar_automata(cadena):
    """
    Simula el recorrido del AFD estado por estado.
    Devuelve una tupla: (es_valido: bool, causa_de_rechazo: str)
    """
    # 1. Verificación global: exactamente una @ y sin espacios/acentos prohibidos
    if cadena.count('@') != 1:
        return False, "El correo debe contener exactamente un símbolo @"
        
    usuario, dominio_extension = cadena.split('@')
    
    # 2. Evaluación de la fase de Nombre de Usuario por estados
    # Regla: Longitud de 3 a 20 caracteres
    if len(usuario) < 3 or len(usuario) > 20:
        return False, f"Longitud de usuario fuera de rango ({len(usuario)} caracteres, esperado 3-20)"
        
    # Estado inicial q0: Debe empezar obligatoriamente con letra
    if usuario[0] not in LETRAS:
        return False, "El usuario debe comenzar obligatoriamente con una letra"
        
    # Estado final del usuario: Debe terminar obligatoriamente con letra o dígito
    if usuario[-1] not in ALFANUMERICO:
        return False, "El usuario debe terminar con letra o dígito"
        
    # Recorrido de estados para detectar caracteres consecutivos prohibidos (.., __, ._, _.)
    # y verificar alfabeto permitido
    for i in range(len(usuario)):
        caracter = usuario[i]
        if caracter not in ALFANUMERICO and caracter not in ('_', '.'):
            return False, f"Carácter no autorizado en usuario ('{caracter}')"
            
        if i > 0:
            anterior = usuario[i-1]
            if anterior in ('_', '.') and caracter in ('_', '.'):
                return False, f"Secuencia de caracteres especiales consecutivos no permitida ('{anterior}{caracter}')"

    # 3. Evaluación de la fase de Dominio y Extensión (Matriz de Compatibilidad)
    if '.' not in dominio_extension:
        return False, "Falta el punto separador entre el dominio y la extensión"
        
    # Separación estricta de dominio y extensión
    partes = dominio_extension.split('.')
    if len(partes) != 2:
        return False, "Estructura de dominio/extensión no válida (no se permiten extensiones compuestas ni subdominios)"
        
    dominio, extension = partes[0], partes[1]
    
    # Verificación en la matriz de compatibilidad
    par = (dominio, extension)
    if par not in PARES_MATRIZ_VALIDOS:
        return False, f"La combinación dominio='{dominio}' con extensión='{extension}' no está autorizada por la matriz"
        
    # Si superó todos los estados y restricciones
    return True, "Cumple con todas las restricciones del lenguaje"


# --- PRUEBA RÁPIDA DEL AUTOMATA ---
if __name__ == "__main__":
    casos_prueba = [
        "ana123@gmail.com",       # Válido
        "a_b9@proton.io",         # Válido
        "ana@gmail.edu",          # Inválido (Matriz)
        "ana..lopez@gmail.com",   # Inválido (Especiales consecutivos)
        "ab@unam.mx"              # Inválido (Usuario corto)
    ]
    
    print("--- RESULTADOS DE EVALUACIÓN DEL AFD ---")
    for correo in casos_prueba:
        valido, motivo = evaluar_automata(correo)
        estado = "VÁLIDO" if valido else "INVÁLIDO"
        print(f"Cadena: {correo:<25} | AFD: {estado:<8} | Motivo: {motivo}")