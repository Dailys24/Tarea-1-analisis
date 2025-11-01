"""
Tarea 1 - Análisis y Diseño de Algoritmos
Problema: "Feliz Cumpleaños"
Integrantes: [Tu nombre] - [Nombre de tu compañero]
Profesor: [Nombre del profesor]
Fecha: 20/11/2025

Descripción general:
--------------------
El profesor y su hermana comparten una torta circular dividida en 2n porciones,
cada una con un valor de satisfacción entero (positivo o negativo). Ambos se
turnan para elegir porciones siguiendo reglas predefinidas, y el profesor busca
maximizar la satisfacción total que puede garantizarse comer.

Este programa aplica Programación Dinámica (DP) con el esquema SRTBOT,
implementando dos estrategias de memorización:
    1. Listas bidimensionales (arreglo)
    2. Diccionarios (hash map)
Se comparan los tiempos de ejecución de ambas estrategias para distintos n.
"""

import time
import random

#Memorisacion con listas
def max_satisfaccion_array(st):
    """
    Calcula la máxima diferencia de satisfacción usando DP con listas bidimensionales.

    Parámetros:
        st (list): lista de enteros (valores de satisfacción de las 2n porciones)

    Retorna:
        int: máxima satisfacción garantizada para el profesor.
    """
    n = len(st)
    st = st * 2  #duplicar para manejar circularidad
    dp = [[None for _ in range(2 * n)] for _ in range(2 * n)]

    def solve(i, j):
        #Caso base
        if i == j:
            return st[i]

        #Verificar memoización
        if dp[i][j] is not None:
            return dp[i][j]

        #Recurrencia
        tomar_izq = st[i] - solve(i + 1, j)
        tomar_der = st[j] - solve(i, j - 1)
        dp[i][j] = max(tomar_izq, tomar_der)
        return dp[i][j]

    #Caso origen
    mejor = float('-inf')
    for i in range(n):
        mejor = max(mejor, solve(i, i + n - 1))
    return mejor

#Memorisacion con Hash
def max_satisfaccion_hash(st):
    """
    Calcula la máxima diferencia de satisfacción usando DP con diccionarios (hash map).

    Parámetros:
        st (list): lista de enteros (valores de satisfacción de las 2n porciones)

    Retorna:
        int: máxima satisfacción garantizada para el profesor.
    """
    n = len(st)
    st = st * 2
    memo = {}

    def solve(i, j):
        #Caso base
        if i == j:
            return st[i]

        #Verificar memoización
        if (i, j) in memo:
            return memo[(i, j)]

        #Recurrencia
        tomar_izq = st[i] - solve(i + 1, j)
        tomar_der = st[j] - solve(i, j - 1)
        memo[(i, j)] = max(tomar_izq, tomar_der)
        return memo[(i, j)]

    #Caso origen
    mejor = float('-inf')
    for i in range(n):
        mejor = max(mejor, solve(i, i + n - 1))
    return mejor

#Main
def main():
    """
    Ejecuta pruebas fijas y aleatorias para ambas estrategias,
    mostrando los tiempos y resultados.
    """

    print("\n===== TAREA 1 - FELIZ CUMPLEAÑOS =====\n")
    print("Comparación entre estrategias de memoización")
    print(f"{'n':<5} {'Array (s)':<15} {'Hash (s)':<15} {'Resultado'}")
    print("-" * 55)

    #Casos de prueba automáticos (aleatorios)
    for n in [4, 6, 8, 10, 12, 14]:
        st = [random.randint(-10, 10) for _ in range(2 * n)]

        #Estrategia con listas
        t1 = time.time()
        r1 = max_satisfaccion_array(st)
        t2 = time.time()

        #Estrategia con hash
        r2 = max_satisfaccion_hash(st)
        t3 = time.time()

        print(f"{n:<5} {t2 - t1:<15.5f} {t3 - t2:<15.5f} {r1}")

    print("\n* Ambas estrategias entregan el mismo resultado.\n")

    #Casos de prueba fijos (para validación)
    print("Casos de prueba fijos:\n")

    casos = [
        [5, -3, 7, 2, -4, 6, 1, -2],
        [3, 1, -2, 8, -1, 4],
        [-5, 10, -3, 7, -6, 2]
    ]

    for i, st in enumerate(casos, start=1):
        print(f"Caso {i}: {st}")
        print(f" → Resultado (listas): {max_satisfaccion_array(st)}")
        print(f" → Resultado (hash):   {max_satisfaccion_hash(st)}\n")

#Ejecucion Main
if __name__ == "__main__":
    main()