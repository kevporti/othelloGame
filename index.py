# Funcion auxiliar para remover la secuencia de escape asignada al "Enter" al inicio o final de una cadena de caracteres.
# removerSecuenciaDeEscape: String -> String
def removerSecuenciaDeEscape(str: str) -> str:
  return str.strip("\n")

# Separar las primeras tres lineas del archivo, destinadas a los nombres de los jugadores junto con su color
# (primeras dos lineas, separando nombre y color designado por una coma) y el color que va a iniciar a colocar fichas (tercer linea).
# leerColoresYJugadores: FileObject -> Tuple[Dict[String, String], String]
def leerColoresYJugadores(archivo) -> tuple[dict[str, str], str]:
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
# leerJugadas: FileObject -> String -> List[Tuple[String, String]]
def leerJugadas(archivo, colorInicial: str) -> list[tuple[str, str]]:
  jugadas = []
  colorActual = colorInicial

  # Recorriendo las lineas del archivo una a una para crear el formato de tupla anterior mencionado.
  for linea in archivo:
    jugadas.append((colorActual, removerSecuenciaDeEscape(linea)))

    colorActual = 'N' if colorActual == 'B' else 'B'

  return jugadas

# Abre el archivo y declara las variables de los jugadores, las jugadas y el color inicial, luego cierra el archivo.
# leerArchivoEntrada: String -> Tuple[Dict[String, String], List[Tuple[String, String]]]
def leerArchivoEntrada(nombreArchivo: str) -> tuple[dict[str, str], list[tuple[str, str]]]:
  archivo = open(nombreArchivo, 'r')

  (jugadores, colorInicial) = leerColoresYJugadores(archivo)
  jugadas = leerJugadas(archivo, colorInicial)

  archivo.close()

  return jugadores, jugadas

# Funcion auxiliar para desestructurar el formato de la jugada en color, indice de la columna e indice de la fila.
# desestructurarJugada: Tuple[String, String] -> Tuple[String, Int, Int]
def desestructurarJugada(jugada: tuple[str, str]) -> tuple[str, int, int]:
  (colorDelJugador, posicionDeLaJugada) = jugada
  indiceDeLaColumna = ord(posicionDeLaJugada[0]) - ord('A')
  indiceDeLaFila = int(posicionDeLaJugada[1]) - 1

  return colorDelJugador, indiceDeLaFila, indiceDeLaColumna

# Verifica si la posicion de la jugada ya esta ocupada. En ese caso, arroja una excepcion.
# controlarJugadaRepetida: List[List[String]] -> Tuple[String, String] -> None
def controlarJugadaRepetida(tablero: list[list[str]], jugada: tuple[str, str]) -> None:
  (_, indiceDeLaFila, indiceDeLaColumna) = desestructurarJugada(jugada)
  if tablero[indiceDeLaFila][indiceDeLaColumna] != " ":
    raise Exception(f'La posicion {jugada[1]} ya esta ocupada')

