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
    (0.50, -0.50, -0.50), #Base direita superior
    (0.50, 0.50, -0.50), 
    (-0.50, 0.50, -0.50),
    (-0.50, -0.50, -0.50), #Base esquerda superior
    (0.50, -0.50, 0.50), #Base direita inferior
    (0.50, 0.50, 0.50),
    (-0.50, -0.50, 0.50), #Base esquerda inferior
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


def MoverPessoa(direcao):
    global pessoaOrigem
    print ("Base esquerda superior " + str(pessoaOrigem[0]))
    print ("Base esquerda inferior" + str(pessoaOrigem[3]))
    print ("Base direita superior " + str(pessoaOrigem[1]))
    print ("Base direita inferior " + str(pessoaOrigem[2]))
    if(direcao == 0): #cima
        pessoaOrigem =  tuple([(i[0],i[1],i[2]-0.10) for i in pessoaOrigem])   
    elif(direcao == 1): #baixo
        pessoaOrigem =  tuple([(i[0],i[1],i[2]+0.10) for i in pessoaOrigem])   
    elif(direcao == 2): #esquerda
        pessoaOrigem =  tuple([(i[0]-0.10,i[1],i[2]) for i in pessoaOrigem])   
    elif(direcao == 3): #direita
        pessoaOrigem =  tuple([(i[0]+0.10,i[1],i[2]) for i in pessoaOrigem])   


def colisao(elevador,pessoa):
    # print(elevador[6][2] )
    # print(elevador[3][2])
    if (pessoa[4][0] >= elevador[6][0] and pessoa[4][0] <= elevador[4][0] and pessoa[4][2] <= elevador[6][2]  and  pessoa[4][2] >= elevador[3][2] ):
        return True
    else:
        return False




#Desenha os elevadores(Retangulos) e as pessoas(esferas)
def Desenhar():
    glBegin(GL_LINES)
    for edge in pessoaArestas:
        for vertex in edge:
                glVertex3fv(pessoaOrigem[vertex])   
    for edge in chaoArestas:
        for vertex in edge:
                glVertex3fv(chaoVertices[vertex])                              
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
            if(colisao(elevadores[index],pessoaOrigem)):
               glfw.terminate()
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

        if glfw.get_key(window,glfw.KEY_R):
            glTranslatef(0, 0, 1)
        if glfw.get_key(window,glfw.KEY_A): 
            glTranslatef(1, 0, 0)
        if glfw.get_key(window,glfw.KEY_F):
            glTranslatef(0, 0, -1)
        if glfw.get_key(window,glfw.KEY_D):
            glTranslatef(-1, 0, 0)
        if glfw.get_key(window,glfw.KEY_W):
            glTranslatef(0, -1, 0)
        if glfw.get_key(window,glfw.KEY_S):
            glTranslatef(0, 1, 0)


        if glfw.get_key(window,glfw.KEY_UP):
            MoverPessoa(0)
        if glfw.get_key(window,glfw.KEY_DOWN): 
            MoverPessoa(1)
        if glfw.get_key(window,glfw.KEY_LEFT):
            MoverPessoa(2)
        if glfw.get_key(window,glfw.KEY_RIGHT):
            MoverPessoa(3)  


        if glfw.get_key(window,glfw.KEY_5):
            glRotatef(1, 10, 0, 0)
        if glfw.get_key(window,glfw.KEY_2): 
            glRotatef(-1, 10, 0, 0)
        if glfw.get_key(window,glfw.KEY_4):
            glRotatef(1, 0, 5,0)
        if glfw.get_key(window,glfw.KEY_6):
            glRotatef(1, 0, -5, 0)      

         
        glfw.poll_events()
        glfw.swap_buffers(window)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Desenhar()

    glfw.terminate()

if __name__ == "__main__": main()
