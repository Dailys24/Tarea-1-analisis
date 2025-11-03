import time
import random
from typing import List, Dict, Set, Tuple

# Valor centinela para memoización (un valor no válido)
SENTINEL = -float('inf') 

# ---
# Implementación 1: Memoización con Arreglos (Listas)
# Requerida por la tarea
# ---

def solve_torta_array(st: List[int]) -> float:
    """
    Resuelve el problema de la torta usando Programación Dinámica
    con memoización basada en Arreglos (Listas de Listas).
    Esta es la primera función requerida para la implementación.
    """
    N = len(st)
    if N == 0:
        return 0.0
    
    # n es la cantidad de porciones en un semicírculo
    n_pequeno = N // 2
    total_sum = sum(st)
    
    # memo[i][k] almacena el resultado de dp(i, k)
    # Tamaño: N * (N+1)
    memo: List[List[float]] = [[SENTINEL] * (N + 1) for _ in range(N)]

    # El problema original es el bloque completo (índice 0, largo N)
    net_score = dp_array(0, N, st, memo, N, n_pequeno)
    
    # Puntuación Neta = (Score Profesor) - (Score Hermana)
    # Suma Total = (Score Profesor) + (Score Hermana)
    # Score Profesor = (Neta + Total) / 2
    return (total_sum + net_score) / 2

def dp_array(i: int, k: int, st: List[int], memo: List[List[float]], N: int, n_pequeno: int) -> float:
    """
    Función recursiva (subproblema) para la memoización con arreglo.
    Calcula la max puntuación neta del bloque contiguo (i, k).
    i = índice de inicio, k = largo del bloque
    """
    # Caso Base 1: Bloque vacío
    if k == 0:
        return 0.0
    
    # [span_0](start_span)Caso Base 2: Regla (b), una sola porción[span_0](end_span)
    if k == 1:
        # El jugador actual se la come. Score_neto = st[i] - 0
        return float(st[i])
        
    # Verificar memoización
    if memo[i][k] != SENTINEL:
        return memo[i][k]

    # --- Lógica de Transición (Recurrencia) ---
    
    # 1. Identificar los índices del bloque actual (i, k)
    current_block_indices = {(i + m) % N for m in range(k)}
    
    possible_moves = []
    
    # 2. Iterar sobre TODOS los 2n (N) posibles ángulos de corte alpha_j
    for j in range(N):
        
        # 3. [span_1](start_span)Validar el corte j según Regla (c.1)[span_1](end_span)
        # "al menos una porción... en cada lado"
        side1_indices = {(j + m) % N for m in range(1, n_pequeno)}
        side2_indices = {(j + n_pequeno + m) % N for m in range(1, n_pequeno)}
        side1_has_pieces = any(p in current_block_indices for p in side1_indices)
        side2_has_pieces = any(p in current_block_indices for p in side2_indices)
        
        if side1_has_pieces and side2_has_pieces:
            possible_moves.append(j)

    # Caso Base 3: "Parar de comer" (no hay movimientos válidos)
    if not possible_moves:
        memo[i][k] = 0.0
        return 0.0
        
    best_net_score = -float('inf')

    # 4. Probar todos los cortes válidos (j) y aplicar minimax
    for j in possible_moves:
        
        # 4a. [span_2](start_span)Calcular score (Regla c.2: comer semicírculo)[span_2](end_span)
        semicircle_indices = {(j + m) % N for m in range(n_pequeno)}
        
        # Comemos la intersección del bloque actual y el semicírculo
        pieces_to_eat = current_block_indices.intersection(semicircle_indices)
        move_score = sum(st[p] for p in pieces_to_eat)
        
        # 4b. Identificar el subproblema restante
        remaining_pieces = current_block_indices.difference(pieces_to_eat)
        
        new_i, new_k = 0, 0
        if remaining_pieces:
            new_k = len(remaining_pieces)
            # Encontrar el índice 'i' del nuevo bloque
            new_i = -1
            for p in remaining_pieces:
                if (p - 1 + N) % N not in remaining_pieces:
                    new_i = p
                    break
        
        # 4c. Aplicar Minimax
        opponent_net_score = dp_array(new_i, new_k, st, memo, N, n_pequeno)
        my_net_score = move_score - opponent_net_score
        best_net_score = max(best_net_score, my_net_score)

    # 5. Guardar y retornar el resultado
    memo[i][k] = best_net_score
    return best_net_score


# ---
# Implementación 2: Memoización con Tablas de Hash (Diccionarios)
# Requerida por la tarea
# ---

