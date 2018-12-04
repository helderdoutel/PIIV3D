# import PyOpenGl
import glfw
import time
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
            glVertex3fv(verticies2[vertex])
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies1[vertex])
    glEnd()


def main():
    global verticies1
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, 'teste', None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    # raise Exception(window)
    gluPerspective(45, (800 / 600), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)
    while not glfw.window_should_close(window):

        if(glfw.get_key(window,glfw.KEY_UP)):         
            glTranslatef(0.0, 0.0,1.0)
            time.sleep(0.05)
        glfw.poll_events()
        glfw.swap_buffers(window)
        #glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Cube()

    glfw.terminate()

if __name__ == "__main__":
    main()
