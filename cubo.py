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

esferaOrigem = (1,25,25)

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
def MoverElevador(index,direcao):
    if(direcao):
        elevadores[index] = tuple([(i[0],i[1]+0.10,i[2]) for i in elevadores[index]])        
    else:
        elevadores[index] = tuple([(i[0],i[1]-0.10,i[2]) for i in elevadores[index]])


#Desenha os elevadores(Retangulos) e as pessoas(esferas)
def Desenhar():
    glBegin(GL_LINES)
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

    glTranslatef(-10, -5, -15)
    #glRotatef(45, 3, 0, 0)

    subida = True;

    while not glfw.window_should_close(window):

        if(subida):
            for index in range(len(elevadores)):
                MoverElevador(index,True)    
                if(elevadores[index][0][1] > 20):
                    subida = False
        else:
            for index in range(len(elevadores)):
                MoverElevador(index,False)    
                if(elevadores[index][0][1] < 1):
                    subida = True                          
         
        glfw.poll_events()
        glfw.swap_buffers(window)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Desenhar()

    glfw.terminate()

if __name__ == "__main__": main()
