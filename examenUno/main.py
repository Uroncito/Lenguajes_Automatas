from gramatica import generar_lote_mezclado, exportar_pruebas_a_csv
from automata import evaluar_automata

SEMILLA = 2026
CANTIDAD_CADENAS = 200

# 1. Generamos el lote mezclado con la semilla fija
lote = generar_lote_mezclado(semilla=SEMILLA, cantidad=CANTIDAD_CADENAS)

# 2. Procesamos e imprimimos los resultados a CSV de 4 columnas
exportar_pruebas_a_csv("reporte_pruebas_200.csv", lote, evaluar_automata)
