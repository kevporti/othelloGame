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

def parsearJugada(jugada):
  color, posicion = jugada
  columnaJugada = ord(posicion[0]) - ord('A')
  filaJugada = int(posicion[1]) - 1

  return color, filaJugada, columnaJugada

#Checkear si la posicion de la jugada no esta ocupada
def reglaUno(tablero, jugada):
  _, filaJugada, columnaJugada = parsearJugada(jugada)
  if tablero[filaJugada][columnaJugada] != " ":
    raise Exception(f'La posicion {jugada[1]} ya esta ocupada')

# Determinar si la posicion de la jugada coincide con tener al menos una ficha del oponente alrededor de la nueva ficha,
# sino, es una jugada invalida. Si la jugada es invalida, se produce una excepcion.
# Tambien determinar si hay una ficha aliada que encierre a la enemiga para poder cambiar el color y validar el movimiento.
def reglaDos(tablero, jugada):
  color, filaJugada, columnaJugada = parsearJugada(jugada)

  if color == 'B':
    colorOponente = 'N'
  else:
    colorOponente = 'B'
  
  hayOponenteAlrededor = False
  hayFichasEncerradas = False

  # Recorrer todas las posiciones del tablero que estan alrededor de la jugada realizada
  for i in range(-1, 2):
    for j in range(-1, 2):
      # Quitando el caso de chequear la posicion de la jugada, vemos las posiciones de alrededor.
      if i != 0 or j != 0:
        filaCheckear = filaJugada + i
        columnaCheckear = columnaJugada + j

        # Checkeando que las posiciones a comparar no se salgan de los parametros del tablero
        seSaleDelTablero = filaCheckear >= 8 or filaCheckear < 0 or columnaCheckear >= 8 or columnaCheckear < 0

        fichasEnemigas = 0
        # Recorriendo filas, columnas y diagonales mientras haya una ficha enemiga, para determinar si al final
        # de todas las fichas hay una aliada que encierre las enemigas y poder validar la jugada.
        while not seSaleDelTablero and tablero[filaCheckear][columnaCheckear] == colorOponente:
          fichasEnemigas += 1

          # Avanzar en cada direccion
          filaCheckear += i
          columnaCheckear += j

          seSaleDelTablero = filaCheckear >= 8 or filaCheckear < 0 or columnaCheckear >= 8 or columnaCheckear < 0
        
        # Hay al menos una ficha enemiga adyacente en esa direccion?
        if fichasEnemigas != 0:
          hayOponenteAlrededor = True
        
        # Hay una ficha aliada que encierra a las enemigas en esa direccion?
        if not seSaleDelTablero and tablero[filaCheckear][columnaCheckear] == color:
          hayFichasEncerradas = True

  # Tirar excepciones si la jugada es invalida
  if not hayOponenteAlrededor:
    raise Exception(f'La posicion {jugada[1]} no tiene ningua ficha del oponente alrededor.')

  if not hayFichasEncerradas:
    raise Exception(f'La posicion {jugada[1]} no encierra fichas del oponente.')

# Checkear que si o si era necesario saltar el turno
def reglaTres(tablero, jugada):
  pass


# Dada una jugada valida, aplica la misma en el tablero
def aplicarJugada(tablero, jugada):
  color, filaJugada, columnaJugada = parsearJugada(jugada)

  tablero[filaJugada][columnaJugada] = color

# Checkea cada jugada (llamando a las respectivas funciones de cada regla) y, si es valida, aplica el resultado de la misma al tablero
def simularJuego(tablero, jugadas):
  for jugada in jugadas:
    color, filaJugada, columnaJugada = parsearJugada(jugada)

    if color != ' ':
      reglaUno(tablero, jugada)
      reglaDos(tablero, jugada)
      aplicarJugada(tablero, jugada)
    else:
      reglaTres(tablero, jugada)
    
    print(jugada)
    imprimirTablero(tablero)
    print()

# Recibe el tablero y devuelve el nombre del jugador, basado en la cantidad de fichas de cada color
def determinarGanador(tablero):
  pass

# Muestra el tablero con el formato adecuado
def imprimirTablero(tablero):
  print('  A B C D E F G H')
  for i in range(8):
    nroFila = i + 1
    contenidoFila = ' '.join(tablero[i])
    print(f'{nroFila} {contenidoFila} {nroFila}')
  print('  A B C D E F G H')

def construirTableroInicial():
  tablero = []
  for i in range(8):
    fila = []
    for j in range(8):
      if (i == 3 and j == 3) or (i == 4 and j == 4):
        fila.append("B")
      elif (i == 3 and j == 4) or (i == 4 and j == 3):
        fila.append("N")
      else:
        fila.append(' ')
    tablero.append(fila)
  return tablero

# Punto de entrada del programa
def main():
  tablero = construirTableroInicial()
  jugadores, jugadas = leerArchivo()

  try:
    simularJuego(tablero, jugadas)
  except Exception as e:
    imprimirTablero(tablero)
    print(str(e))
  else:
    imprimirTablero(tablero)
    determinarGanador(tablero)
    # mostrar ganador

# 
if __name__ == '__main__':
  main()
