#Integrantes: Nicolas Rosales y Angelo González

#Librerias necesarias
import time
import random
import sys
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple

#Aumentamos el límite de recursión para soportar la profundidad del árbol en n grandes
sys.setrecursionlimit(20000)
SENTINEL = -float('inf') 

#1. Blindaje y validación de entrada
def validar_entrada(st: List[int]) -> bool:
    """Valida que la entrada cumpla con las reglas del problema (lista par de enteros)."""
    try:
        if not isinstance(st, list):
            print("Error: La entrada debe ser una lista.")
            return False
        if len(st) == 0:
            print("Error: La lista está vacía.")
            return False
        if len(st) % 2 != 0:
            print(f"Error: El tamaño {len(st)} no es par (se requiere 2n).")
            return False
        if not all(isinstance(x, int) for x in st):
            print("Error: Todos los elementos deben ser enteros.")
            return False
        return True
    except Exception:
        return False

#2. Estrategia: Arreglos (Matriz)
def solve_torta_array(st: List[int]) -> float:
    if not validar_entrada(st): return 0.0
    
    N = len(st)
    n_pequeno = N // 2
    total_sum = sum(st)
    
    #Inicializamos la tabla de memoización (Matriz N x N+1)
    memo: List[List[float]] = [[SENTINEL] * (N + 1) for _ in range(N)]

    #[O]Objetivo (Original):
    #Calcular el estado inicial: bloque completo que empieza en 0 con largo N
    #El resultado es la diferencia neta óptima (Puntos Profe - Puntos Hermana)
    score_neto = dp_array(0, N, st, memo, N, n_pequeno)
    
    #Recuperamos el puntaje total del profesor usando álgebra simple:
    #Profe = (Total + Neto) / 2
    return (total_sum + score_neto) / 2

def dp_array(i: int, k: int, st: List[int], memo: List[List[float]], N: int, n_pequeno: int) -> float:
    """
    [S]Subproblema: dp(i, k)
    Calcula la máxima puntuación neta garantizada para el jugador actual,
    dado un bloque contiguo de 'k' porciones comenzando en el índice 'i'
    """
    
    #[B]Casos base (Bottom)
    if k == 0: return 0.0               #Bloque vacío -> 0 puntos
    if k == 1: return float(st[i])      #Una porción -> Me la como
    
    #Verificación de Memoización (Evita re-cálculo)
    if memo[i][k] != SENTINEL: return memo[i][k]

    #Identificamos qué porciones están disponibles en este bloque (i, k)
    indices_bloque = {(i + m) % N for m in range(k)}
    movimientos_validos = []
    
    #[T]Tiempo de transición: Iteramos O(N) posibles cortes
    for j in range(N):
        #Regla (c.1): Un ángulo es válido si hay porciones a AMBOS lados de la línea
        lado1 = {(j + m) % N for m in range(1, n_pequeno)}
        lado2 = {(j + n_pequeno + m) % N for m in range(1, n_pequeno)}
        
        #Verificamos intersección: ¿Hay piezas del bloque actual en ambos lados?
        if not indices_bloque.isdisjoint(lado1) and \
           not indices_bloque.isdisjoint(lado2):
            movimientos_validos.append(j)

    #[B]Caso base adicional: "Parar de comer"
    if not movimientos_validos:
        memo[i][k] = 0.0
        return 0.0
        
    mejor_neto = -float('inf')

    #[R]Relación de recurrencia
    #Probamos cada corte válido y aplicamos Minimax
    for j in movimientos_validos:
        #Regla (c.2): Comer semicírculo
        semicirculo = {(j + m) % N for m in range(n_pequeno)}
        
        #Calculamos ganancia inmediata (intersección de lo disponible y el semicírculo)
        piezas_a_comer = indices_bloque.intersection(semicirculo)
        ganancia_actual = sum(st[p] for p in piezas_a_comer)
        
        #Calculamos el estado resultante para el oponente
        piezas_restantes = indices_bloque.difference(piezas_a_comer)
        
        nuevo_i, nuevo_k = 0, 0
        if piezas_restantes:
            nuevo_k = len(piezas_restantes)
            #Buscamos el inicio del nuevo bloque (índice cuyo anterior no está)
            for p in piezas_restantes:
                if (p - 1 + N) % N not in piezas_restantes:
                    nuevo_i = p
                    break
        
        #Llamada Recursiva: ¿Cuánto ganará el oponente en su turno?
        neto_oponente = dp_array(nuevo_i, nuevo_k, st, memo, N, n_pequeno)
        
        #Lógica Minimax: Mi Neto = Lo que gano - Lo que gana el oponente
        mejor_neto = max(mejor_neto, ganancia_actual - neto_oponente)

    #Guardamos y retornamos
    memo[i][k] = mejor_neto
    return mejor_neto

