import random
from Elevador import Elevador
from Passageiro import Passageiro
import time
import datetime
import numpy as np
import glfw
import OpenGL
import math
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
    (0, -0.5, 10),
    (30, -0.5, 10),
    (30, -0.5, -1),
    (0, -0.5, -1),
)

chaoArestas = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
)

# Gera os elevadores com os devidos espacamentos e propriedades iniciais
# Roda apenas uma vez no inicio de cada rodada


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


def gerar_passageiros(funcionarios_total=1000, max_por_min=30, min_por_min=0, espacamento_inicial=1, elevadores=[]):
    hora_chegada = datetime.datetime(2018, 1, 1, 8, 0, 0, 0)
    # datetime.datetime.now() - datetime.timedelta(minutes=15)
    # hr de chegada individual
    maior_x_elevadores = 0
    menor_x_elevadores = 10000
    for index in range(len(elevadores)):
        maior = max([i[0] for i in elevadores[index].get_vertices()])
        menor = min([i[0] for i in elevadores[index].get_vertices()])
        if maior > maior_x_elevadores:
            maior_x_elevadores = maior
        if menor < menor_x_elevadores:
            menor_x_elevadores = menor
    centro = menor_x_elevadores + \
        ((maior_x_elevadores - menor_x_elevadores) / 2)
    fila = []

    espacamento = espacamento_inicial
    id_passageiro = 0
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
            passageiro = Passageiro(
                id_passageiro=id_passageiro, hora_chegada=hora_chegada)
            id_passageiro += 1
            tupla = tuple([(i[0] + centro, i[1], i[2] + 10)
                           for i in pessoaOrigem])
            passageiro.set_vertices(tupla)
            espacamento += espacamento
            fila.append(passageiro)
            hora_chegada = hora_chegada + datetime.timedelta(seconds=tec)
            chegou -= 1
        if chegou == 0:
            hora_chegada = hora_chegada + datetime.timedelta(minutes=1)
    return fila


# Move o elevador 3D
def MoverElevador(index, direcao):
    if(direcao):
        elevadores[index].set_vertices(tuple(
            [(i[0], i[1] + velocidade_elevador, i[2]) for i in elevadores[index].get_vertices()]))
    else:
        elevadores[index].set_vertices(tuple(
            [(i[0], i[1] - velocidade_elevador, i[2]) for i in elevadores[index].get_vertices()]))


# Verifica se houve colisao entre uma pessoa e um elevador, isto eh, se a
# pessoa entrou no elevador
def colisao(elevador, pessoa):
    # print(elevador[6][2] )
    # print(elevador[3][2])
    if (pessoa[4][0] >= elevador[6][0] and pessoa[4][0] <= elevador[4][0] and pessoa[4][2] <= elevador[6][2] and pessoa[4][2] >= elevador[3][2]):
        return True
    else:
        return False


def mover_passageiro(index, hora_atual, velocidade=0.83):
    # Pega coordenadas do elevador destino
    xe, ye, ze = elevadores[fila[index].get_elevador()].get_centro_objeto()
    # Pega coordenadas do passageiro
    xp, yp, zp = fila[index].get_centro_objeto()
    distancia = math.sqrt(((xp - xe) ** 2) + ((zp - ze)**2))
    viagens = distancia / velocidade
    velocidade_x = (xp - xe) / viagens
    velocidade_z = (zp - ze) / viagens
    fila[index].set_vertices(
        tuple([(i[0] - velocidade_x, i[1], i[2] - velocidade_z) for i in fila[index].get_vertices()]))
    xe, ye, ze = elevadores[fila[index].get_elevador()].get_centro_objeto()
    xp, yp, zp = fila[index].get_centro_objeto()
    if colisao(elevadores[fila[index].get_elevador()].get_vertices(), fila[index].get_vertices()):
        fila[index].set_hora_elevador(hora_atual)
    elif zp <= ze:
        # print(zp, ze)
        fila[index].set_hora_elevador(hora_atual)


def mover_passageiro_fila(index, posicao, hora_atual):
    fila[index].set_vertices(
        tuple([(i[0], i[1], i[2] + posicao) for i in fila[index].get_vertices()]))


def atualizar_posicao(index, posicao):
    posiscao_atual = fila[index].get_posicao()
    nova = posiscao_atual - posicao
    # print(index, posiscao_atual, posicao, nova)
    fila[index].set_vertices(
        tuple([(i[0], i[1], i[2] - nova) for i in fila[index].get_vertices()]))
    fila[index].set_posicao(posicao)


