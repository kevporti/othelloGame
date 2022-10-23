import pytest
from index import *

def test_removerSecuenciaDeEscape():
  assert removerSecuenciaDeEscape('\nhola') == 'hola'
  assert removerSecuenciaDeEscape('hola\n') == 'hola'

def test_leerColoresYJugadores():
  archivo = open('archivosTests/testUno.txt', 'r')

  assert leerColoresYJugadores(archivo) == ({'N': 'Kevin', 'B': 'Juan'}, 'N')

  archivo.close()

def test_leerJugadas():
  archivo = open('archivosTests/testUno.txt', 'r')
  (_, colorInicial) = leerColoresYJugadores(archivo)

  assert leerJugadas(archivo, colorInicial) == [('N', 'D3'), ('B', 'E3'), ('N', 'F4'), ('B', 'G3')]

  archivo.close()

def test_leerArchivoEntrada():
  assert leerArchivoEntrada('archivosTests/testUno.txt') == ({'N': 'Kevin', 'B': 'Juan'}, [('N', 'D3'), ('B', 'E3'), ('N', 'F4'), ('B', 'G3')])

def test_desestructurarJugada():
  jugadaUno = ('N', 'D3')
  jugadaDos = ('B', 'H7')
  jugadaTres = ('B', 'A1')

  assert desestructurarJugada(jugadaUno) == ('N', 2, 3)
  assert desestructurarJugada(jugadaDos) == ('B', 6, 7)
  assert desestructurarJugada(jugadaTres) == ('B', 0, 0)

def test_controlarJugadaRepetida():
  tablero = construirTableroInicial()
  jugada = ('B', 'A1')

  assert controlarJugadaRepetida(tablero, jugada) == None

  tablero[0][0] = 'B'

  with pytest.raises(Exception) as err:
    controlarJugadaRepetida(tablero, jugada)

  assert str(err.value) == f'La posicion {jugada[1]} ya esta ocupada'

def test_controlarJugadasValidas():
  tablero = construirTableroInicial()

  # Ninguna ficha alrededor
  jugada = ('B', 'A1')
  with pytest.raises(Exception) as err:
    controlarJugadaValidas(tablero, jugada)
  assert str(err.value) == f'La posicion {jugada[1]} no tiene ningua ficha del oponente alrededor.'

  # Ficha aliada alrededor pero no enemiga
  jugada = ('B', 'C3')
  with pytest.raises(Exception) as err:
    controlarJugadaValidas(tablero, jugada)
  assert str(err.value) == f'La posicion {jugada[1]} no tiene ningua ficha del oponente alrededor.'

  # Ficha enemiga alrededor pero no encierra
  jugada = ('B', 'C6')
  with pytest.raises(Exception) as err:
    controlarJugadaValidas(tablero, jugada)
  assert str(err.value) == f'La posicion {jugada[1]} no encierra fichas del oponente.'

  # Ficha enemiga alrededor y encierra. Devuelve coordenadas de la ficha encerrada.
  jugada = ('B', 'C5')
  assert controlarJugadaValidas(tablero, jugada) == [(4, 3)]

def test_imprimirTablero():
  tablero = construirTableroInicial()

  assert imprimirTablero(tablero) == None
