from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math 
import random

import time
Starting_Time=time.time()

#Widow Size
window_width=1000
window_height=800
Aspect_Ratio=window_width/window_height

# Camera-related variables
camera_z_axis_position=500
camera_angle=0
view_mode=0
first_person_mode=False

# Arena Parameter
GRID_LENGTH =1000

#Player Variable
player_x=800
player_y=0
Player_face_angle=180

player_min_position=-GRID_LENGTH+50
player_max_postion=GRID_LENGTH-50

 # Field of view
fovY = 120 

  

#Tower
Tower_max_HP=20
Tower_Current_HP=20
#Game parameter
Game_over=False

#Supporting Functions
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def collide_with_tower(x, y):
    dist = math.sqrt(x*x + y*y)
    return dist < (70 + 35) #Tower Radius , Player Radius


# Drawing Arena
def draw_outer_full_ground(): 
    x = -GRID_LENGTH * 4
    row = 0
    while x < GRID_LENGTH * 4:
        y = -GRID_LENGTH * 4
        col = 0
        while y < GRID_LENGTH * 4:
            height =((x+y)%200)/50
            # height = (x % 200) / 50

            if row % 2 == 0:
                glColor3f(0.30, 0.18, 0.08)   # very dark soil
            else:
                glColor3f(0.70, 0.55, 0.35)   # light dry soil

            glPushMatrix()

            glTranslatef(x + 50,y + 50,height / 2)
            glScalef(100, 100, height)
            glutSolidCube(1)

            glPopMatrix()

            y += 100    
            col += 1
        x += 100         
        row += 1

def draw_arena():
    glBegin(GL_QUADS)
    y = -GRID_LENGTH
    row=0
    while y < GRID_LENGTH:
        x = -GRID_LENGTH
        col=0
        while x < GRID_LENGTH:
            if (row + col) % 4 == 0:
                glColor3f(0.18, 0.55, 0.18)   # dark grass
            elif (row + col) % 4 == 1:
                glColor3f(0.28, 0.70, 0.28)   # light grass
            elif (row + col) % 4 == 2:
                glColor3f(0.35, 0.30, 0.20)   # mud / dirt
            else:
                glColor3f(0.25, 0.65, 0.25)   # mixed grass

            #( 100*100) Size Tile    
            glVertex3f(x, y, 0)
            glVertex3f(x + 100, y, 0)
            glVertex3f(x + 100, y + 100, 0)
            glVertex3f(x, y + 100, 0)
            x += 100
            col += 1
        y += 100
        row += 1
    glEnd()

#SKY
def Day_Night_Transition():
    elapsed = time.time() - Starting_Time
    t = elapsed / 210 #Total Game will run 210s (3.5 min)

    if t > 1:
        t = 1
    # Day sky color
    day = (0.53, 0.81, 0.92)
    # Night sky color
    night = (0.05, 0.05, 0.20)

    #Transition
    r = day[0] * (1 - t) + night[0] * t
    g = day[1] * (1 - t) + night[1] * t
    b = day[2] * (1 - t) + night[2] * t

    glClearColor(r, g, b, 1)

#Player
def draw_player():
    glPushMatrix()
    glTranslatef(player_x, player_y,0)
    glRotatef(Player_face_angle, 0, 0, 1)

    if Game_over:
        glRotatef(90, 1, 0, 0)

    # Legs
    glColor3f(0.01, 0, 0.1)
    glPushMatrix()
    glTranslatef(-18, -14, 0)
    glScalef(0.45, 0.35, 1.15)
    gluCylinder(gluNewQuadric(), 10, 40, 50, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-18, 14, 0)
    glScalef(0.45, 0.35, 1.15)
    gluCylinder(gluNewQuadric(), 10, 40, 50, 10, 10)
    glPopMatrix()

    # Torso
    glColor3f(1.0, 0.6, 0.2)
    glPushMatrix()
    glTranslatef(0, 0, 105)
    glScalef(1.05, 0.7, 1.2)
    glutSolidCube(80)
    glPopMatrix()

    # Head
    glColor3f(0.05, 0.05, 0.05)
    glPushMatrix()
    glTranslatef(0, 0, 150)
    gluSphere(gluNewQuadric(), 30, 15, 15)
    glPopMatrix()

    # Arms
    skin = (0.85, 0.75, 0.62)
    glColor3f(*skin)
    glPushMatrix()
    glTranslatef(40, 20, 110)
    glScalef(0.45, 0.35, 1.15)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 15, 10, 60, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(40, -25, 110)
    glScalef(0.45, 0.35, 1.15)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 15, 10, 60, 10, 10)
    glPopMatrix()

    #gun cylinder
    glColor3f(0.6, 0.6, 0.6)
    glPushMatrix()
    glTranslatef(40, 0, 120)
    glScalef(0.45, 0.35, 1.15)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 18, 6, 190, 10, 10)
    glPopMatrix()

    glPopMatrix()

