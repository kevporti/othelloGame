# ----------- DISEÑO DE DATOS -----------
# El TABLERO esta representado por una lista de filas, siendo cada fila una lista de casillas, y cada casilla representada con un string.
# Dentro de cada casilla luego se guardara la inicial del color de la ficha que esta colocada ahi, sino estara un string con un espacio (" ") representando
# que no se ha hecho una jugada en esa posicion.
# Los COLORES se representan como strings, utilizando las iniciales de los mismos ('B' para blanco y 'N' para negro).
# El conjunto de las JUGADAS se representan mediante una lista de tuplas, donde cada tupla es una jugada que contiene el color de los 
# jugadores dependiendo del turno de cada uno, y su jugada correspondiente.
# Los JUGADORES se representan utilizando un diccionario, en el cual las claves son los colores que les corresponde y los
# valores asociados son los nombres de los jugadores.
# ---------------------------------------

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

# Dado el nombre del archivo, llama a las funciones necesarias para leer el mismo. Devuelve una tupla que contiene un diccionario que indica
# el color asignado a cada jugador, y una lista de jugadas (cada jugada representada por una tupla)
# leerArchivoEntrada: String -> Tuple[Dict[String, String], List[Tuple[String, String]]]
def leerArchivoEntrada(nombreArchivo: str) -> tuple[dict[str, str], list[tuple[str, str]]]:
  archivo = open(nombreArchivo, 'r')

  (jugadores, colorInicial) = leerColoresYJugadores(archivo)
  jugadas = leerJugadas(archivo, colorInicial)

  archivo.close()

  return (jugadores, jugadas)

# Funcion auxiliar para desestructurar el formato de la jugada en color, indice de la columna e indice de la fila.
# desestructurarJugada: Tuple[String, String] -> Tuple[String, Int, Int]
def desestructurarJugada(jugada: tuple[str, str]) -> tuple[str, int, int]:
  (colorDelJugador, posicionDeLaJugada) = jugada
  indiceDeLaColumna = ord(posicionDeLaJugada[0]) - ord('A') # convertir la letra de la columna en el indice adecuado
  indiceDeLaFila = int(posicionDeLaJugada[1]) - 1

  return (colorDelJugador, indiceDeLaFila, indiceDeLaColumna)

# Validar que la jugada este dentro del tablero
# validarJugadaDentroTablero: Tuple[String, String] -> Dict[String, Boolean | String]
def validarJugadaDentroTablero(jugada: tuple[str, str]) -> dict[str, bool | str]:
  (color, indiceDeLaFila, indiceDeLaColumna) = desestructurarJugada(jugada)
  
  if indiceDeLaFila >= 8 or indiceDeLaFila < 0 or indiceDeLaColumna >= 8 or indiceDeLaColumna < 0:
    return {
      'jugadaValida': False,
      'color': color, 
      'error': f'La posicion {jugada[1]} se sale del tablero.'
    }
  
  return {
    'jugadaValida': True,
  }

# Verifica si la posicion de la jugada ya esta ocupada.
# controlarJugadaRepetida: List[List[String]] -> Tuple[String, String] -> Dict[String, Boolean | String]
def controlarJugadaRepetida(tablero: list[list[str]], jugada: tuple[str, str]) -> dict[str, bool | str]:
  (color, indiceDeLaFila, indiceDeLaColumna) = desestructurarJugada(jugada)

  if tablero[indiceDeLaFila][indiceDeLaColumna] != " ":
    return {
      'jugadaValida': False, 
      'color': color, 
      'error': f'La posicion {jugada[1]} ya esta ocupada.'
    }

  return {
    'jugadaValida': True,
  }

# Determina si la casilla elegida en la jugada coincide con tener al menos una ficha del oponente alrededor de la nueva ficha
# y si, a su vez, hay una ficha aliada en direccion vertical, horizontal o diagonal que, junto con la ficha a colocar, encierre fichas enemigas.
# controlarJugadaValida: List[List[String]] -> Tuple[String, String] -> Dict[String, Boolean | String | List[Tuple[Int, Int]]]
def controlarJugadaValida(tablero: list[list[str]], jugada: tuple[str, str]) -> dict[str, bool | str | list[tuple[int, int]]]:
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

  if not hayOponenteAlrededor:
    return {
      'jugadaValida': False,
      'color': colorDelJugador,
      'error': f'La posicion {jugada[1]} no tiene ningua ficha del oponente alrededor.'
    }

  if not hayFichasEncerradas:
    return {
      'jugadaValida': False,
      'color': colorDelJugador,
      'error': f'La posicion {jugada[1]} no encierra fichas del oponente.'
    }
  
  return {
    'jugadaValida': True,
    'fichasEncerradas': fichasEncerradas
  }