def Desenhar(hora):
    glBegin(GL_LINES)
    for passageiro in fila:  # Desenha passageiros que estao esperando na fila
        if passageiro.esperando(hora):
            for edge in pessoaArestas:
                for vertex in edge:
                    glVertex3fv(passageiro.get_vertices()[vertex])

    for edge in chaoArestas:  # Desenha o chao
        for vertex in edge:
            glVertex3fv(chaoVertices[vertex])

    for elevador in elevadores:  # Desenha os elevadores
        for edge in edges:
            for vertex in edge:
                glVertex3fv(elevador.get_vertices()[vertex])
    glEnd()


def ajustar_chao_e_camera():
    global chaoVertices

    chaoVertices = list(chaoVertices)

    x1 = elevadores[len(elevadores) - 1].get_vertices()[0][0] + 4

    chaoVertices[1] = tuple((x1, chaoVertices[1][1], chaoVertices[1][2]))
    chaoVertices[2] = tuple((x1, chaoVertices[2][1], chaoVertices[2][2]))

    chaoVertices = tuple(chaoVertices)

    # glTranslatef(0,0,(x1/2)*-1)


def iniciar_viagem(index, hora_atual, tempo_viagem):
    # quebrar = np.random.choice([0, 1], p=[0.99, 0.01])
    # Verifica se o elevador ja esta em movimento, se nao, esta apto a iniciar
    # uma viagem
    if not elevadores[index].em_viagem(hora_atual):
        esperar = False
        # Se tiver algum passageiro se movendo ate o elevador, o elevador deve
        # esperar
        for x in elevadores[index].get_passageiros():
            if fila[x].andando():
                esperar = True
                break
        if not esperar:  # Se ninguem estiver se movendo ate o elevador,
            elevadores[index].set_ultima_partida(hora_atual)
            elevadores[index].set_tempo_viagem(tempo_viagem)
            # incrementa o contador de viagens realizadas pelo elevador
            elevadores[index].set_viagens()
            elevadores[index].zerar_passageiro()


def main():
    window = inicializar()
    ajustar_chao_e_camera()

    # Setup da simulacao

    contador = 0
    hora_atual = datetime.datetime(2018, 1, 1, 8, 0, 0, 0)

    fila_esperando = []
    # Loop de execucao principal
    while not glfw.window_should_close(window):

        # Logica para cada elevador
        for index in range(len(elevadores)):

            elevador = elevadores[index]

            # Calcula o tempo de viagem do elevador
            tempo_viagem = round(np.random.normal(120, 10, 1)[0])
            tempo_viagem = round(tempo_viagem / 2) * 2
            tempo_viagem = datetime.timedelta(seconds=tempo_viagem)

            if elevador.get_ultima_partida() + elevador.get_tempo_viagem() + datetime.timedelta(minutes=2) <= hora_atual:
                iniciar_viagem(index, hora_atual, tempo_viagem)

            if len(elevador.get_passageiros()) >= 10:
                iniciar_viagem(index, hora_atual, tempo_viagem)

            # Se o elevador estiver em viagem, movimenta o mesmo
            if elevador.get_ultima_partida() + elevador.get_tempo_viagem() > hora_atual:
                if(elevador.get_ultima_partida() + (elevador.get_tempo_viagem() / 2)) > hora_atual:
                    if index == 0:
                        contador += 1
                    MoverElevador(index, True)
                else:
                    MoverElevador(index, False)

        # Logica para cada passageiro
        parar = True
        for passageiro in fila:
            if passageiro.get_hora_elevador() is None:
                parar = False
        if parar:
            print('FIM DA SIMULACAO')
            break
        for passageiro in fila:
            # Se o passageiro estiver esperando e nao estiver com um elevador atribuido
            # Procura um elevador no terreo com menos de 10 passageiros
            if passageiro.esperando(hora_atual) and not passageiro.andando():
                if passageiro.get_id() not in fila_esperando:
                    mover_passageiro_fila(
                        passageiro.get_id(), len(fila_esperando), hora_atual)
                    passageiro.set_posicao(len(fila_esperando))
                    fila_esperando.append(passageiro.get_id())
                else:
                    atualizar_posicao(passageiro.get_id(),
                                      fila_esperando.index(passageiro.get_id()))
                for index in range(len(elevadores)):
                    if not elevadores[index].em_viagem(hora_atual) and len(elevadores[index].get_passageiros()) < 10:
                        fila_esperando.remove(passageiro.get_id())
                        passageiro.set_posicao(None)
                        passageiro.set_elevador(index)
                        elevadores[index].add_passageiro(passageiro.get_id())
                        break
                for index in fila_esperando:
                    atualizar_posicao(index, fila_esperando.index(index))
            # Move o passageiro ate o seu respectivo elevador atribuido
            if passageiro.andando():
                mover_passageiro(passageiro.get_id(), hora_atual)
        # for index in fila_esperando:
        #     if not fila[index].andando():
        #         atualizar_posicao(index, fila_esperando.index(index))

        # Verifica se alguma tecla foi pressionada e faz o respectivo
        # tratamento
        teclado(window)
        glfw.poll_events()
        glfw.swap_buffers(window)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Desenhar(hora_atual)
        hora_atual = hora_atual + datetime.timedelta(seconds=1)

    glfw.terminate()


