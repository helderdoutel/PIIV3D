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
    (0, -0.5, 0),  # base esquerda superior
    (0.1, -0.5, 0),  # base direita superior
    (0.1, -0.5, 0.1),  # base direita inferior
    (0, -0.5, 0.1),  # base esquerda inferior
    (0.05, 1, 0.1)  # topo
)

pessoaArestas = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 0),
    (4, 1),
    (4, 2),
    (4, 3)
)

chaoVertices = (
    (0, -0.5, -50),
    (50, -0.5, -50),
    (50, -0.5, 50),
    (0, -0.5, 50),
)

chaoArestas = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
)


# detecta colisao entre pessoa e elevador
def colisao(elevador, pessoa):
    if (pessoa[4][0] >= elevador[6][0] and pessoa[4][0] <= elevador[4][0] and pessoa[4][2] <= elevador[6][2] and pessoa[4][2] >= elevador[3][2]):
        return True
    else:
        return False


def gerar_elevadores(quantidade, espacamento_inicial):
    espacamento = espacamento_inicial
    elevadores = []
    for i in range(quantidade):
        tupla = tuple([(i[0] + espacamento, i[1], i[2])
                       for i in verticesOrigem])
        elevador = Elevador()
        elevador.set_vertices(tupla)
        elevador.set_ultima_partida(datetime.datetime(2018, 1, 1, 8, 0, 0, 0))
        elevador.set_tempo_viagem(datetime.timedelta(minutes=0))
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


def MoverElevador(index, direcao, velocidade):
    if(direcao):
        elevadores[index].set_vertices(tuple(
            [(i[0], i[1] + velocidade, i[2]) for i in elevadores[index].get_vertices()]))
    else:
        elevadores[index].set_vertices(tuple(
            [(i[0], i[1] - velocidade, i[2]) for i in elevadores[index].get_vertices()]))


def Desenhar():
    glBegin(GL_LINES)
    # for edge in pessoaArestas:
    #     for vertex in edge:
    #             glVertex3fv(pessoaOrigem[vertex])
    # for edge in chaoArestas:
    #     for vertex in edge:
    #             glVertex3fv(chaoVertices[vertex])
    for elevador in elevadores:
        for edge in edges:
            for vertex in edge:
                glVertex3fv(elevador.get_vertices()[vertex])
    glEnd()

elevadores = gerar_elevadores(6, 5)


def iniciar_viagem(index, hora_inicio, tempo_viagem):
    # quebrar = np.random.choice([0, 1], p=[0.99, 0.01])
    elevadores[index].set_ultima_partida(hora_inicio)
    elevadores[index].set_tempo_viagem(tempo_viagem)
    elevadores[index].set_passageiros([])
    elevadores[index].set_viagens(1)


def main():

    if not glfw.init():
        return
    hora_inicio = datetime.datetime(2018, 1, 1, 8, 0, 0, 0)
    window = glfw.create_window(1920, 1080, 'Simulação 3D', None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    gluPerspective(90, (1920 / 1080), 0., 25.0)

    glTranslatef(-15, -5, -15)

    # subidas = [True, True, True, True, True, True]

    velocidade = 0.10
    velocidades = []

    for index in range(len(elevadores)):
        velocidades.append(velocidade)
        # velocidade += 0.10
    flag = 0
    contador = 0
    while not glfw.window_should_close(window):
        for index in range(len(elevadores)):
            tempo_viagem = round(np.random.normal(120, 10, 1)[0])
            tempo_viagem = datetime.timedelta(seconds=tempo_viagem)
            if elevadores[index].get_ultima_partida() + elevadores[index].get_tempo_viagem() + datetime.timedelta(minutes=2) == hora_inicio:
                iniciar_viagem(index, hora_inicio, tempo_viagem)
            if elevadores[index].get_ultima_partida() + elevadores[index].get_tempo_viagem() > hora_inicio:
                if(elevadores[index].get_ultima_partida() + (elevadores[index].get_tempo_viagem() / 2)) > hora_inicio:
                    if index == 0:
                        contador += 1
                    MoverElevador(index, True, velocidades[index])
                else:
                    MoverElevador(index, False, velocidades[index])

        glfw.poll_events()
        glfw.swap_buffers(window)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Desenhar()
        hora_inicio = hora_inicio + datetime.timedelta(seconds=1)
    glfw.terminate()

if __name__ == "__main__":
    main()
