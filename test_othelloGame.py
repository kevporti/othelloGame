import pytest
from index import *

def test_removerSecuenciaDeEscape():
  assert removerSecuenciaDeEscape('\nhola') == 'hola'
  assert removerSecuenciaDeEscape('hola\n') == 'hola'

def test_leerColoresYJugadores():
  archivoTestUno = open('archivosTests/testUno.txt', 'r')
  archivoTestDos = open('archivosTests/testDos.txt', 'r')
  archivoTestTres = open('archivosTests/testTres.txt', 'r')

  assert leerColoresYJugadores(archivoTestUno) == ({
    'N': 'Kevin',
    'B': 'Juan'
  }, 'N')
  assert leerColoresYJugadores(archivoTestDos) != ({
    'B': 'Facu',
    'N': 'Martin'
  }, 'B')
  assert leerColoresYJugadores(archivoTestTres) == ({
    'B': 'Pedro',
    'N': 'Julia'
  }, 'N')

  archivoTestUno.close()
  archivoTestDos.close()
  archivoTestTres.close()

def test_leerJugadas():
  archivoTestUno = open('archivosTests/testUno.txt', 'r')
  archivoTestDos = open('archivosTests/testDos.txt', 'r')
  archivoTestTres = open('archivosTests/testTres.txt', 'r')
  (_, colorInicialTestUno) = leerColoresYJugadores(archivoTestUno)
  (_, colorInicialTestDos) = leerColoresYJugadores(archivoTestDos)
  (_, colorInicialTestTres) = leerColoresYJugadores(archivoTestTres)

  assert leerJugadas(archivoTestUno, colorInicialTestUno) == [('N', 'D3'), ('B', 'E3'), ('N', 'F4'), ('B', 'G3')]
  assert leerJugadas(archivoTestDos, colorInicialTestDos) != [('N', 'E6'), ('B', 'F4'), ('N', 'C3'), ('B', 'C4'), ('N', 'D3'), ('B', 'D6')]
  assert leerJugadas(archivoTestTres, colorInicialTestTres) != [('B', 'D3'), ('N', 'E3'), ('B', 'F3'), ('N', 'E2'), ('B', 'D1'), ('N', 'G3'), ('B', 'H3'), ('N', 'C3')]

  archivoTestUno.close()
  archivoTestDos.close()
  archivoTestTres.close()

def test_leerArchivoEntrada():
  assert leerArchivoEntrada('archivosTests/testUno.txt') == ({
    'N': 'Kevin', 
    'B': 'Juan'
  }, [('N', 'D3'), ('B', 'E3'), ('N', 'F4'), ('B', 'G3')])
  assert leerArchivoEntrada('archivosTests/testUno.txt') != ({
    'N': 'Juan', 
    'B': 'Kevin'
  }, [('N', 'D3'), ('B', 'E3'), ('N', 'F4'), ('B', 'G3')])
  assert leerArchivoEntrada('archivosTests/testUno.txt') != ({
    'N': 'Kevin', 
    'B': 'Kevin'
  }, [('B', 'D3'), ('N', 'E3'), ('B', 'F4'), ('N', 'G3')])

def test_desestructurarJugada():
  jugadaUno = ('N', 'D3')
  jugadaDos = ('B', 'H7')
  jugadaTres = ('B', 'A1')

  assert desestructurarJugada(jugadaUno) == ('N', 2, 3)
  assert desestructurarJugada(jugadaDos) == ('B', 6, 7)
  assert desestructurarJugada(jugadaTres) == ('B', 0, 0)
  assert desestructurarJugada(jugadaTres) != ('B', 1, 1)

def test_validarJugadaDentroTablero():
  jugadaUno = ('N', 'D3')
  jugadaDos = ('B', 'H9')
  jugadaTres = ('B', 'Z1')

  assert validarJugadaDentroTablero(jugadaUno) == {
    'jugadaValida': True
  }
  assert validarJugadaDentroTablero(jugadaDos) == {
    'jugadaValida': False, 
    'color': jugadaDos[0], 
    'error': f'La posicion {jugadaDos[1]} se sale del tablero.'
  }
  assert validarJugadaDentroTablero(jugadaTres) != {
    'jugadaValida': True
  }
  assert validarJugadaDentroTablero(jugadaTres) == {
    'jugadaValida': False, 
    'color': jugadaTres[0], 
    'error': f'La posicion {jugadaTres[1]} se sale del tablero.'
  }

def test_controlarJugadaRepetida():
  tablero = construirTableroInicial()
  jugadaUno = ('B', 'A1')
  jugadaDos = ('N', 'H6')
  jugadaTres = ('N', 'D4')

  assert controlarJugadaRepetida(tablero, jugadaUno) == {
    'jugadaValida': True
  }
  assert controlarJugadaRepetida(tablero, jugadaDos) == {
    'jugadaValida': True
  }

  tablero[0][0] = 'N'

  controlarJugadaRepetida(tablero, jugadaUno) == {
    'jugadaValida': False,
    'color': jugadaUno[0],
    'error': f'La posicion {jugadaUno[1]} ya esta ocupada.'
  }
  controlarJugadaRepetida(tablero, jugadaTres) == {
    'jugadaValida': False,
    'color': jugadaTres[0],
    'error': f'La posicion {jugadaTres[1]} ya esta ocupada.'
  }