def solve_torta_hash(st: List[int]) -> float:
    """
    Resuelve el problema de la torta usando Programación Dinámica
    con memoización basada en Tablas de Hash (Diccionarios).
    """
    N = len(st)
    if N == 0:
        return 0.0
    
    n_pequeno = N // 2
    total_sum = sum(st)
    
    # memo[(i, k)] almacena el resultado de dp(i, k)
    memo: Dict[Tuple[int, int], float] = {}

    net_score = dp_hash(0, N, st, memo, N, n_pequeno)
    
    return (total_sum + net_score) / 2

def dp_hash(i: int, k: int, st: List[int], memo: Dict[Tuple[int, int], float], N: int, n_pequeno: int) -> float:
    """
    Función recursiva (subproblema) para la memoización con hash.
    La lógica es IDÉNTICA a 'dp_array', solo cambia el
    almacenamiento en 'memo'.
    """
    # Casos Base
    if k == 0:
        return 0.0
    if k == 1:
        return float(st[i])
        
    # Verificar memoización
    if (i, k) in memo:
        return memo[(i, k)]

    # --- Lógica de Transición (Exactamente la misma que antes) ---
    
    current_block_indices = {(i + m) % N for m in range(k)}
    possible_moves = []
    
    for j in range(N):
        side1_indices = {(j + m) % N for m in range(1, n_pequeno)}
        side2_indices = {(j + n_pequeno + m) % N for m in range(1, n_pequeno)}
        side1_has_pieces = any(p in current_block_indices for p in side1_indices)
        side2_has_pieces = any(p in current_block_indices for p in side2_indices)
        if side1_has_pieces and side2_has_pieces:
            possible_moves.append(j)

    if not possible_moves:
        memo[(i, k)] = 0.0
        return 0.0
        
    best_net_score = -float('inf')

    for j in possible_moves:
        semicircle_indices = {(j + m) % N for m in range(n_pequeno)}
        pieces_to_eat = current_block_indices.intersection(semicircle_indices)
        move_score = sum(st[p] for p in pieces_to_eat)
        remaining_pieces = current_block_indices.difference(pieces_to_eat)
        
        new_i, new_k = 0, 0
        if remaining_pieces:
            new_k = len(remaining_pieces)
            new_i = -1
            for p in remaining_pieces:
                if (p - 1 + N) % N not in remaining_pieces:
                    new_i = p
                    break
        
        opponent_net_score = dp_hash(new_i, new_k, st, memo, N, n_pequeno)
        my_net_score = move_score - opponent_net_score
        best_net_score = max(best_net_score, my_net_score)

    # Guardar y retornar el resultado
    memo[(i, k)] = best_net_score
    return best_net_score


# ---
# Bloque Principal de Ejecución (Para Entrega 2)
# ---
if __name__ == "__main__":
    
    # 1. Prueba simple (para verificar la lógica)
    st_test = [10, 1, 1, 10]
    print(f"Prueba simple st={st_test}")
    print(f"Resultado (Array): {solve_torta_array(st_test)}")
    print(f"Resultado (Hash):  {solve_torta_hash(st_test)}")
    print("-" * 60)

    # 2. Análisis experimental (para la Entrega 2 y los gráficos)
    print("Iniciando análisis experimental (puede tardar)...")
    print(f"{'n':<5} {'N':<5} {'Tiempo Array (s)':<20} {'Tiempo Hash (s)':<20} {'Resultado'}")
    print("-" * 60)

    # n=12 (N=24) puede tardar varios segundos/minutos.
    # n=14 (N=28) puede tardar mucho más. 
    # Ajusta la lista según el tiempo que tengas para el análisis.
    valores_n = [2, 4, 6, 8, 10, 12] 
    
    for n_val in valores_n:
        N_val = 2 * n_val
        # Generamos datos aleatorios para la prueba
        st_random = [random.randint(-10, 10) for _ in range(N_val)]
        
        # --- Estrategia con Arreglos ---
        t_start_array = time.time()
        r_array = solve_torta_array(st_random)
        t_end_array = time.time()
        time_array = t_end_array - t_start_array
        
        # --- Estrategia con Hash ---
        t_start_hash = time.time()
        r_hash = solve_torta_hash(st_random)
        t_end_hash = time.time()
        time_hash = t_end_hash - t_start_hash
        
        # Los resultados deben ser idénticos (salvo mínimos errores de flotante)
        resultado_str = f"{r_array:.2f}"
        
        print(f"{n_val:<5} {N_val:<5} {time_array:<20.6f} {time_hash:<20.6f} {resultado_str}")

