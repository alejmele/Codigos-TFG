import random


# Función generadora de una instancia de tamaño N con un porcentaje de empates del
# 100*p_emp % y un porcentaje de incompletitud del 100*p_emp %.
# Naturalmente, debe darse p_emp + p_inc <= 1.
# Esta función no asegura que las listas tengan los porcentajes exactos indicados,
# ya que toma estos porcentajes como probabilidades de empate/incompletitud para cada
# elemento de la lista. 
# No obstante, para valores de N >= 15 se comporta como tal.
def generar_instancia_SMTI(N: int, p_emp: float, p_inc: float) -> list[list[int]]:
    mat_pref = []
    for _ in range(N):
        fila = []
        for _ in range(2):
            l_pref = []
            l_val = []
            j = 1
            for _ in range(N):
                p_e = random.uniform(0, 1)
                if p_e > (1 - p_inc):
                    l_val.append(N + 1)
                else:
                    l_val.append(j)
                    if p_e > p_emp:
                        j += 1
            for i in range(N - 1, -1, -1):
                p = random.randint(0, i)
                l_pref.append(l_val[p])
                l_val.pop(p)
            fila += l_pref
        mat_pref.append(fila)
    return mat_pref


# Función generadora de num_inst instancias con los parametros anteriores.
# Guarda los elementos de las listas en forma de matriz en el archivo de texto 'fichero'.
# Cada instancia queda separada por una linea en blanco.
def generar_banco_pruebas(N: int, p_emp: float, p_inc: float, num_inst: int, fichero: str) -> None:
    archivo = open(fichero, 'w', encoding='utf-8')
    for _ in range(num_inst):
        M = generar_instancia_SMTI(N, p_emp, p_inc)
        for fila in M:
            for elem in fila:
                info = str(elem)
                archivo.write(info)
                archivo.write(' ')
            archivo.write('\n')
        archivo.write('\n')
