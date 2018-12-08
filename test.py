# import PyOpenGl
import time
import glfw
import time
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

pessoaOrigem = (
    (0, 0.5, 0),
    (1, 0.5, 0),
    (0.5, 0.5, 0.5),
    (0.5,2, 1),
)

pessoaArestas = (
    (0,1),
    (1,2),
    (2,0),
    (3,0),
    (3,1),
    (3,2)
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

elevadores = []


#Gerar os vertices dos elevadores lado lado
def GerarElevadores(quantidade, espacamento_inicial):
    espacamento = espacamento_inicial
    for i in range(quantidade):
        tupla = tuple([(i[0]+espacamento,i[1],i[2]) for i in verticesOrigem])
        elevadores.append(tupla)
        #print(tupla)
        espacamento += espacamento_inicial

#Move elevador para cima e para baixo
def MoverElevador(index,direcao,velocidade):
    if(direcao):
        elevadores[index] = tuple([(i[0],i[1]+velocidade,i[2]) for i in elevadores[index]])        
    else:
        elevadores[index] = tuple([(i[0],i[1]-velocidade,i[2]) for i in elevadores[index]])


#Desenha os elevadores(Retangulos) e as pessoas(esferas)
def Desenhar():
    glBegin(GL_LINES)
    for edge in pessoaArestas:
        for vertex in edge:
                glVertex3fv(pessoaOrigem[vertex])              
    for elevador in elevadores:
        for edge in edges:
            for vertex in edge:
                glVertex3fv(elevador[vertex])      
    glEnd()



def main():

    
    GerarElevadores(3,5)

    if not glfw.init():
        return

    window = glfw.create_window(1920, 1080, 'Simulação 3D', None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    gluPerspective(90, (1920 / 1080), 0.,25.0)

    glTranslatef(-15, 5, -15)
    glRotatef(75, 10, 0, 0)

    subidas = [True,True,True,True,True,True]
    mover = [True,False,False]
    
    velocidade = 0.10

        

    while not glfw.window_should_close(window):

        for index in range(len(elevadores)):
            if(subidas[index]):
                if(mover[index]):
                    MoverElevador(index,True,velocidade)  
                if(elevadores[0][0][1] > 5):
                    mover[1] = True
                if(elevadores[1][0][1] > 7):
                    mover[2] = True                   
                if(elevadores[index][0][1] > 10):
                    subidas[index] = False

            else:
                if(mover[index]):
                    MoverElevador(index,False,velocidade)    
                if(elevadores[index][0][1] < 1):
                    subidas[index] = True

        # glRotatef(75, 10, 0, 0)
        time.sleep(0.10)

         
        glfw.poll_events()
        glfw.swap_buffers(window)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Desenhar()

    glfw.terminate()

if __name__ == "__main__": main()
