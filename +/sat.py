import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def draw_axes():
    """Desenha os eixos X, Y e Z no espaço 3D."""
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)  # Eixo X (Vermelho)
    glVertex3f(0, 0, 0)
    glVertex3f(2, 0, 0)
    
    glColor3f(0, 1, 0)  # Eixo Y (Verde)
    glVertex3f(0, 0, 0) 
    glVertex3f(0, 2, 0)
    
    glColor3f(0, 0, 1)  # Eixo Z (Azul)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 2)
    glEnd()

def draw_satellite():
    """Desenha um cubo representando o satélite."""
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.5, 0.5)
    vertices = [
        [-0.5, -0.5, -0.5],
        [ 0.5, -0.5, -0.5],
        [ 0.5,  0.5, -0.5],
        [-0.5,  0.5, -0.5],
        [-0.5, -0.5,  0.5],
        [ 0.5, -0.5,  0.5],
        [ 0.5,  0.5,  0.5],
        [-0.5,  0.5,  0.5]
    ]
    
    faces = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [2, 3, 7, 6],
        [0, 3, 7, 4],
        [1, 2, 6, 5]
    ]
    
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

def create_3d_view():
    """Inicializa a visualização 3D com OpenGL."""
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_axes()
        draw_satellite()
        pygame.display.flip()
        pygame.time.wait(10)
    
    pygame.quit()

if __name__ == "__main__":
    create_3d_view()
