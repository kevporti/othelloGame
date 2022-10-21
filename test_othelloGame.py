from index import *

def test_removerSecuenciaDeEscape():
  assert removerSecuenciaDeEscape('\nhola') == 'hola'
  assert removerSecuenciaDeEscape('hola\n') == 'hola'

def test_definirJugadoresYColores():
  archivo = open('juegoParadoPorDobleSkipGanadorB.txt', 'r')

  assert definirJugadoresYColores(archivo) == ({'N': 'Kevin', 'B': 'Juan'}, 'N')
  archivo.close()

def test_definirJugadas():
  archivo = open('juegoParadoPorDobleSkipGanadorB.txt', 'r')
  (_, colorInicial) = definirJugadoresYColores(archivo)

  assert definirJugadas(archivo, colorInicial) == [('N', 'D3'), ('B', 'E3'), ('N', 'F4'), ('B', 'G3'), ('N', 'F3'), ('B', 'C5'), ('N', 'H3'), ('B', 'F2'), ('N', 'C4'), ('B', 'C3'), ('N', 'E2'), ('B', 'E1'), ('N', 'B3'), ('B', 'H4'), ('N', 'H5'), ('B', 'A3')]
  archivo.close()

def test_desestructurarArchivo():
  assert desestructurarArchivo() == ({'N': 'Kevin', 'B': 'Juan'}, [('N', 'D3'), ('B', 'E3'), ('N', 'F4'), ('B', 'G3'), ('N', 'F3'), ('B', 'C5'), ('N', 'H3'), ('B', 'F2'), ('N', 'C4'), ('B', 'C3'), ('N', 'E2'), ('B', 'E1'), ('N', 'B3'), ('B', 'H4'), ('N', 'H5'), ('B', 'A3')])

def test_desestructurarJugada():
  jugadaUno = ('N', 'D3')
  jugadaDos = ('B', 'H7')
  jugadaTres = ('B', 'A1')

  assert desestructurarJugada(jugadaUno) == ('N', 2, 3)
  assert desestructurarJugada(jugadaDos) == ('B', 6, 7)
  assert desestructurarJugada(jugadaTres) == ('B', 0, 0)

'''
def test_controlarJugadaRepetida():
  tablero = []
  jugada = []

  assert controlarJugadaRepetida(tablero, jugada) ==
  '''