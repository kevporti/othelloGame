# Funcion auxiliar para remover la secuencia de escape asignada al "Enter" al inicio o final de una cadena de caracteres.
# removerSecuenciaDeEscape: String -> String
def removerSecuenciaDeEscape(str):
  return str.strip("\n")

# Separar las primeras tres lineas del archivo, destinadas a los nombres de los jugadores junto con su color
# (primeras dos lineas, separando nombre y color designado por una coma) y el color que va a iniciar a colocar fichas (tercer linea).
# definirJugadoresYColores: FileObject -> Tuple(Dict{String: String}, String)
def definirJugadoresYColores(archivo):
  [nombreUno, colorUno] = archivo.readline().split(',')
  [nombreDos, colorDos] = archivo.readline().split(',')
  colorInicial = archivo.readline()

  jugadores = {
    removerSecuenciaDeEscape(colorUno): nombreUno,
    removerSecuenciaDeEscape(colorDos): nombreDos,
  }

  return (jugadores, removerSecuenciaDeEscape(colorInicial))

# Lee las lineas del archivo correspondientes a las jugadas y devuelve una lista de tuplas de la forma (color del jugador, jugada)
# en base al color inicial definido anteriormente.
# definirJugadas: FileObject, String -> List[Tuple(String, String)]
def definirJugadas(archivo, colorInicial):
  jugadas = []
  colorActual = colorInicial

  # Recorriendo las lineas del archivo una a una para crear el formato de tupla anterior mencionado.
  for linea in archivo:
    jugadas.append((colorActual, removerSecuenciaDeEscape(linea)))

    colorActual = 'N' if (colorActual == 'B') else 'B'

  return jugadas

# Abre el archivo y declara las variables de los jugadores, las jugadas y el color inicial, luego cierra el archivo.
# desestructurarArchivo: None -> Dict{String: String}, List[Tuple(String, String)]
def desestructurarArchivo():
  archivo = open('juegoParadoPorDobleSkipGanadorB.txt', 'r')

  (jugadores, colorInicial) = definirJugadoresYColores(archivo)
  jugadas = definirJugadas(archivo, colorInicial)

  archivo.close()

  return jugadores, jugadas

# Funcion auxiliar para desestructurar el formato de la jugada en color, indice de la columna e indice de la fila.
# desestructurarJugada: Tuple(String, String) -> String, Int, Int
def desestructurarJugada(jugada):
  colorDelJugador, posicionDeLaJugada = jugada
  indiceDeLaColumna = ord(posicionDeLaJugada[0]) - ord('A')
  indiceDeLaFila = int(posicionDeLaJugada[1]) - 1

  return colorDelJugador, indiceDeLaFila, indiceDeLaColumna

# Checkear si la posicion de la jugada no esta ocupada
# controlarJugadaRepetida: List[List[String]], Tuple(String, String) -> None
def controlarJugadaRepetida(tablero, jugada):
  _, indiceDeLaFila, indiceDeLaColumna = desestructurarJugada(jugada)
  if tablero[indiceDeLaFila][indiceDeLaColumna] != " ":
    raise Exception(f'La posicion {jugada[1]} ya esta ocupada')

