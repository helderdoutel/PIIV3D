import random
from Elevador import Elevador
from Passageiro import Passageiro
import time
import datetime
import numpy as np
import glfw
import OpenGL
OpenGL.ERROR_CHECKING = False
OpenGL.FULL_LOGGING = True
from OpenGL.GL import *
from OpenGL.GLU import *

verticesOrigem = (
    (0.50, -0.50, -0.50),
    (0.50, 0.50, -0.50),
    (-0.50, 0.50, -0.50),
    (-0.50, -0.50, -0.50),
    (0.50, -0.50, 0.50),
    (0.50, 0.50, 0.50),
    (-0.50, -0.50, 0.50),
    (-0.50, 0.50, 0.50)
)

esferaOrigem = (1, 25, 25)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)


def gerar_passageiros(quantidade, espacamento_inicial):
    espacamento = espacamento_inicial
    elevadores = []
    for i in range(quantidade):
        tupla = tuple([(i[0] + espacamento, i[1], i[2])
                       for i in verticesOrigem])
        elevador = Elevador()
        elevador.set_vertices(tupla)
        elevadores.append(elevador)
        # print(tupla)
        espacamento += espacamento_inicial
    return elevadores


def gerar_passageiros(funcionarios_total=1000, max_por_min=30, min_por_min=0):
    hora_chegada = datetime.datetime(2018, 1, 1, 8, 0, 0, 0)
    # datetime.datetime.now() - datetime.timedelta(minutes=15)
    fila = []

    # hr de chegada individual
    while funcionarios_total > 0:
        chegou = (np.random.poisson(max_por_min, 1))[0]
        # random.randint(min_por_min, max_por_min)
        if (funcionarios_total - chegou) < 0:
            chegou = funcionarios_total
        funcionarios_total -= chegou
        if chegou > 0:
            tec = float(60) / float(chegou)
        else:
            tec = 0
        while chegou > 0:
            passageiro = passageiro(hora_chegada=hora_chegada)
            fila.append(passageiro)
            hora_chegada = hora_chegada + datetime.timedelta(seconds=tec)
            chegou -= 1
        if chegou == 0:
            hora_chegada = hora_chegada + datetime.timedelta(minutes=1)

print('teste')