# Determina si la posicion de la jugada coincide con tener al menos una ficha del oponente alrededor de la nueva ficha,
# si no, es una jugada invalida.
# Tambien determina si hay una ficha aliada que encierre a la enemiga para poder cambiar el color y validar el movimiento.
# Si la jugada es invalida, se produce una excepcion.
# controlarJugadasValidas: List[List[String]] -> Tuple[String, String] -> Tuple[Int, Int]
def controlarJugadasValidas(tablero: list[list[str]], jugada: tuple[str, str]) -> list[tuple[int, int]]:
  (colorDelJugador, indiceDeLaFila, indiceDeLaColumna) = desestructurarJugada(jugada)
  colorDelOponente = 'N' if colorDelJugador == 'B' else 'B'
  hayOponenteAlrededor = False
  hayFichasEncerradas = False

  fichasEncerradas = []
  # Recorrer todas las posiciones del tablero que estan alrededor de la jugada realizada.
  for i in range(-1, 2):
    for j in range(-1, 2):
      # Quitando el caso de verificar la posicion de la jugada, vemos las posiciones de alrededor.
      if i != 0 or j != 0:
        indiceDeLaFilaAVerificar = indiceDeLaFila + i
        indiceDeLaColumnaAVerificar = indiceDeLaColumna + j

        # Verificando que las posiciones a comparar no se salgan de los parametros del tablero.
        seSaleDelTablero = indiceDeLaFilaAVerificar >= 8 or indiceDeLaFilaAVerificar < 0 or indiceDeLaColumnaAVerificar >= 8 or indiceDeLaColumnaAVerificar < 0

        fichasEnemigas = []
        # Recorriendo filas, columnas y diagonales mientras haya una ficha enemiga, para determinar si al final
        # de todas las fichas hay una aliada que encierre las enemigas y poder validar la jugada.
        while not seSaleDelTablero and tablero[indiceDeLaFilaAVerificar][indiceDeLaColumnaAVerificar] == colorDelOponente:
          fichasEnemigas.append((indiceDeLaFilaAVerificar, indiceDeLaColumnaAVerificar))

          # Avanzar en cada direccion
          indiceDeLaFilaAVerificar += i
          indiceDeLaColumnaAVerificar += j

          seSaleDelTablero = indiceDeLaFilaAVerificar >= 8 or indiceDeLaFilaAVerificar < 0 or indiceDeLaColumnaAVerificar >= 8 or indiceDeLaColumnaAVerificar < 0
        
        # Hay al menos una ficha enemiga adyacente en esa direccion?
        if fichasEnemigas != []:
          hayOponenteAlrededor = True
        
          # Hay una ficha aliada que encierra a las enemigas en esa direccion?
          if not seSaleDelTablero and tablero[indiceDeLaFilaAVerificar][indiceDeLaColumnaAVerificar] == colorDelJugador:
            hayFichasEncerradas = True
            fichasEncerradas += fichasEnemigas

  # Tirar excepciones si la jugada es invalida
  if not hayOponenteAlrededor:
    raise Exception(f'La posicion {jugada[1]} no tiene ningua ficha del oponente alrededor.')

  if not hayFichasEncerradas:
    raise Exception(f'La posicion {jugada[1]} no encierra fichas del oponente.')
  
  return fichasEncerradas

# Dada una jugada valida, aplicar la misma al tablero.
# aplicarJugada: List[List[String]] -> Tuple[String, String] -> None
def aplicarJugada(tablero: list[list[str]], jugada: tuple[str, str], fichasEncerradas: list[tuple[int, int]]) -> None:
  (colorDelJugador, indiceDeLaFila, indiceDeLaColumna) = desestructurarJugada(jugada)

  # Ficha colocada
  tablero[indiceDeLaFila][indiceDeLaColumna] = colorDelJugador

  # Cambiar fichas encerradas
  for (i, j) in fichasEncerradas:
    tablero[i][j] = colorDelJugador

