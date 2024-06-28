# En este código generaremos todas los emparejamientos estables de una instancia
# de SM mediante el método de backtracking.
# Este método explora todas las posibles soluciones (en nuestro caso va construyendo
# los emparejamientos parciales), descartando aquellas que no sean factibles
# La complejidad crece rápidamente con N, por lo que solo se debe utilizar con
# valores pequeños de N


# Definimos estas funciones por comodidad
def rank_hombre(h: int, m: int, mat_pref: list[list[int]]) -> int:
    return mat_pref[h - 1][m - 1]


def rank_mujer(h: int, m: int, mat_pref: list[list[int]], N: int) -> int:
    return mat_pref[m - 1][N + h - 1]


# Comprobamos la estabilidad viendo si entre pares de parejas no hay pares bloqueantes
# (es decir, comprueba si (h_i, m_j) y (h_j, m_i) son bloqueantes).
def comprobar_estabilidad(p_i: tuple[int], p_j: tuple[int], mat_pref: list[list[int]], N: int) -> bool:
    (h_i, m_i) = p_i
    (h_j, m_j) = p_j
    es_estable_i_j = (rank_hombre(h_i, m_i, mat_pref) <= rank_hombre(h_i, m_j, mat_pref)) or \
                     (rank_mujer(h_j, m_j, mat_pref, N) <= rank_mujer(h_i, m_j, mat_pref, N))
    es_estable_j_i = (rank_hombre(h_j, m_j, mat_pref) <= rank_hombre(h_j, m_i, mat_pref)) or \
                     (rank_mujer(h_i, m_i, mat_pref, N) <= rank_mujer(h_j, m_i, mat_pref, N))
    return es_estable_i_j and es_estable_j_i


# Al contrario que en el resto de algoritmos, vamos comprobando la estabilidad del emparejamiento
# parcialmente, viendo si el par introducido en la iteración k genera pares bloqueantes.
def es_valida(M: list[int], p: tuple[int], mat_pref: list[list[int]], N: int, k: int) -> bool:
    if k == 0:
        return True
    else:
        i = 0
        b = True
        while i < k and b:
            b = comprobar_estabilidad((i + 1, M[i]), p, mat_pref, N)
            i += 1
        return b


# Inicializamos con k = 0, M = [0..0], libres = [1..N] sols = []
def backtracking_SM(mat_pref: list[list[int]], N: int, M: list[int], libres: list[int], k: int, sols):
    if k == N:
        sol = M.copy()
        sols.append(sol)
    else:
        for i in range(N - k):
            m_act = libres[i]
            p = (k + 1, m_act)
            libres.pop(i)   # Marcamos libres
            if es_valida(M, p, mat_pref, N, k):
                M[k] = m_act
                backtracking_SM(mat_pref, N, M, libres, k + 1, sols)
            libres.insert(i, m_act)