def inicializar():

    if not glfw.init():
        return

    window = glfw.create_window(
        largura_tela, altura_tela, 'Simulador de elevadores 3D com OPENGL', None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Setup da inicial da camera
    gluPerspective(90, (largura_tela / altura_tela), 0., 25.0)
    glTranslatef(-15, -5, -15)

    return window


# Metodo que controla os eventos de key press
def teclado(window):
    global chaoVertices
    if glfw.get_key(window, glfw.KEY_ESCAPE):
        glfw.terminate()

    if glfw.get_key(window, glfw.KEY_W):
        glTranslatef(0, -2, 0)
    if glfw.get_key(window, glfw.KEY_S):
        glTranslatef(0, 2, 0)
    if glfw.get_key(window, glfw.KEY_A):
        glTranslatef(2, 0, 0)
    if glfw.get_key(window, glfw.KEY_D):
        glTranslatef(-2, 0, 0)
    if glfw.get_key(window, glfw.KEY_R):
        glTranslatef(0, 0, 2)
    if glfw.get_key(window, glfw.KEY_F):
        glTranslatef(0, 0, -2)

    if glfw.get_key(window, glfw.KEY_UP):
        glRotatef(5, 1, 0, 0)
    if glfw.get_key(window, glfw.KEY_DOWN):
        glRotatef(5, -1, 0, 0)
    if glfw.get_key(window, glfw.KEY_LEFT):
        glRotatef(5, 0, 1, 0)
    if glfw.get_key(window, glfw.KEY_RIGHT):
        glRotatef(5, 0, -1, 0)

    if glfw.get_key(window, glfw.KEY_O):
        chaoVertices = list(chaoVertices)
        chaoVertices[1] = tuple(
            (chaoVertices[1][0] + 1, chaoVertices[1][1], chaoVertices[1][2]))
        chaoVertices[2] = tuple(
            (chaoVertices[2][0] + 1, chaoVertices[2][1], chaoVertices[2][2]))
        chaoVertices = tuple(chaoVertices)
    if glfw.get_key(window, glfw.KEY_L):
        chaoVertices = list(chaoVertices)
        chaoVertices[1] = tuple(
            (chaoVertices[1][0] - 1, chaoVertices[1][1], chaoVertices[1][2]))
        chaoVertices[2] = tuple(
            (chaoVertices[2][0] - 1, chaoVertices[2][1], chaoVertices[2][2]))
        chaoVertices = tuple(chaoVertices)


# Gera os elevadores e a fila de passageiros de acordo com os elevadores
ne = input('Quantos elevadores?\n')
while not ne.isdigit():
    ne = input('(Númerico) Quantos elevadores?\n')
elevadores = gerar_elevadores(int(ne), 5)
total = input('Quantas pessoas no total?\n')
while not total.isdigit():
    total = input('(Númerico) Quantas pessoas no total?\n')
total = int(total)
p_media = input('Quantas pessoas em média por minuto?\n')
if not p_media.isdigit():
    p_media = 30
    print('Assumindo 30 pessoas em média por minuto')
p_media = int(p_media)
fila = gerar_passageiros(funcionarios_total=total,
                         max_por_min=p_media, elevadores=elevadores)
velocidade_elevador = 0.50
largura_tela = 1280
altura_tela = 720

if __name__ == "__main__":
    main()
