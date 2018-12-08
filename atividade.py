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

pessoaOrigem = (
    (0, -0.5, 0), # base esquerda superior
    (0.1, -0.5, 0), # base direita superior
    (0.1, -0.5, 0.1), # base direita inferior
    (0, -0.5, 0.1), # base esquerda inferior
    (0.05,1,0.1) #topo
)

pessoaArestas = (   
    (0,1),
    (1,2),
    (2,3),
    (3,0),
    (4,0),
    (4,1),
    (4,2),  
    (4,3)
)

chaoVertices = (
    (0, -0.5, -50),
    (50, -0.5, -50),
    (50, -0.5, 50),
    (0, -0.5, 50),
)

chaoArestas = (
    (0,1),
    (1,2),
    (2,3),
    (3,0),
)


#detecta colisao entre pessoa e elevador
def colisao(elevador,pessoa):
    if (pessoa[4][0] >= elevador[6][0] and pessoa[4][0] <= elevador[4][0] and pessoa[4][2] <= elevador[6][2]  and  pessoa[4][2] >= elevador[3][2] ):
        return True
    else:
        return False


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