#Tower
def draw_Tower():
    health_ratio = Tower_Current_HP / Tower_max_HP

    tower_height = health_ratio * 700  #Max Height =700

    scale_z = tower_height / 70 # Cube height,width

    #Tower
    glPushMatrix()
    glTranslatef(0, 0, tower_height / 2)
    glScalef(1.6, 1.6, scale_z)
    glColor3f(1.0, 0.85, 0.1)
    glutSolidCube(70)
    glPopMatrix()

    # Sphere of on the Top
    glPushMatrix()
    glTranslatef(0, 0, tower_height)
    glColor3f(0.95, 0.95, 0.95)
    gluSphere(gluNewQuadric(), 35, 16, 16)
    glPopMatrix()


def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global view_mode,Game_over,Player_face_angle,player_x,player_y

    if Game_over:
        glutPostRedisplay()
        return
     # # Move forward (W key)
    if key == b'w':
        dx= math.cos(math.radians(Player_face_angle))
        dy=math.sin(math.radians(Player_face_angle))
        prevx=player_x
        player_x+=dx*30
        if player_min_position>player_x or player_x>player_max_postion or collide_with_tower(player_x,player_y):
            player_x=prevx
        prevy=player_y
        player_y+=dy*30
        if player_min_position>player_y or player_y>player_max_postion or collide_with_tower(player_x,player_y):
            player_y=prevy


    # # Move backward (S key)
    if key == b's':
        dx= math.cos(math.radians(Player_face_angle))
        dy=math.sin(math.radians(Player_face_angle))
        prevx=player_x
        prevy=player_y
        player_x-=dx*30
        player_y-=dy*30
        if player_min_position>player_x or player_x>player_max_postion or collide_with_tower(player_x,player_y):
            player_x=prevx
        if player_min_position>player_y or player_y>player_max_postion or collide_with_tower(player_x,player_y):
            player_y=prevy

    # # Rotate gun left (A key)
    if key == b'a':
        Player_face_angle=(Player_face_angle+5)%360

    # # Rotate gun right (D key)
    if key == b'd':
        Player_face_angle=(Player_face_angle-5)%360
    # # Toggle Cemera View
    if key == b'c':
        view_mode = (view_mode + 1) % 3
        glutPostRedisplay()
        return

    # # Toggle cheat vision (V key)
    # if key == b'v':

    # # Reset the game if R key is pressed
    # if key == b'r':


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_angle, camera_z_axis_position

    if key == GLUT_KEY_LEFT:
        camera_angle -= 5
    elif key == GLUT_KEY_RIGHT:
        camera_angle += 5
    elif key == GLUT_KEY_UP:
        camera_z_axis_position += 5
    elif key == GLUT_KEY_DOWN:
        camera_z_axis_position -= 5

    camera_z_axis_position=min(max(camera_z_axis_position,200),1000)
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    global first_person_mode
    if state != GLUT_DOWN:
        return
    if button == GLUT_LEFT_BUTTON:
        pass
        # bullet_fire()
    elif button == GLUT_RIGHT_BUTTON:
        first_person_mode= not first_person_mode

    glutPostRedisplay()



def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    glutPostRedisplay()

def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY,Aspect_Ratio, 0.1, 3000) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    if first_person_mode: #FPP
        Rad_Player_face_angle = math.radians(Player_face_angle)
        fx = math.cos(Rad_Player_face_angle)
        fy = math.sin(Rad_Player_face_angle)

        eye_x = player_x + fx * 40
        eye_y = player_y + fy * 40
        eye_z = 180

        center_x = player_x + fx * 400
        center_y = player_y + fy * 400
        center_z = 80

        gluLookAt(eye_x, eye_y, eye_z,
                  center_x, center_y, center_z,
                  0, 0, 1)
        return

    if view_mode==0: #View From a broder angle of arena
        rad_camera_angle = math.radians(camera_angle)
        cam_x = math.cos(rad_camera_angle) * 1300  #x Distance =1300 
        cam_y = math.sin(rad_camera_angle) * 1300  #y Distance =1300
        cam_z = camera_z_axis_position

        gluLookAt(cam_x, cam_y, cam_z,
                0, 0, 0,
                0, 0, 1)
        
    elif view_mode==1: #TPP view 
        Rad_Player_face_angle = math.radians(Player_face_angle)
        fx = math.cos(Rad_Player_face_angle)
        fy = math.sin(Rad_Player_face_angle)

        # Camera Postion behind the player
        cam_x = player_x - fx * 75
        cam_y = player_y - fy * 75
        cam_z = 280

        #View at forward position
        look_x = player_x + fx * 200
        look_y = player_y + fy * 200
        look_z = 120

        gluLookAt(cam_x, cam_y, cam_z,
                look_x, look_y, look_z,
                0, 0, 1)
        
    else: #Top View
         gluLookAt(0, 0, 1300,
                  0, 0, 0,
                  0, 1, 0)




def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    Day_Night_Transition()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, window_width,window_height)  # Set viewport size

    setupCamera()  # Configure camera perspective

    #Environment Setup
    draw_outer_full_ground()
    draw_arena()
    draw_Tower()

    #player
    draw_player()

    
    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(window_width, window_height)  # Window size
    glutInitWindowPosition(150, 0)  # Window position
    glutCreateWindow(b"Defend The Tower")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()