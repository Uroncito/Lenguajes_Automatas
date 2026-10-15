# ==========================================================
# SCRIPT INTERACTIVO DE EVALUACIÓN DE CORREOS
# ==========================================================

# Importamos únicamente la función de evaluación de nuestro AFD
from automata import evaluar_automata

def probar_correo_interactivo():
    print("==========================================================")
    print("      VALIDADOR INTERACTIVO DE CORREOS ELECTRONICOS       ")
    print("==========================================================")
    print("Escribe una dirección de correo para evaluarla en el AFD.")
    print("Escribe 'salir' o 'exit' para terminar el programa.\n")
    
    while True:
        # 1. Entrada de texto por teclado
        entrada = input("Ingrese un correo: ").strip()
        
        # Opción para finalizar el bucle
        if entrada.lower() in ['salir', 'exit']:
            print("\n¡Programa finalizado! Hasta luego.")
            break
            
        # Validación de entrada vacía
        if not entrada:
            print("No ingresaste ninguna cadena. Intenta de nuevo.\n")
            continue
            
        # 2. Evaluación de la cadena con el Autómata (AFD)
        es_valido, motivo = evaluar_automata(entrada)
        
        # 3. Impresión visual del resultado
        print("-" * 58)
        if es_valido:
            print(f" RESULTADO: VÁLIDO")
            print(f" Detalle:   {motivo}")
        else:
            print(f" RESULTADO: INVÁLIDO")
            print(f" Causa:     {motivo}")
        print("-" * 58 + "\n")

# Punto de entrada principal
if __name__ == "__main__":
    probar_correo_interactivo()