def test_controlarJugadasValidas():
  tablero = construirTableroInicial()

  # Ninguna ficha alrededor
  jugadaUno = ('B', 'A1')
  assert controlarJugadaValidas(tablero, jugadaUno) == {
    'jugadaValida': False, 
    'color': jugadaUno[0], 
    'error': f'La posicion {jugadaUno[1]} no tiene ningua ficha del oponente alrededor.'
  }

  # Ficha aliada alrededor pero no enemiga
  jugadaDos = ('B', 'C3')
  assert controlarJugadaValidas(tablero, jugadaDos) == {
    'jugadaValida': False, 
    'color': jugadaDos[0], 
    'error': f'La posicion {jugadaDos[1]} no tiene ningua ficha del oponente alrededor.'
  }

  # Ficha enemiga alrededor pero no encierra
  jugadaTres = ('B', 'C6')
  assert controlarJugadaValidas(tablero, jugadaTres) == {
    'jugadaValida': False, 
    'color': jugadaTres[0], 
    'error': f'La posicion {jugadaTres[1]} no encierra fichas del oponente.'
  }

  # Ficha enemiga alrededor y encierra. Devuelve coordenadas de la ficha encerrada.
  jugada = ('B', 'C5')
  assert controlarJugadaValidas(tablero, jugada) == {
    'jugadaValida': True, 
    'fichasEncerradas': [(4, 3)]
  }

def test_determinarGanador():
  tablero = construirTableroInicial()
  
  assert determinarGanador(tablero) == 'empate'
  tablero[3][2:4] = ['N', 'N']
  assert determinarGanador(tablero) == 'N'

  tablero = construirTableroInicial()
  tablero[4][2:4] = ['B', 'B']
  assert determinarGanador(tablero) == 'B'

def test_controlarSalteoDeJugada():
  tablero = construirTableroInicial()
  tableroAntesDelSaltoDeTurno = [('B', 'A3'), ('B', 'B3'), ('B', 'C3'), ('B', 'D4'), ('B', 'E3'), ('B', 'F3'), ('B', 'G3'), ('B', 'E1'), ('B', 'E2'), ('B', 'C4'), ('B', 'C5'), ('B', 'D3'), ('B', 'D4'), ('B', 'D5'), ('B', 'E4'), ('B', 'E5'), ('B', 'F4'), ('B', 'F2'), ('N', 'H3'), ('N', 'H4'), ('N', 'H5')]

  for jugada in tableroAntesDelSaltoDeTurno:
    (colorDelJugador, indiceDeLaFila, indiceDeLaColumna) = desestructurarJugada(jugada)
    tablero[indiceDeLaFila][indiceDeLaColumna] = colorDelJugador

  assert controlarSalteoDeJugada(tablero, 'N') == {
    'jugadaValida': True
  }
  assert controlarSalteoDeJugada(tablero, 'B') == {
    'jugadaValida': True
  }

  tablero[2][0] = ' '

  assert controlarSalteoDeJugada(tablero, 'N') == {
    'jugadaValida': False,
    'color': 'N',
    'error': f'Se podria haber colocado una ficha en la posicion A3.'
  }
  assert controlarSalteoDeJugada(tablero, 'B') == {
    'jugadaValida': True
  }

def test_construirTableroInicial():
  tablero = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', 'B', 'N', ' ', ' ', ' '], [' ', ' ', ' ', 'N', 'B', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

  assert construirTableroInicial() == tablero

def test_simularJuego():
  archivoTestUno = 'archivosTests/testUno.txt'
  archivoTestDos = 'archivosTests/testDos.txt'
  archivoTestTres = 'archivosTests/testTres.txt'
  archivoTestCuatro = 'archivosTests/testCuatro.txt'
  (_, jugadasTestUno) = leerArchivoEntrada(archivoTestUno)
  (_, jugadasTestDos) = leerArchivoEntrada(archivoTestDos)
  (_, jugadasTestTres) = leerArchivoEntrada(archivoTestTres)
  (_, jugadasTestCuatro) = leerArchivoEntrada(archivoTestCuatro)

  tablero = construirTableroInicial()
  assert simularJuego(tablero, jugadasTestUno) == {
    'partidaValida': False, 
    'partidaIncompleta': True, 
    'color': 'N', 
    'error': 'Se podria haber colocado una ficha en la posicion E2.'
  }

  tablero = construirTableroInicial()
  assert simularJuego(tablero, jugadasTestDos) == {
    'partidaValida': True
  }

  assert simularJuego(construirTableroInicial(), jugadasTestTres) == {
    'partidaValida': False, 
    'partidaIncompleta': True, 
    'color': 'N', 
    'error': 'Se podria haber colocado una ficha en la posicion B3.'
  }

  tablero = construirTableroInicial()
  assert simularJuego(tablero, jugadasTestCuatro) == {
    'partidaValida': True
  }