#3. Estrategia: Hash (Diccionario)
def solve_torta_hash(st: List[int]) -> float:
    if not validar_entrada(st): return 0.0
    N = len(st)
    n_pequeno = N // 2
    total_sum = sum(st)
    
    #Inicializamos diccionario vacío
    memo: Dict[Tuple[int, int], float] = {}

    score_neto = dp_hash(0, N, st, memo, N, n_pequeno)
    return (total_sum + score_neto) / 2

def dp_hash(i: int, k: int, st: List[int], memo: Dict[Tuple[int, int], float], N: int, n_pequeno: int) -> float:
    #[S]Subproblema (Misma lógica, distinto almacenamiento)
    
    #[B]Casos base
    if k == 0: return 0.0
    if k == 1: return float(st[i])
    if (i, k) in memo: return memo[(i, k)]

    indices_bloque = {(i + m) % N for m in range(k)}
    movimientos_validos = []
    
    #Validación de cortes
    for j in range(N):
        lado1 = {(j + m) % N for m in range(1, n_pequeno)}
        lado2 = {(j + n_pequeno + m) % N for m in range(1, n_pequeno)}
        
        if not indices_bloque.isdisjoint(lado1) and \
           not indices_bloque.isdisjoint(lado2):
            movimientos_validos.append(j)

    if not movimientos_validos:
        memo[(i, k)] = 0.0
        return 0.0
        
    mejor_neto = -float('inf')

    #[R]Recurrencia
    for j in movimientos_validos:
        semicirculo = {(j + m) % N for m in range(n_pequeno)}
        piezas_a_comer = indices_bloque.intersection(semicirculo)
        ganancia_actual = sum(st[p] for p in piezas_a_comer)
        
        piezas_restantes = indices_bloque.difference(piezas_a_comer)
        
        nuevo_i, nuevo_k = 0, 0
        if piezas_restantes:
            nuevo_k = len(piezas_restantes)
            for p in piezas_restantes:
                if (p - 1 + N) % N not in piezas_restantes:
                    nuevo_i = p
                    break
        
        neto_oponente = dp_hash(nuevo_i, nuevo_k, st, memo, N, n_pequeno)
        mejor_neto = max(mejor_neto, ganancia_actual - neto_oponente)

    memo[(i, k)] = mejor_neto
    return mejor_neto

#4. Experimentos y gráficos
if __name__ == "__main__":
    print("\n" + "="*60)
    print("TAREA 2: FELIZ CUMPLEAÑOS (CODIGO DOCUMENTADO SRTBOT)")
    print("="*60)

    #1. Verificación caso pdf
    st_pdf = [7, 8, 2, 3, 1, 1, 5, 6]
    print(f"\n[1] Verificación PDF. Entrada: {st_pdf}")
    res = solve_torta_array(st_pdf)
    print(f"Resultado: {res}")

    #2. Análisis experimental
    print("\n[2] Generando datos y gráfico...")
    valores_n = [2, 4, 6, 8, 10, 12, 14]
    tiempos_array = []
    tiempos_hash = []
    
    print(f"{'n':<5} {'N':<5} {'Array(s)':<12} {'Hash(s)':<12}")
    print("-" * 40)

    for n_val in valores_n:
        N_val = 2 * n_val
        st = [random.randint(1, 10) for _ in range(N_val)]
        
        #Medir Array
        t0 = time.perf_counter()
        solve_torta_array(st)
        dt_array = time.perf_counter() - t0
        tiempos_array.append(dt_array)
        
        #Medir Hash
        t0 = time.perf_counter()
        solve_torta_hash(st)
        dt_hash = time.perf_counter() - t0
        tiempos_hash.append(dt_hash)
        
        print(f"{n_val:<5} {N_val:<5} {dt_array:<12.5f} {dt_hash:<12.5f}")

    #3. Gráfico
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(valores_n, tiempos_array, marker='o', label='Arreglos (Matriz)', color='blue')
        plt.plot(valores_n, tiempos_hash, marker='s', label='Hash (Dict)', color='red', linestyle='--')
        
        plt.title(r'Comparación de Tiempos: Arreglos vs Hash ($O(n^4)$)')
        plt.xlabel('Valor de n (Semicírculos)')
        plt.ylabel('Tiempo (segundos)')
        plt.legend()
        plt.grid(True)
        
        plt.savefig('grafico_tiempos_final.png')
        print("\n>> Gráfico 'grafico_tiempos_final.png' generado correctamente.")
        plt.show()
    except Exception as e:
        print(f"\nNo se pudo generar el gráfico: {e}")
