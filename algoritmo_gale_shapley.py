# Detemos la ejecución del algoritmo cuando todos los hombres estén emparejados o
# cuando hayan agotado su lista de preferencias.
def criterio_parada(M: list[int], listas_pref: list[list[int]], N: int):
    for h in range(1, N + 1):
        m = M[h - 1]
        if m == 0 and len(listas_pref[h - 1]) > 0:
            return True
    return False


# Algoritmo Gale-Shapley
def gsa1(mat_pref: list[list[int]], N: int) -> list[int]:
    M = [0] * N
    listas_pref = []
    pretendientes = []
    # Inicializamos las listas de preferencia de cada hombre (ordenadas de menor a mayor preferencia)
    for h in range(1, N + 1):
        lista_h = [m + 1 for m in range(N)]
        lista_h.sort(key=lambda m : mat_pref[h - 1][m - 1])
        listas_pref.append(lista_h)
    # Inicializamos la lista de pretendientes de cada mujer
    for _ in range(N):
        pretendientes.append([])
    # Iniciamos la fase de proposiciones
    while criterio_parada(M, listas_pref, N):
        # Los hombres sin pareja se proponen a la primera mujer en su lista
        for h in range(1, N + 1):
            m = M[h - 1]
            if m == 0 and len(listas_pref[h - 1]) > 0:
                pretendientes[listas_pref[h - 1][0] - 1].append(h)
                listas_pref[h - 1].pop(0)
        # Las mujeres deciden con quien quedarse
        for m in range(1, N + 1):
            pret_m = pretendientes[m - 1]
            if len(pret_m) == 1:
                h = pret_m[0]
                M[h - 1] = m
            elif len(pret_m) > 1:
                while len(pret_m) > 1:
                    h_1 = pret_m[0]
                    h_2 = pret_m[1]
                    rank_1 = mat_pref[m - 1][N + h_1 - 1]
                    rank_2 = mat_pref[m - 1][N + h_2 - 1]
                    if rank_1 < rank_2:
                        pret_m.pop(1)
                        M[h_2 - 1] = 0
                    else:
                        pret_m.pop(0)
                        M[h_1 - 1] = 0
                h = pret_m[0]
                M[h - 1] = m
    return M
