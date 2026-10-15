import random
import csv

# ==========================================
# 1. CATÁLOGOS OFICIALES Y MATRIZ
# ==========================================

DOMINIOS_VALIDOS = [
    "gmail", "outlook", "yahoo", "hotmail", "proton", 
    "icloud", "unam", "ipn", "educacion", "empresa"
]

EXTENSIONES_VALIDAS = [
    "com", "mx", "org", "net", "edu", "gov", "io", "info"
]

PARES_VALIDOS = [
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
]

SET_PARES_VALIDOS = set(PARES_VALIDOS)

# Catálogos para mutaciones
DOMINIOS_INVALIDOS = [
    "facebook", "google", "Gmail", "Outlook", "g_mail", 
    "hotmail123", "yahoo_mx", "protonmail", "empresa_falsa"
]

EXTENSIONES_INVALIDAS = [
    "xyz", "EDU", "COM", "con", "mxx", "net1", 
    "com.mx", "edu.mx", "org.es"
]

# Alfabetos
LETRAS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITOS = "0123456789"
ALFANUMERICO = LETRAS + DIGITOS


# ==========================================
# 2. FUNCIONES AUXILIARES DE SELECCIÓN DE PARES
# ==========================================

def obtener_par_valido():
    return random.choice(PARES_VALIDOS)

def obtener_par_incompatible():
    while True:
        dom = random.choice(DOMINIOS_VALIDOS)
        ext = random.choice(EXTENSIONES_VALIDAS)
        if (dom, ext) not in SET_PARES_VALIDOS:
            return dom, ext

def obtener_par_fuera_de_catalogo():
    opcion = random.choice(["dom_invalido", "ext_invalida", "ambos_invalidos"])
    if opcion == "dom_invalido":
        return random.choice(DOMINIOS_INVALIDOS), random.choice(EXTENSIONES_VALIDAS)
    elif opcion == "ext_invalida":
        return random.choice(DOMINIOS_VALIDOS), random.choice(EXTENSIONES_INVALIDAS)
    else:
        return random.choice(DOMINIOS_INVALIDOS), random.choice(EXTENSIONES_INVALIDAS)


# ==========================================
# 3. GENERADOR DE CORREOS VÁLIDOS
# ==========================================

def generar_usuario_valido():
    longitud_objetivo = random.randint(3, 20)
    usuario = [random.choice(LETRAS)]
    
    while len(usuario) < longitud_objetivo - 1:
        ultimo = usuario[-1]
        opciones = list(ALFANUMERICO)
        if ultimo not in ('_', '.'):
            opciones.append('_')
            opciones.append('.')
        usuario.append(random.choice(opciones))
        
    usuario.append(random.choice(ALFANUMERICO))
    return "".join(usuario)

def generar_correo_valido():
    usuario = generar_usuario_valido()
    dominio, extension = obtener_par_valido()
    return f"{usuario}@{dominio}.{extension}", "Cumple con todas las restricciones del lenguaje"


# ==========================================
# 4. MÓDULO MUTADOR (GENERADOR DE INVÁLIDOS)
# ==========================================

def generar_correo_invalido():
    tipo_mutacion = random.choice([
        "longitud_corta", "longitud_larga", "inicio_invalido", 
        "fin_invalido", "especiales_consecutivos", "sin_arroba", 
        "doble_arroba", "caracter_prohibido", "par_incompatible", "fuera_de_catalogo"
    ])
    
    usuario_base = generar_usuario_valido()
    dom_valido, ext_valida = obtener_par_valido()
    
    if tipo_mutacion == "longitud_corta":
        usr = random.choice(LETRAS) * random.randint(1, 2)
        return f"{usr}@{dom_valido}.{ext_valida}", "Usuario demasiado corto (longitud < 3)"
        
    elif tipo_mutacion == "longitud_larga":
        usr = random.choice(LETRAS) + "".join(random.choices(ALFANUMERICO, k=random.randint(20, 23)))
        return f"{usr}@{dom_valido}.{ext_valida}", "Usuario demasiado largo (longitud > 20)"
        
    elif tipo_mutacion == "inicio_invalido":
        usr = random.choice(DIGITOS + "_.") + usuario_base[1:]
        return f"{usr}@{dom_valido}.{ext_valida}", "El usuario debe comenzar obligatoriamente con una letra"
        
    elif tipo_mutacion == "fin_invalido":
        usr = usuario_base[:-1] + random.choice("_.")
        return f"{usr}@{dom_valido}.{ext_valida}", "El usuario no puede terminar en punto ni guion bajo"
        
    elif tipo_mutacion == "especiales_consecutivos":
        secuencia = random.choice(["..", "__", "._", "_."])
        pos = random.randint(1, len(usuario_base) - 1)
        usr = usuario_base[:pos] + secuencia + usuario_base[pos:]
        return f"{usr}@{dom_valido}.{ext_valida}", "El usuario contiene caracteres especiales consecutivos no permitidos"
        
    elif tipo_mutacion == "sin_arroba":
        return f"{usuario_base}.{dom_valido}.{ext_valida}", "Falta el símbolo separador @"
        
    elif tipo_mutacion == "doble_arroba":
        return f"{usuario_base}@@{dom_valido}.{ext_valida}", "La dirección contiene más de un símbolo @"
        
    elif tipo_mutacion == "caracter_prohibido":
        invalido = random.choice(["#", "$", "%", "ñ", "Á", " "])
        return f"{usuario_base}{invalido}a@{dom_valido}.{ext_valida}", f"Contiene un carácter no autorizado ('{invalido}')"
        
    elif tipo_mutacion == "par_incompatible":
        dom_inc, ext_inc = obtener_par_incompatible()
        return f"{usuario_base}@{dom_inc}.{ext_inc}", f"Combinación (dominio='{dom_inc}', extensión='{ext_inc}') no autorizada por la matriz"
        
    elif tipo_mutacion == "fuera_de_catalogo":
        dom_fc, ext_fc = obtener_par_fuera_de_catalogo()
        return f"{usuario_base}@{dom_fc}.{ext_fc}", f"El dominio ('{dom_fc}') o la extensión ('{ext_fc}') no pertenecen al catálogo autorizado"


