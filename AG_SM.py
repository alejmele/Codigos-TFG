import random


# Comprueba si un par es estable en SM
# Esta misma función comprueba la estabilidad débil en SMT
def es_estable(par: tuple[int], M: list[int], mat_pref, N: int) -> bool:
    (h_p, m_p) = par
    rank_h_p = mat_pref[h_p - 1][m_p - 1]
    rank_m_p = mat_pref[m_p - 1][N + h_p - 1]
    h_M = M.index(m_p) + 1
    m_M = M[h_p - 1]
    rank_h_M = mat_pref[h_p - 1][m_M - 1]
    rank_m_M = mat_pref[m_p - 1][N + h_M - 1]
    return (rank_h_M <= rank_h_p) or (rank_m_M <= rank_m_p)


# Comprueba si un par es estable en SMI (o en SMTI con la estabilidad débil)
# Hay que tener en cuenta si el par es aceptable o no antes de comparar rankings
def es_estable_SMI(par: tuple[int], M: list[int], mat_pref, N: int) -> bool:
    (h_p, m_p) = par
    rank_h_p = mat_pref[h_p - 1][m_p - 1]
    rank_m_p = mat_pref[m_p - 1][N + h_p - 1]
    h_M = M.index(m_p) + 1
    m_M = M[h_p - 1]
    rank_h_M = mat_pref[h_p - 1][m_M - 1]
    rank_m_M = mat_pref[m_p - 1][N + h_M - 1]
    aceptables = (rank_h_p != N + 1) and (rank_m_p != N + 1)
    if m_p == m_M:
        return True
    else:
        return (not aceptables) or rank_h_M <= rank_h_p or rank_m_M <= rank_m_p


# Itera sobre el conjunto de posibles pares y cuenta los estables.
# Para la versión con incompletitud, usar la función es_estable_SMI
def num_estables(M: list[int], mat_pref: list[list[int]], N: int) -> int:
    cont = 0
    for h in range(1, N + 1):
        for m in range(1, N + 1):
            if es_estable((h,m), M, mat_pref, N):
                cont += 1
    return cont


def suma_rankings_hombres(M: list[int], mat_pref: list[list[int]], N: int):
    s = 0
    for h in range(1, N + 1):
        m = M[h - 1]
        s += mat_pref[h - 1][m - 1]
    return s


def suma_rankings_mujeres(M: list[int], mat_pref: list[list[int]], N: int):
    s = 0
    for h in range(1, N + 1):
        m = M[h - 1]
        s += mat_pref[m - 1][N + h - 1]
    return s


# Calcula el peor ranking entre hombres y mujeres del emparejamiento M
def max_rank(M: list[int], mat_pref: list[list[int]], N: int):
    max_rank = 0
    for h in range(1, N + 1):
        m = M[h - 1]
        rank_h = mat_pref[h - 1][m - 1] 
        rank_m = mat_pref[m - 1][N + h - 1]
        max_rank = max(max_rank,rank_h,rank_m)
    return max_rank


# Definimos los costes de arrepentimiento (regret), igualitario (egalitarian)
# y de similitud (sex-fair) según la memoria
def regret(M: list[int], mat_pref: list[list[int]], N: int) -> int:
    return max_rank(M, mat_pref, N)


def egalitarian(M: list[int], mat_pref: list[list[int]], N: int) -> int:
    sm = suma_rankings_hombres(M, mat_pref, N)
    sw = suma_rankings_mujeres(M, mat_pref, N)
    return sm + sw


def sex_fair(M: list[int], mat_pref: list[list[int]], N: int) -> int:
    sm = suma_rankings_hombres(M, mat_pref, N)
    sw = suma_rankings_mujeres(M, mat_pref, N)
    return abs(sm - sw)


# Definimos las distintas funciones de fitness en función de la métrica
# que se quiera estudiar
def func_fitness_SM_basico(ind: list, mat_pref: list[list[int]], N: int) -> int:
    return num_estables(ind, mat_pref, N)


def func_fitness_SM_regret(ind: list, mat_pref: list[list[int]], N: int) -> int:
    e = num_estables(ind, mat_pref, N)
    c = regret(ind, mat_pref, N)
    return e - c / N


def func_fitness_SM_egalitarian(ind: list, mat_pref: list[list[int]], N: int) -> int:
    e = num_estables(ind, mat_pref, N)
    c = egalitarian(ind, mat_pref, N)
    return e - c / (2 * N**2)


def func_fitness_SM_sex_fair(ind: list, mat_pref: list[list[int]], N: int) -> int:
    e = num_estables(ind, mat_pref, N)
    c = sex_fair(ind, mat_pref, N)
    return e - c / N**2


# Generamos la población inicial generando permutaciones aleatorias a partir de
# la función random.uniform
def generar_poblacion(num_individuos: int, N: int) -> list:
    poblacion = []
    for _ in range(num_individuos):
        ind = []
        l_val = list(range(1, N + 1))
        for i in range(N - 1, -1, -1):
            p = random.randint(0, i)
            ind.append(l_val[p])
            l_val.pop(p)
        poblacion.append(ind)
    return poblacion

