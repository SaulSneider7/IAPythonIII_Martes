# -------------------------------------------------------------------------
# Crack the Code
# Aprendizaje por reforzamiento
# -------------------------------------------------------------------------
# Importar bibliotecas que se utilizarán - no modifiques esta sección
import pygame
from pygame.locals import *
import numpy as np
from time import sleep
import laberintos

# -------------------------------------------------------------------------
# Sesión 1: Laberintos, acciones y recompensas

# Recompensas y tamaño del laberinto
# Escribe aquí tu código
# Elegimo nuestro laberiento que vamos a usar
recompensas = laberintos.laberinto_1

# Tamanos de imagen y ventana
# Escribe aquí tu código
filas = recompensas.shape[0]
columnas = recompensas.shape[1]

size = 32 # Este sera el tamano de las imagenes
ventana_alto = columnas * size
ventana_acho = filas * size

# Iniciar pygame y crear ventana
# Escribe aquí tu código
pygame.init()
ventana = pygame.display.set_mode((ventana_alto, ventana_acho), pygame.HWSURFACE)

# Cargar imagenes del muro, jugador y la meta
# Escribe aquí tu código
img_muro = pygame.image.load("Imagenes/Muro.jpg").convert()
img_jugador = pygame.image.load("Imagenes/Jugador.jpg").convert()
img_meta = pygame.image.load("Imagenes/Meta.jpg").convert()

# Función para dibujar el estado actual del laberinto y la posición del jugador
def dibujar_laberinto(jugador_x, jugador_y):
    # Escribe aquí tu código
    for i in range(0, recompensas.shape[0]):
        for j in range(0, recompensas.shape[1]):
            if recompensas[i, j] == -100:
                ventana.blit(img_muro, (j * size, i * size))
            if recompensas[i , j] == 100:
                ventana.blit(img_meta, (j * size, i * size))
    ventana.blit(img_jugador, (jugador_y * size, jugador_x * size))


# -------------------------------------------------------------------------
# Sesión 2: Fin del juego, punto inicial y punto siguiente

# Define la condición final
# Si la recompensa es -1 (es una casilla vacia) entonces el juego sigue
# Si choca con un muro (pierde) o llega a la meta (gana) el juego termina
def fin_del_juego(fila_actual, columna_actual):
    # Escribe aquí tu código
    if recompensas[fila_actual, columna_actual] == -1.:
        return False
    else:
        return True

# Inicia el juego desde una posición aleatoria
def punto_inicial():
    # Escribe aquí tu código
    while True:
        # Buscar un valor de fila y columna para empezar el juego
        fila_actual = np.random.randint(filas)
        columna_actual = np.random.randint(columnas)

        #Si la posicion elegida no es un moro o la meta se puede iniciar el juego
        if not fin_del_juego(fila_actual, columna_actual):
            break
    #Retorna el resultado obtenido
    return fila_actual, columna_actual


# Esta función nos ayuda a elegir una acción facilmente y calcular la nueva posición utilizando solo un numero
def punto_siguiente(fila_actual, columna_actual, indice_de_accion):
    # Escribe aquí tu código
    #Guardar los valores actuales
    nueva_fila = fila_actual
    nueva_columna = columna_actual

    #Acciones: 0 = arriba, 1 = derecha, 2 = abajo, 3 = izquierda
    acciones = ['arriba', 'derecha', 'abajo', 'izquierda']

    if acciones[indice_de_accion] == 'arriba' and fila_actual > 0:
        nueva_fila -= 1
    elif acciones[indice_de_accion] == 'derecha' and columna_actual < columnas - 1:
        nueva_columna += 1
    elif acciones[indice_de_accion] == 'abajo' and fila_actual < columnas - 1:
        nueva_columna += 1
    elif acciones[indice_de_accion] == 'izquierda' and columna_actual < columnas - 1:
        nueva_columna += 1

    return nueva_fila, nueva_columna

# -------------------------------------------------------------------------
# Sesión 3: Entrenamiento

# Tabla con los valores Q y parametros del entrenamiento
# Escribe aquí tu codigo
valores_q = np.zeros((filas, columnas, 4))

#Parametros del entrenamiento
exploracion = 0.1
descuento = 0.9
aprendizaje = 0.9

# Es una función que nos ayuda a explorar nuevas posibilidades o a utilizar el conocimiento que ya tenemos
# para ello utiliza el parametro explorar, el cual es un porcentaje que nos ayuda a decidir que tantas veces vamos
# a utilizar valores al azar y cuantas veces vamos a usar las mejores respuestas que tenemos
def siguiente_accion(fila_actual, columna_actual, explorar):
    # Escribe aquí tu código
    if np.random.random() > explorar:
        # Se una la funcion argmax para descubrir el mejor camino
        return np.argmax(valores_q[fila_actual, columna_actual])
    else:
        #Retorne un numero aleatorio
        return np.random.randint(4)


# -------------------------------------------------------------------------
# JUEGO - Este parte del código se modificará sesión a sesión

# Escribe tu codigo aquí
#Entrenamos nuestra IA haciendo que resulva el laberinto 1000 veces
x, y = punto_inicial()

while True:
    #Guardar posicion anterior
    x_anterior = x
    y_anterior = y

    #accion al azar usando la funcion siguiente_accion
    accion = siguiente_accion(x, y, exploracion)

    x, y = punto_siguiente(x, y, accion)

    valores_q_actual = valores_q[x_anterior, y_anterior, accion]

    #calcular nuevo valor
    recompensa = recompensas[x, y]
    temporal_difference = recompensa + (descuento * np.max(valores_q[x, y, :])) - valores_q_actual
    nuevo_valor_q = valores_q_actual + (aprendizaje * temporal_difference)

    #Actualizar nuevo Valor
    valores_q[x_anterior, y_anterior, accion] = nuevo_valor_q
    ventana.fill((0, 0, 0))

    #dibujar laberinto
    dibujar_laberinto(x,y)
    pygame.display.flip()
    #Condicion del fin del juego
    if fin_del_juego(x, y):
        if recompensas[x, y] == 100:
            print("Has ganado!")
        else:
            print("Has Perdido!")
        break
# -------------------------------------------------------------------------
# Sesión 4 - Resultados del entrenamiento

# Define una función que va a elegir siempre el camino más corto entre un punto inicial y la meta
def camino_mas_corto(inicio_x, inicio_y):
    # Escribe aquí tu codigo
    pass


# Dibuja el camino más corto desde una posición hasta la meta
def dibuja_camino_mas_corto(inicio_x, inicio_y):
    # Escribe aquí tu codigo
    pass


# Prueba tu inteligencia artificial para resolver el laberinto desde varias posiciones iniciales
# Escribe aquí tu codigo


# -------------------------------------------------------------------------
# No borres esta linea, deja esto siempre hasta el final
# Cierra el juego
pygame.quit()