# ==========================================
# 5. GENERACIÓN DE LOTE MEZCLADO
# ==========================================

def generar_lote_mezclado(semilla, cantidad=200, proporcion_validos=0.5):
    """
    Inicializa la semilla y genera 'cantidad' de cadenas (válidas e inválidas mezcladas).
    Devuelve una lista de tuplas: [(cadena, es_valido_esperado, razon_original)]
    """
    random.seed(semilla)
    lote = []
    
    for _ in range(cantidad):
        # Decide si crea una cadena válida o una inválida según la proporción
        es_valido = random.random() < proporcion_validos
        
        if es_valido:
            cadena, causa = generar_correo_valido()
            lote.append((cadena, True, causa))
        else:
            cadena, causa = generar_correo_invalido()
            lote.append((cadena, False, causa))
            
    return lote


# ==========================================
# 6. VERIFICADOR INDEPENDIENTE (ORÁCULO)
# ==========================================

def verificador_independiente(cadena):
    """
    Verificador de control desarrollado independientemente de las funciones del AFD.
    Devuelve True si es VÁLIDO o False si es INVÁLIDO.
    """
    if cadena.count('@') != 1:
        return False
    
    usr, dom_ext = cadena.split('@')
    
    # Reglas de Usuario
    if len(usr) < 3 or len(usr) > 20:
        return False
    if usr[0] not in LETRAS or usr[-1] not in ALFANUMERICO:
        return False
        
    for i in range(len(usr)):
        if usr[i] not in ALFANUMERICO and usr[i] not in ('_', '.'):
            return False
        if i > 0 and usr[i-1] in ('_', '.') and usr[i] in ('_', '.'):
            return False
            
    # Reglas de Dominio/Extensión
    partes = dom_ext.split('.')
    if len(partes) != 2:
        return False
        
    return (partes[0], partes[1]) in SET_PARES_VALIDOS


# ==========================================
# 7. EXPORTACIÓN A ARCHIVO CSV (4 COLUMNAS)
# ==========================================

def exportar_pruebas_a_csv(nombre_archivo, lote, funcion_automata):
    """
    Evalúa cada cadena del lote con el AFD y el Verificador Independiente, 
    y genera el archivo .csv con 4 columnas.
    """
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        
        # Encabezados de las 4 columnas
        escritor.writerow([
            "cadena", 
            "resultado_afd", 
            "justificacion_invalido", 
            "verificador_independiente"
        ])
        
        for cadena, es_valido_original, causa_original in lote:
            # 1. Evaluación del Autómata (AFD)
            es_valido_afd, motivo_afd = funcion_automata(cadena)
            res_afd_str = "VÁLIDO" if es_valido_afd else "INVÁLIDO"
            
            # 2. Evaluación del Verificador Independiente
            es_valido_verif = verificador_independiente(cadena)
            res_verif_str = "VÁLIDO" if es_valido_verif else "INVÁLIDO"
            
            # 3. Determinación de la justificación
            # Si el AFD rechaza la cadena, se coloca el motivo del fallo
            justificacion = "Cumple con todas las restricciones" if es_valido_afd else motivo_afd
            
            # Escritura de la fila en el CSV
            escritor.writerow([
                cadena, 
                res_afd_str, 
                justificacion, 
                res_verif_str
            ])
            
    print(f"✓ Archivo CSV creado exitosamente: '{nombre_archivo}'")