# Seleccionamos los individuos por torneo.
# Tomamos dos individuos distintos de la población mediante la función random.randint 
# (si por casualidad i y j son iguales volvemos a generar un entero aleatorio)
# y seleccionamos el mejor de los dos.
# Repetimos el proceso hasta reducir la población a la mitad
def seleccionar(poblacion: list, num_individuos: int, mat_pref: list[list[int]], func_fit: callable, N: int) -> None:
    tam = num_individuos
    for _ in range(num_individuos // 2):
        i = random.randint(0, tam - 1)
        j = random.randint(0, tam - 1)
        while i == j:
            j = random.randint(0, tam - 1)
        fit_i = func_fit(poblacion[i], mat_pref, N)
        fit_j = func_fit(poblacion[j], mat_pref, N)
        if fit_i <= fit_j:
            poblacion.pop(i)
        else:
            poblacion.pop(j)
        tam -= 1


def combinar_seg(ind: list[int], seg: list[int]) -> list[int]:
    inic = seg[0]
    hijo = []
    for v in ind:
        if v == inic:
            hijo += seg
        elif v not in seg:
            hijo.append(v)
    return hijo

# Cruzamos ambos padres por segmento como se indica en la memoria.
# Lo hacemos de forma que el segmento que intercambiamos siempre sea no nulo.
def cruzar_segmento(ind_1: list, ind_2: list, N: int) -> tuple[list]:
    c_1 = random.randint(0, N - 2)
    c_2 = random.randint(c_1 + 1, N - 1)
    h_1 = combinar_seg(ind_2, ind_1[c_1:c_2])
    h_2 = combinar_seg(ind_1, ind_2[c_1:c_2])
    return (h_1, h_2)

# Cruzamos ambos padres por cruce cíclico como se indica en la memoria.
def cruzar_ciclico(ind_1: list, ind_2: list, N: int) -> tuple[list]:
    c = random.randint(0, N - 1)
    x_0 = ind_1[c]
    h_1 = [None for _ in range(N)]
    h_2 = [None for _ in range(N)]
    h_1[c] = ind_1[c]
    h_2[c] = ind_2[c]
    while ind_2[c] != x_0:
        c = ind_1.index(ind_2[c])
        h_1[c] = ind_1[c]
        h_2[c] = ind_2[c]
    for i in range(N):
        if h_1[i] == None:
            h_1[i] = ind_2[i]
            h_2[i] = ind_1[i]
    return (h_1, h_2)


def intercambiar(l: list, i: int, j: int) -> None:
    temp = l[i]
    l[i] = l[j]
    l[j] = temp

# La función de mutación.
# Si el número generado por random.uniform está por debajo de prob_mut intercambiamos
# dos posiciones al azar del emparejamiento
def mutar(ind: int, prob_mut: float, N: int) -> None:
    r = random.uniform(0, 1)
    if r <= prob_mut:
        pos_1 = random.randint(0, N - 1)
        pos_2 = random.randint(0, N - 1)
        while pos_1 == pos_2:
            pos_2 = random.randint(0, N - 1)
        intercambiar(ind, pos_1, pos_2)


def algoritmo_genetico(num_individuos: int, num_gen: int, func_fit: callable, metrica: callable, prob_mut: int, mat_pref: list[list[int]], N: int) -> None:
    mejor_ind = []
    mejor_fit = 0
    mejor_pares = None
    mejor_metrica = None
    # Generamos la población inicial
    poblacion = generar_poblacion(num_individuos, N)
    for gen in range(num_gen):
        # Seleccionamos los individuos por torneo
        seleccionar(poblacion, num_individuos, mat_pref, func_fit, N)
        # Cruzamos los individuos seleccionados al azar hasta reponer la población
        for _ in range(num_individuos // 4):    # Tomar el numero de individuos múltiplo de 4
            pos_1 = random.randint(0, (num_individuos // 2) - 1)
            pos_2 = random.randint(0, (num_individuos // 2) - 1)
            while pos_1 == pos_2:
                pos_2 = random.randint(0, (num_individuos // 2) - 1)
            (h1, h2) = cruzar_ciclico(poblacion[pos_1], poblacion[pos_2], N)
            poblacion.append(h1)
            poblacion.append(h2)
        # Mutamos los individuos con la probabilidad indicada
        for ind in poblacion:
            mutar(ind, prob_mut, N)
        # Evaluamos los individuos y nos quedamos con el que mejor fitness tenga
        for ind in poblacion:
            fit_ind = func_fit(ind, mat_pref, N)
            if fit_ind > mejor_fit:
                # Almacenamos los datos que nos interesan para su posterior procesado
                mejor_ind = ind.copy()
                mejor_fit = fit_ind
                mejor_pares = num_estables(mejor_ind, mat_pref, N)
                mejor_metrica = metrica(mejor_ind, mat_pref, N)
    return (mejor_ind, mejor_fit, mejor_pares, mejor_metrica)