# Determinar si la posicion de la jugada coincide con tener al menos una ficha del oponente alrededor de la nueva ficha,
# sino, es una jugada invalida. Si la jugada es invalida, se produce una excepcion.
# Tambien determinar si hay una ficha aliada que encierre a la enemiga para poder cambiar el color y validar el movimiento.
# controlarJugadasValidas: List[List[String]], Tuple(String, String) -> None
def controlarJugadasValidas(tablero, jugada):
  colorDelJugador, indiceDeLaFila, indiceDeLaColumna = desestructurarJugada(jugada)
  colorDelOponente = 'N' if colorDelJugador == 'B' else 'B'
  hayOponenteAlrededor = False
  hayFichasEncerradas = False

  # Recorrer todas las posiciones del tablero que estan alrededor de la jugada realizada.
  for i in range(-1, 2):
    for j in range(-1, 2):
      # Quitando el caso de verificar la posicion de la jugada, vemos las posiciones de alrededor.
      if i != 0 or j != 0:
        indiceDeLaFilaAVerificar = indiceDeLaFila + i
        indiceDeLaColumnaAVerificar = indiceDeLaColumna + j

        # Verificando que las posiciones a comparar no se salgan de los parametros del tablero.
        seSaleDelTablero = indiceDeLaFilaAVerificar >= 8 or indiceDeLaFilaAVerificar < 0 or indiceDeLaColumnaAVerificar >= 8 or indiceDeLaColumnaAVerificar < 0

        fichasEnemigas = 0
        # Recorriendo filas, columnas y diagonales mientras haya una ficha enemiga, para determinar si al final
        # de todas las fichas hay una aliada que encierre las enemigas y poder validar la jugada.
        while not seSaleDelTablero and tablero[indiceDeLaFilaAVerificar][indiceDeLaColumnaAVerificar] == colorDelOponente:
          fichasEnemigas += 1

          # Avanzar en cada direccion
          indiceDeLaFilaAVerificar += i
          indiceDeLaColumnaAVerificar += j

          seSaleDelTablero = indiceDeLaFilaAVerificar >= 8 or indiceDeLaFilaAVerificar < 0 or indiceDeLaColumnaAVerificar >= 8 or indiceDeLaColumnaAVerificar < 0
        
        # Hay al menos una ficha enemiga adyacente en esa direccion?
        if fichasEnemigas != 0:
          hayOponenteAlrededor = True
        
        # Hay una ficha aliada que encierra a las enemigas en esa direccion?
        if not seSaleDelTablero and tablero[indiceDeLaFilaAVerificar][indiceDeLaColumnaAVerificar] == colorDelJugador:
          hayFichasEncerradas = True

  # Tirar excepciones si la jugada es invalida
  if not hayOponenteAlrededor:
    raise Exception(f'La posicion {jugada[1]} no tiene ningua ficha del oponente alrededor.')

  if not hayFichasEncerradas:
    raise Exception(f'La posicion {jugada[1]} no encierra fichas del oponente.')

# Verificar que si o si era necesario saltar el turno.
# reglaTres: List[List[String]], Tuple(String, String) -> None
def reglaTres(tablero, jugada):
  pass


# Dada una jugada valida, aplicar la misma al tablero.
# aplicarJugada: List[List[String]], Tuple(String, String) -> None
def aplicarJugada(tablero, jugada):
  colorDelJugador, indiceDeLaFila, indiceDeLaColumna = desestructurarJugada(jugada)

  tablero[indiceDeLaFila][indiceDeLaColumna] = colorDelJugador

# Verifica cada jugada (llamando a las respectivas funciones de cada regla) y, si es valida, aplica el resultado de la misma al tablero.
# simularJuego: List[List[String]], Tuple(String, String) -> None
def simularJuego(tablero, jugadas):
  for jugada in jugadas:
    colorDelJugador, indiceDeLaFila, indiceDeLaColumna = desestructurarJugada(jugada)

    # Si el "color del jugador" no es un string vacio, hacer los respectivos controles de la jugada, sino verificar que la jugada (skippeada)
    # era la unica opcion.
    if colorDelJugador != ' ':
      controlarJugadaRepetida(tablero, jugada)
      controlarJugadaRepetida(tablero, jugada)
      controlarJugadasValidas(tablero, jugada)
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

# Construye el tablero con las cuatro piezas iniciales en el centro.
# construitTableroInicial: None -> List[List[String]]
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

# Punto de entrada del programa. Invoca al tablero, los jugadores y las jugadas e intenta simular un juego, si hay errores,
# se le informa al usuario y se muestra el tablero anterior a esa jugada, sino se muestra el tablero final con el ganador.
# main: None -> None
def main():
  tablero = construirTableroInicial()
  jugadores, jugadas = desestructurarArchivo()

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
