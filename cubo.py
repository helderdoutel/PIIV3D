# import PyOpenGl
import time
import glfw
import OpenGL
OpenGL.ERROR_CHECKING = False
OpenGL.FULL_LOGGING = True
from OpenGL.GL import *
from OpenGL.GLU import *


verticies1 = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

verticies2 = (
    (0.25, -0.25, -0.25),
    (0.25, 0.25, -0.25),
    (-0.25, 0.25, -0.25),
    (-0.25, -0.25, -0.25),
    (0.25, -0.25, 0.25),
    (0.25, 0.25, 0.25),
    (-0.25, -0.25, 0.25),
    (-0.25, 0.25, 0.25)
)



print(verticies2, verticies1)

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





def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies1[vertex])
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies2[vertex])            
    glEnd()


def main():
    global verticies2
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, 'Simulação 3D', None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    # raise Exception(window)
    gluPerspective(90, (800 / 600), 0., 50.0)

    glTranslatef(0.0, 0.0, -5)

    while not glfw.window_should_close(window):
        if glfw.get_key(window,glfw.KEY_ESCAPE):
            break
        if glfw.get_key(window,glfw.KEY_UP):
            v2 = []
            for x in (verticies2):
                v = []
                flag = 0
                for y in x:
                    if flag == 0:
                        v.append(y + 0.1)
                        flag = 1
                    else:
                        v.append(y)
                v2.append(v)

            verticies2 = v2
        if glfw.get_key(window,glfw.KEY_DOWN):
            glTranslate(0,-1,0)
        if glfw.get_key(window,glfw.KEY_LEFT):
            glTranslate(-1,0,0)
        if glfw.get_key(window,glfw.KEY_RIGHT):
            glTranslate(1,0,0)

        glfw.poll_events()
        glfw.swap_buffers(window)
        #glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Cube()
        time.sleep(0.001)


    glfw.terminate()

if __name__ == "__main__": main()