# Verificar que si o si era necesario saltar el turno.
# salteoDeJugada: List[List[String]] -> String -> None
def salteoDeJugada(tablero: list[list[str]], colorDelJugador) -> None:
  # Recorriendo una imitacion del tablero para obtener los indices del mismo
  for nroFila in range(0, 8):
    for nroColumna in range(0, 8):
      # Restringiendo las verificaciones a las posiciones del tablero que tengan fichas.
      if tablero[nroFila][nroColumna] != ' ':
        # Intentar jugadas en cada posicion alrededor de la ficha.
        for i in range(-1, 2):
          for j in range(-1, 2):
            # Sumando/restando al indice de la jugada del tablero para poder alcanzar las posiciones alrededor del mismo.
            indiceDeLaFilaAVerificar = nroFila + i
            indiceDeLaColumnaAVerificar = nroColumna + j
            
            # Verificando que las posiciones a comparar no se salgan de los parametros del tablero.
            seSaleDelTablero = indiceDeLaFilaAVerificar >= 8 or indiceDeLaFilaAVerificar < 0 or indiceDeLaColumnaAVerificar >= 8 or indiceDeLaColumnaAVerificar < 0

            # Solo verificar si la jugada es posible en posiciones vacias.
            if not seSaleDelTablero and tablero[indiceDeLaFilaAVerificar][indiceDeLaColumnaAVerificar] == ' ':
              letraColumna = chr(indiceDeLaColumnaAVerificar + ord('A')) # Convertir indice a letra
              jugada = (colorDelJugador, letraColumna + str(indiceDeLaFilaAVerificar + 1)) # Armar jugada para probar si hubiera sido valida

              try:
                # Intentar jugada
                controlarJugadasValidas(tablero, jugada)
              except:
                # Si tira excepcion, la jugada no era posible y el salto de turno es valido.
                pass
              else:
                # Si no se produce una excepcion, se encontro una jugada que se podria haber realizado
                raise Exception(f'Se podria haber colocado una ficha en la posicion {jugada[1]}.')

# Verifica cada jugada (llamando a las respectivas funciones de cada regla) y, si es valida, aplica el resultado de la misma al tablero.
# simularJuego: List[List[String]] -> List[Tuple[String, String]] -> None
def simularJuego(tablero: list[list[str]], jugadas: list[tuple[str, str]]) -> None:
  for jugada in jugadas:
    (color, posicion) = jugada
    # Verificar si se salteo el turno
    if posicion != '':
      # Controlar reglas si no se salteo
      controlarJugadaRepetida(tablero, jugada)
      fichasEncerradas = controlarJugadasValidas(tablero, jugada)
      aplicarJugada(tablero, jugada, fichasEncerradas)
    else:
      # Controlar que no habia jugada posible si se salteo
      salteoDeJugada(tablero, color)
    
    # TODO: remove this debugging stuff
    print(jugada)
    imprimirTablero(tablero)
    print()

# Recibe el tablero y devuelve el color del jugador ganador, basado en la cantidad de fichas de cada color
# determinarGanador: List[List[String]] -> String
def determinarGanador(tablero: list[list[str]]) -> str:
  pass

# Muestra el tablero con el formato adecuado
# imprimirTablero: List[List[String]] -> None
def imprimirTablero(tablero: list[list[str]]) -> None:
  print('  A B C D E F G H')
  for i in range(8):
    nroFila = i + 1
    contenidoFila = ' '.join(tablero[i])
    print(f'{nroFila} {contenidoFila} {nroFila}')
  print('  A B C D E F G H')

# Construye el tablero con las cuatro piezas iniciales en el centro.
# construitTableroInicial: None -> List[List[String]]
def construirTableroInicial() -> list[list[str]]:
  tablero = []
  for i in range(8):
    fila = []
    for j in range(8):
      if (i == j == 3) or (i == j == 4):
        fila.append("B")
      elif (i == 3 and j == 4) or (i == 4 and j == 3):
        fila.append("N")
      else:
        fila.append(' ')
    tablero.append(fila)

  return tablero

# Punto de entrada del programa. Llama a las funciones para crea el tablero, leer la entrada del usuario y simular el juego. Si hay errores,
# se le informa al usuario y se muestra el tablero anterior a esa jugada, si no, se muestra el tablero final con el ganador.
# main: None -> None
def main() -> None:
  nombreArchivo = input('Ingrese el nombre del archivo de entrada: ')
  try:
    _, jugadas = leerArchivoEntrada(nombreArchivo)
  except FileNotFoundError:
    print('No se encontro el archivo.')
  else:
    tablero = construirTableroInicial()

    try:
      simularJuego(tablero, jugadas)
    except Exception as e:
      imprimirTablero(tablero)
      print(str(e))
    else:
      imprimirTablero(tablero)
      determinarGanador(tablero)
      # mostrar ganador

# No ejecutar codigo al importar funciones desde este archivo
if __name__ == '__main__':
  main()
