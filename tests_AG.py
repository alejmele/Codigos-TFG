from time import perf_counter
from multiprocessing import Pool
import AG_SM


# Función que lee un archivo de datos con instancias de un problema en el formato especificado
# en generador_instancias, y las convierte en listas de listas.
def leer_archivo(fichero: str) -> list:
    archivo = open(fichero, 'r', encoding='utf-8')
    datos = archivo.read()
    l_datos = datos.split('\n')
    L = len(l_datos)
    i = 0
    l_instancias = []
    while i < L:
        instancia = []
        while l_datos[i]:
            str_fila = l_datos[i].split()
            fila = list(map(int, str_fila))
            instancia.append(fila)
            i += 1
        if i != L - 1:
            l_instancias.append((instancia, i + 1))
        i += 1
    return l_instancias


# Función que realiza el la ejecución del algoritmo genético para una instancia mat_pref.
# Devuelve todos los datos que nos aporten información relevante, como el tiempo de ejecución,
# el mejor fitness obtenido, etc.
# Guardamos también el orden de las instancias para poder reordenarlas luego, ya que la
# paralelización realizada no lo conserva.
def procesar_instancia(num_ind, num_gen, func_fit, metrica, prob_mut, N, mat_pref, nr_inst):
    t1 = perf_counter()
    (mejor_ind, mejor_fit, mejor_pares, mejor_metrica) = AG_SM.algoritmo_genetico(num_ind, num_gen, func_fit, metrica, prob_mut, mat_pref, N)
    t2 = perf_counter()
    return (nr_inst, mejor_ind, mejor_fit, mejor_pares, mejor_metrica, t2 - t1)


# Función que procesa los resultados obtenidos. Se deja en blanco, ya que depende del test
# que estemos realizando. Puede tratarse de calcular medias y escribirlas en un archivo, hallar
# la mejor y la peor solución, realizar una gráfica con matplotlib, etc.
def procesar_resultados(l_res, N):
    pass


# Función principal a la que se llama para realizar los tests.
# Hacemos uso del modulo multiprocessing para paralelizar la ejecución de las instancias
def hacer_test(num_ind, num_gen, func_fit, metrica, prob_mut, N, fichero):
    pool = Pool(6)
    l_instancias = leer_archivo(fichero)
    # Se crea la lista de argumentos para el starmap
    l_argumentos = [(num_ind, num_gen, func_fit, metrica, prob_mut, N, mat_pref, nr_inst) for (mat_pref, nr_inst) in l_instancias]
    # La pool va ejecutando las instancias especificadas en la lista l_argumentos
    l_resultados = pool.starmap(procesar_instancia, l_argumentos)
    # Reordenamos la lista para recuperar el orden original de instancias
    l_resultados.sort(key = lambda x : x[0])
    procesar_resultados(l_resultados, N)