# Dada una jugada valida, y las fichas que fueron encerradas durante la misma, la aplica sobre el tablero.
# aplicarJugada: List[List[String]] -> Tuple[String, String] -> None
def aplicarJugada(tablero: list[list[str]], jugada: tuple[str, str], fichasEncerradas: list[tuple[int, int]]) -> None:
  (colorDelJugador, indiceDeLaFila, indiceDeLaColumna) = desestructurarJugada(jugada)

  # Ficha que el jugador acaba de colocar
  tablero[indiceDeLaFila][indiceDeLaColumna] = colorDelJugador

  # Cambiar el color de las fichas enemigas encerradas
  for (i, j) in fichasEncerradas:
    tablero[i][j] = colorDelJugador

# Verificar que el jugador que salteo el turno no tenia otra opcion, es decir, no podia realizar ninguna jugada valida.
# controlarSalteoDeJugada: List[List[String]] -> String -> Dict[String, Boolean | String]
def controlarSalteoDeJugada(tablero: list[list[str]], colorDelJugador: str) -> dict[str, bool | str]:
  seEncontroJugadaPosible = False

  # Recorrer posiciones del tablero
  nroFila = 0
  while nroFila < 8 and not seEncontroJugadaPosible:
    nroColumna = 0
    while nroColumna < 8 and not seEncontroJugadaPosible:
      # Solo verificar jugadas posibles alrededor de casillas que tengan fichas
      if tablero[nroFila][nroColumna] != ' ':
        # Intentar jugadas en cada posicion alrededor de la ficha:
        i = -1
        while i < 2 and not seEncontroJugadaPosible:
          j = -1
          while j < 2 and not seEncontroJugadaPosible:
            # Sumar/restar a los indices de la casilla para poder alcanzar las posiciones alrededor de la misma
            indiceDeLaFilaAVerificar = nroFila + i
            indiceDeLaColumnaAVerificar = nroColumna + j
            
            # Verificar que las posiciones a comparar no se salgan del rango de indices del tablero.
            seSaleDelTablero = indiceDeLaFilaAVerificar >= 8 or indiceDeLaFilaAVerificar < 0 or indiceDeLaColumnaAVerificar >= 8 or indiceDeLaColumnaAVerificar < 0

            # Solo verificar si la jugada es posible en posiciones vacias ya que no es posible colocar una ficha en una casilla ocupada
            if not seSaleDelTablero and tablero[indiceDeLaFilaAVerificar][indiceDeLaColumnaAVerificar] == ' ':
              letraColumna = chr(indiceDeLaColumnaAVerificar + ord('A')) # Convertir indice a letra
              jugada = (colorDelJugador, letraColumna + str(indiceDeLaFilaAVerificar + 1)) # Armar jugada para probar si hubiera sido valida

              # Intentar jugada
              resultado = controlarJugadaValida(tablero, jugada)
              if resultado['jugadaValida']:
                # Si la jugada es valida, se encontro una jugada que se podria haber realizado y lo reportamos como error
                resultado = {
                  'jugadaValida': False,
                  'color': colorDelJugador,
                  'error': f'Se podria haber colocado una ficha en la posicion {jugada[1]}.'
                }
                # Evitar seguir probando jugadas en otras casillas
                seEncontroJugadaPosible = True

            j += 1
          i += 1
      nroColumna += 1
    nroFila += 1
  
  if seEncontroJugadaPosible:
    return resultado

  return {
    'jugadaValida': True
  }


