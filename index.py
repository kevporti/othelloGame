# Funcion auxiliar para sacar el simbolo del enter en un string
def sacarEnter(str):
  return str.strip("\n")

# Definir estado inicial del juego. Separar jugadores y guardar el color que inicia.
def leerJugadores(archivo):
  [nombreUno, colorUno] = archivo.readline().split(',')
  [nombreDos, colorDos] = archivo.readline().split(',')
  colorInicial = archivo.readline()

  jugadores = {
    sacarEnter(colorUno): nombreUno,
    sacarEnter(colorDos): nombreDos,
  }

  return (jugadores, sacarEnter(colorInicial))

# Lee las jugadas del archivo y devuelve una lista de tuplas de la forma (color del jugador, jugada)
def leerJugadas(archivo, colorInicial):
  jugadas = []
  colorActual = colorInicial
  for linea in archivo:
    jugadas.append((colorActual, sacarEnter(linea)))

    if colorActual == 'B':
      colorActual = 'N'
    else: 
      colorActual = 'B'

  return jugadas

# Abre el archivo y declara las variables de los jugadores, las jugadas y el color inicial, luego cierra el archivo.
def leerArchivo():
  archivo = open('juegoParadoPorDobleSkipGanadorB.txt', 'r')

  (jugadores, colorInicial) = leerJugadores(archivo)
  jugadas = leerJugadas(archivo, colorInicial)

  archivo.close()

  return jugadores, jugadas

# Determinar si la posicion de la jugada coincide con tener al menos una ficha del oponente alrededor de la nueva ficha,
# sino, es una jugada invalida. Si la jugada es invalida, se produce una excepcion.
def reglaUno(tablero, jugada):
  pass

# Determinar si la posicion de la jugada coincide con la reglaUno y en ese espacio (vertical, horizontal u oblicuo)
# se encuentra una ficha aliada para encerrar esas fichas enemigas y convertirse en una jugada valida. Si la jugada
# es invalida, se produce una excepcion.
def reglaDos(tablero, jugada):
  pass

# Dada una jugada valida, aplica la misma en el tablero
def aplicarJugada(tablero, jugada):
  pass

# Checkea cada jugada (llamando a las respectivas funciones de cada regla) y, si es valida, aplica el resultado de la misma al tablero
def simularJuego(tablero, jugadas):
  for jugada in jugadas:
    reglaUno(tablero, jugada)
    reglaDos(tablero, jugada)

# Recibe el tablero y devuelve el nombre del jugador, basado en la cantidad de fichas de cada color
def determinarGanador(tablero):
  pass

# Muestra el tablero con el formato adecuado
def imprimirTablero(tablero):
  pass

# Punto de entrada del programa
def main():
  tablero = [[0 for _ in range(8)] for _ in range(8)]

  jugadores, jugadas = leerArchivo()

  try:
    simularJuego(tablero, jugadas)
  except:
    imprimirTablero(tablero)
    # mostrar jugada invalida
  else:
    imprimirTablero(tablero)
    determinarGanador(tablero)
    # mostrar ganador

# 
if __name__ == '__main__':
  main()