# Verifica cada jugada (llamando a las respectivas funciones de cada regla) y, si es valida, aplica el resultado de la misma al tablero.
# simularJuego: List[List[String]] -> List[Tuple[String, String]] -> Dict[String, Boolean | String]
def simularJuego(tablero: list[list[str]], jugadas: list[tuple[str, str]]) -> dict[str, str | bool]:
  i = 0
  while i < len(jugadas) and (i == 0 or resultado['jugadaValida']):
    jugada = jugadas[i]
    (color, posicion) = jugada
    # Verificar si se salteo el turno
    if posicion != '':
      # Controlar reglas si no se salteo
      resultado = validarJugadaDentroTablero(jugada)
      if not resultado['jugadaValida']:
        continue

      resultado = controlarJugadaRepetida(tablero, jugada)
      if not resultado['jugadaValida']:
        continue

      resultado = controlarJugadaValida(tablero, jugada)
      if not resultado['jugadaValida']:
        continue

      aplicarJugada(tablero, jugada, resultado['fichasEncerradas'])
    else:
      # Controlar que no habia jugada posible si se salteo
      resultado = controlarSalteoDeJugada(tablero, color)
      if not resultado['jugadaValida']:
        continue

    i += 1 
    
  # Una vez terminados los movimientos ingresados por el usuario, si no se produjo ningun error, comprobar si la partida quedo sin terminar o no.
  resultado['partidaIncompleta'] = False
  resultado['dobleSalteo'] = None
  if resultado['jugadaValida']:
    colorTurnoSiguiente = 'N' if color == 'B' else 'B'
    # Simular un salteo de jugada para saber si una jugada era posible.
    resultado = controlarSalteoDeJugada(tablero, colorTurnoSiguiente)
    
    if not resultado['jugadaValida']:
      # Si esa simulacion da como resultado que es una jugada invalida, entonces es porque habia alguna jugada posible y, por lo tanto, la partida esta incompleta.
      resultado['partidaIncompleta'] = True
      resultado['dobleSalteo'] = False
    else:
      # Si saltear es una jugada valida, entonces hay que verificar un segundo salto de turno para ver que no se puede continuar jugando.
      colorTurnoSiguiente = 'N' if colorTurnoSiguiente == 'B' else 'B'
      # Simular un salteo de jugada para saber si una jugada era posible.
      resultado = controlarSalteoDeJugada(tablero, colorTurnoSiguiente)
      
      if not resultado['jugadaValida']:
        # Si esa simulacion da como resultado que es una jugada invalida, entonces es porque habia alguna jugada posible y, por lo tanto, la partida esta incompleta.
        resultado['partidaIncompleta'] = True
        resultado['dobleSalteo'] = True
      else:
        # Si saltear es una jugada valida, entonces la partida no esta incompleta.
        resultado['partidaIncompleta'] = False
        resultado['dobleSalteo'] = None

  if not resultado['jugadaValida']:
    return {
      'partidaValida': False,
      'partidaIncompleta': resultado['partidaIncompleta'],
      'dobleSalteo': resultado['dobleSalteo'],
      'color': resultado['color'],
      'error': resultado['error']
    }

  return {
    'partidaValida': True
  }

# Recibe el tablero y devuelve el color del jugador ganador (o indica que hubo empate si corresponde), basado en la cantidad de fichas de cada color
# determinarGanador: List[List[String]] -> String
def determinarGanador(tablero: list[list[str]]) -> str:
  fichasBlancas = 0
  fichasNegras = 0

  # Contar fichas de cada color
  for linea in tablero:
    for casilla in linea:
      if casilla == 'B':
        fichasBlancas += 1
      elif casilla == 'N':
        fichasNegras += 1
  
  # Devolver resultado
  if fichasBlancas < fichasNegras:
    return 'N'
  elif fichasBlancas > fichasNegras:
    return 'B'
  else:
    return 'empate'

# Construye el tablero con las cuatro piezas iniciales en el centro.
# construirTableroInicial: None -> List[List[String]]
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

# Muestra el tablero con el formato adecuado
# imprimirTablero: List[List[String]] -> None
def imprimirTablero(tablero: list[list[str]]) -> None:
  print('  | A B C D E F G H |')
  print('--+-----------------+--')
  for i in range(8):
    nroFila = i + 1
    contenidoFila = ' '.join(tablero[i])
    print(f'{nroFila} | {contenidoFila} | {nroFila}')
  print('--+-----------------+--')
  print('  | A B C D E F G H |')

# Punto de entrada del programa. Llama a las funciones para crea el tablero, leer la entrada del usuario y simular el juego. Si hay errores,
# se le informa al usuario y se muestra el tablero anterior a esa jugada, si no, se muestra el tablero final con el ganador.
# main: None -> None
def main() -> None:
  nombreArchivo = input('Ingrese la ruta del archivo de entrada: ')
  try:
    (jugadores, jugadas) = leerArchivoEntrada(nombreArchivo)
  except FileNotFoundError:
    print('No se encontro el archivo.')
  else:
    tablero = construirTableroInicial()

    resultado = simularJuego(tablero, jugadas)

    if resultado['partidaValida']:
      imprimirTablero(tablero)
      ganador = determinarGanador(tablero)
      if ganador != 'empate':
        print(f'El ganador es: {jugadores[ganador]}.')
      else:
        print('Ha habido un empate.')
    else:
      imprimirTablero(tablero)
      turnoDeJugador = jugadores[resultado['color']]
      error = resultado['error']

      if resultado['partidaIncompleta']:
        if resultado['dobleSalteo']:
          turnoSalteado = jugadores['N' if resultado['color'] == 'B' else 'B']
          print(f'Partida incompleta. Era el turno de {turnoSalteado} y se podia saltear ese turno y luego {turnoDeJugador} tendria al menos un movimiento posible: {error}')
        else:
          print(f'Partida incompleta. Era el turno de {turnoDeJugador} y aun habia uno o mas movimientos posibles: {error}')

      else:
        print(f'Jugada invalida ejecutada por {turnoDeJugador}: {error}')

# No ejecutar codigo al importar funciones desde este archivo
if __name__ == '__main__':
  main()
