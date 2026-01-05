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
player_x=500
player_y=0
Player_face_angle=180

player_min_position=-GRID_LENGTH+50
player_max_postion=GRID_LENGTH-50

Player_Current_HP=10
Player_Max_HP=10

 # Field of view
fovY = 120 

#Obstacle
obstacles = []
build_mode = "wall"
Obstacle_last_time=time.time()

#Tower
Tower_max_HP=20
Tower_Current_HP=20

#Enemy
enemies=[]
enemy_scale_over_time=0
enemy_shrink_last_time=time.time()

#Bullet
bullets=[]
Max_bullet_limit=30
Current_bullet=30

#Game parameter
Game_over=False
Game_Current_point=0
Game_Max_point=0
paused=False
Game_wave=1
Game_Wave_Start_Time=time.time()
Game_win=False

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

#movement Supporting
def collide_with_tower(x, y):
    dist = math.sqrt(x*x + y*y)
    return dist < (70 +100) #Tower Radius , Player Radius

#Supporting Obstacle 
def obstacle_collision(x, y):   
    for ob in obstacles:
        dx = x - ob["x"]
        dy = y - ob["y"]
        if math.sqrt(dx*dx + dy*dy) < 90:  #Obstacle width=80 , extra 10
            return ob
    return None

#Enemy Draw Supporting
def draw_humanoid(body_color, head_color, scale=1.0):
    # Legs
    glColor3f(*body_color)
    glPushMatrix()
    glTranslatef(-18 * scale, -14 * scale, 0)
    glScalef(0.45 * scale, 0.35 * scale, 1.15 * scale)
    gluCylinder(gluNewQuadric(), 10, 40, 50, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-18 * scale, 14 * scale, 0)
    glScalef(0.45 * scale, 0.35 * scale, 1.15 * scale)
    gluCylinder(gluNewQuadric(), 10, 40, 50, 10, 10)
    glPopMatrix()

    # Torso
    glColor3f(*body_color)
    glPushMatrix()
    glTranslatef(0, 0, 105 * scale)
    glScalef(1.05 * scale, 0.7 * scale, 1.2 * scale)
    glutSolidCube(80)
    glPopMatrix()

    # Head
    glColor3f(*head_color)
    glPushMatrix()
    glTranslatef(0, 0, 150 * scale)
    gluSphere(gluNewQuadric(), 30 * scale, 15, 15)
    glPopMatrix()

    # Arms
    skin = (0.85, 0.75, 0.62)
    glColor3f(*skin)
    glPushMatrix()
    glTranslatef(40 * scale, 20 * scale, 110 * scale)
    glScalef(0.45 * scale, 0.35 * scale, 1.15 * scale)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 15, 10, 60, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(40 * scale, -25 * scale, 110 * scale)
    glScalef(0.45 * scale, 0.35 * scale, 1.15 * scale)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 15, 10, 60, 10, 10)
    glPopMatrix()

def enemy_spawn_position():
    margin = 80
    side = random.randint(0, 3)

    if side == 0:
        x = -GRID_LENGTH + margin
        y = random.uniform(-GRID_LENGTH + margin, GRID_LENGTH - margin)
    elif side == 1:
        x = GRID_LENGTH - margin
        y = random.uniform(-GRID_LENGTH + margin, GRID_LENGTH - margin)
    elif side == 2:
        x = random.uniform(-GRID_LENGTH + margin, GRID_LENGTH - margin)
        y = -GRID_LENGTH + margin
    else:
        x = random.uniform(-GRID_LENGTH + margin, GRID_LENGTH - margin)
        y = GRID_LENGTH - margin

    return x, y

def create_enemies_list(kind,target):
    x, y = enemy_spawn_position()
    if kind == "scout":
        return {
            "kind": "scout",
            "x": x,
            "y": y,
            "hp": 1,
            "speed": 45,
            "target":target
            }


    if kind == "brute":
        return {
            "kind": "brute",
            "x": x,
            "y": y,
            "hp": 2,
            "speed": 20,
            "target":target
        }

    else:
        return {
            "kind": "boss",
            "x": x,
            "y": y,
            "hp": 5,
            "speed": 15,
            "target":"Tower"
        }

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
                glColor3f(0.45, 0.35, 0.25)   # dark soil
            else:
                glColor3f(0.70, 0.55, 0.35)   # light dry soil

            glPushMatrix()

            glTranslatef(x + 50,y + 50,height / 2)
            glScalef(200, 200, height)
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
    t = elapsed / 170 #Total Game will run 180s (3 min)

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

#Obstacle
def place_obstacle():
    global Game_Current_point,build_mode,obstacles

    if Game_Current_point<5:
        return
    
    Rad_Player_face_angle = math.radians(Player_face_angle)
    fx = math.cos(Rad_Player_face_angle)
    fy = math.sin(Rad_Player_face_angle)

    x = player_x + fx * 120  #Place the obstacle
    y = player_y + fy * 120  

    #Check if it is near to tower or not
    

    # Check if overlap another obstacle
    if obstacle_collision(x, y):
        return
    
    Game_Current_point-=5
    obstacles.append({
        "type": build_mode,
        "x": x,
        "y": y,
        "duration":10 })
    
def draw_obstacles():
    for i in obstacles:
        glPushMatrix()
        glTranslatef(i["x"], i["y"], 30)

        scale=1
        if i["duration"] < 2.0:
            scale = i["duration"] / 2.0 
        glScalef(scale, scale, scale)

        if i["type"] == "wall":
            glColor3f(0.4, 0.4, 0.4)
            glutSolidCube(80)
        else:
            glColor3f(0.9, 0.1, 0.1)
            gluCylinder(gluNewQuadric(), 30, 0, 70, 10, 10)

        glPopMatrix()

def update_obstacles():
    global obstacles, Obstacle_last_time

    current_time = time.time()
    dt = current_time - Obstacle_last_time
    Obstacle_last_time = current_time

    for i in obstacles[:]:  # copy list of obstacle
        i["duration"] -= dt

        if i["duration"] <= 0:
            obstacles.remove(i)

#Enemy
def spawn_enemy_per_wave():
    global Game_wave,enemies
    if Game_wave==1:
        enemies=[]
        for i in range(4):
            enemies.append(create_enemies_list("scout","Tower"))
        enemies.append(create_enemies_list("scout","Player"))

    elif Game_wave==2:
        enemies=[]
        for i in range(5):
            enemies.append(create_enemies_list("scout","Tower"))
        for i in range(2):
            enemies.append(create_enemies_list("scout","Player"))
        
        for i in range(2):
            enemies.append(create_enemies_list("brute","Tower"))
        for i in range(1):
            enemies.append(create_enemies_list("brute","Player"))

    elif Game_wave==3:
        enemies=[]
        for i in range(7):
            enemies.append(create_enemies_list("scout","Tower"))
        for i in range(3):
            enemies.append(create_enemies_list("scout","Player"))
        
        for i in range(3):
            enemies.append(create_enemies_list("brute","Tower"))
        for i in range(2):
            enemies.append(create_enemies_list("brute","Player"))
        

def draw_enemy():
    for e in enemies:
        s = 1.0 + 0.08 * math.sin(enemy_scale_over_time * 3.0)
        glPushMatrix()
        glTranslatef(e["x"], e["y"], 0)

        if e["target"]=="Tower":
            ang = math.degrees(math.atan2(-e["y"], -e["x"]))
            glRotatef(ang, 0, 0, 1)
        elif e["target"]=="Player":
            ang = math.degrees(math.atan2(player_y-e["y"], player_x-e["x"]))
            glRotatef(ang, 0, 0, 1)

        if e["kind"] == "scout":
            body = (0.9, 0.2, 0.2)   # red
            head = (0.05, 0.05, 0.05)
            scale = 0.9 * s
        elif e["kind"] == "brute":
            body = (0.2, 0.7, 0.7)   # cyan
            head = (0.05, 0.05, 0.05)
            scale = 1.1 * s
        else:
            body = (0.6, 0.0, 0.8)   # purple boss
            head = (0.1, 0.1, 0.1)
            scale = 1.25 * s

        draw_humanoid(body_color=body, head_color=head, scale=scale)
        glPopMatrix()

def enemy_movement(dt):
    global Game_Max_point,Game_Current_point,enemies
    for e in enemies:
            ex,ey=e["x"],e["y"]
            if e["target"]=="Tower":
                dx = 0 - ex
                dy = 0 - ey

                distance= math.sqrt(dx**2+dy**2)
                if distance >0.01:
                    if dx>0:
                        e["x"]+=(e["speed"]*dt)
                    else:
                        e["x"]-=(e["speed"]*dt)
                    if dy>0:
                        e["y"]+=(e["speed"]*dt)
                    else:
                        e["y"]-=(e["speed"]*dt)

            else:
                dx = player_x - ex
                dy = player_y - ey

                distance= math.sqrt(dx**2+dy**2)
                if distance >0.01:
                    if dx>0:
                        e["x"]+=(e["speed"]*dt)
                    else:
                        e["x"]-=(e["speed"]*dt)
                    if dy>0:
                        e["y"]+=(e["speed"]*dt)
                    else:
                        e["y"]-=(e["speed"]*dt)
            
            obs=obstacle_collision(e["x"],e["y"])

            #obastacle Check
            if obs is None:
                continue
            if obs["type"]=="wall":
                e["x"]=ex
                e["y"]=ey
                continue
           



def enemy_collision():
    global enemies, Player_Current_HP, Tower_Current_HP, Game_over,Game_Current_point,Game_Max_point

    ENEMY_RADIUS = 30
    PLAYER_RADIUS = 30
    TOWER_RADIUS = 70

    for e in enemies[:]:  
            #colllide with tower
            dist = math.sqrt(e["x"]**2 + e["y"]**2)
            if dist < ENEMY_RADIUS + TOWER_RADIUS:
                Tower_Current_HP -= 1
                enemies.remove(e)
                enemies.append(create_enemies_list(e["kind"], e["target"]))

                if Tower_Current_HP <= 0:
                    Game_over = True
                break

            #Collide with player
            dist = math.sqrt(
                (player_x - e["x"])**2 +
                (player_y - e["y"])**2
            )

            if dist < ENEMY_RADIUS + PLAYER_RADIUS:
                Player_Current_HP -= 1
                enemies.remove(e)
                enemies.append(create_enemies_list(e["kind"], e["target"]))

                if Player_Current_HP <= 0:
                    Game_over = True
                break
            
            obs=obstacle_collision(e["x"],e["y"])

            #obastacle Check  
            if obs is not None:         
                if obs["type"]=="spike":
                    if e["hp"]<=2:
                            enemies.remove(e)
                            Game_Max_point+=1
                            Game_Current_point+=1
                            enemies.append(create_enemies_list(e["kind"],e["target"]))
                    
                    else:
                            e["hp"]-=2

#Bullet
def create_bullet_list():
    global Player_face_angle,Current_bullet
    if Current_bullet>0:
        dx= math.cos(math.radians(Player_face_angle))
        dy=math.sin(math.radians(Player_face_angle))
        bullet_x=player_x+(dx*150)
        bullet_y=player_y+(dy*150)
        bullets.append([bullet_x,bullet_y,dx,dy])
        Current_bullet-=1

def draw_bullet():
    for b in bullets:
        glPushMatrix()
        glTranslatef(b[0], b[1],110)
        glColor3f(0.15, 0.15, 0.15)
        glScalef(12, 12, 12)
        glutSolidCube(1.0)
        glPopMatrix()

def bullet_movement(dt):
    bullet_speed=500
    for b in bullets[:]:
            b[0]+=b[2]*(bullet_speed*dt)
            b[1]+=b[3]*(bullet_speed*dt)
            
            if (b[0]<-GRID_LENGTH or b[0] > GRID_LENGTH or b[1] < -GRID_LENGTH or b[1] > GRID_LENGTH):
                bullets.remove(b)

def bullet_hit_enemy():
    global Game_Current_point,Game_Max_point
    for b1 in bullets[:]:
            for e1 in enemies[:]:
                dis=math.sqrt((b1[0]-e1["x"])**2 + (b1[1]-e1["y"])**2 )
                if dis < 30+12: #enemies radi , bullet scale
                    if b1 in bullets:
                        bullets.remove(b1)
                    else:
                        break
                    if e1["hp"]==1:
                        if e1 in enemies:
                            enemies.remove(e1)
                        else:
                            break
                        Game_Max_point+=1
                        Game_Current_point+=1
                        enemies.append(create_enemies_list(e1["kind"],e1["target"]))
                        break
                    else:
                        e1["hp"]-=1
                        break

#Game Wave Change
def update_Game_wave_by_time():
    global Game_wave, Game_Wave_Start_Time,Player_Max_HP,Player_Current_HP,Game_win

    elapsed = time.time() - Game_Wave_Start_Time

    # Wave 1 → 30s
    if Game_wave == 1 and elapsed >= 30:
        Player_Current_HP=Player_Max_HP
        Game_wave = 2
        Game_Wave_Start_Time = time.time()
        spawn_enemy_per_wave()

    # Wave 2 → 60s
    elif Game_wave == 2 and elapsed >= 90:
        Player_Current_HP=Player_Max_HP
        Game_wave = 3
        Game_Wave_Start_Time = time.time()
        spawn_enemy_per_wave()
    elif Game_wave == 3 and elapsed >= 90:
        if not Game_over:
            Game_win = True
    

#Upgarde HP
def Increase_Player_HP():
    global Game_Current_point,Player_Max_HP,Player_Current_HP
    if Game_Current_point < 2: # Minimum two points needed to buy HP
        return
    if Player_Current_HP == Player_Max_HP:
        return
    Game_Current_point -= 2
    Player_Current_HP += 1

def Increase_Tower_HP():
    global Game_Current_point, Tower_Current_HP, Tower_max_HP
    if Tower_Current_HP == Tower_max_HP:
        return
    if Game_Current_point < 3:
        return
    Game_Current_point -= 3

    Tower_Current_HP+=1

#Restart
def restrart():
    global camera_z_axis_position,camera_angle,view_mode,first_person_mode,Starting_Time

    global player_x,player_y,  Player_face_angle,player_min_position,player_max_postion,Player_Current_HP,Player_Max_HP,RID_LENGTH
    global obstacles,Obstacle_last_time,build_mode
    global Tower_max_HP,Tower_Current_HP
    global enemies,enemy_scale_over_time, enemy_shrink_last_time
    global bullets ,Max_bullet_limit, Current_bullet
    global Game_over,Game_Current_point,Game_Max_point,paused,Game_wave,Game_Wave_Start_Time

    # Camera-related variables
    Starting_Time=time.time()
    camera_z_axis_position=500
    camera_angle=0
    view_mode=0
    first_person_mode=False

    #Player Variable
    player_x=500
    player_y=0
    Player_face_angle=180

    player_min_position=-GRID_LENGTH+50
    player_max_postion=GRID_LENGTH-50

    Player_Current_HP=10
    Player_Max_HP=10

    #Obstacle
    obstacles = []
    build_mode = "wall"
    Obstacle_last_time=time.time()

    #Tower
    Tower_max_HP=20
    Tower_Current_HP=20

    #Enemy
    enemies=[]
    enemy_scale_over_time=0
    enemy_shrink_last_time=time.time()

    #Bullet
    bullets=[]
    Max_bullet_limit=30
    Current_bullet=30

    #Game parameter
    Game_over=False
    Game_Current_point=690
    Game_Max_point=0
    paused=False
    Game_wave=1
    Game_Wave_Start_Time=time.time()

pause_start_time=0.0  
def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global view_mode,Game_over,Player_face_angle,player_x,player_y,build_mode,paused,Max_bullet_limit,Current_bullet,Game_Current_point

    if key == b'r':
        restrart()
        spawn_enemy_per_wave()
        glutPostRedisplay()
        return
    if Game_over:
        glutPostRedisplay()
        return
    if key == b' ':
        global pause_start_time,Starting_Time,Game_Wave_Start_Time,Obstacle_last_time,enemy_shrink_last_time

        if not paused:
            paused=True
            pause_start_time=time.time()
        else:
            paused=False
            paused_duration=time.time()-pause_start_time
            Starting_Time+=paused_duration #Freeze sky transition time
            Game_Wave_Start_Time+=paused_duration #Freeze wave timer so enemies don't spawn instantly
            Obstacle_last_time+=paused_duration #Freeze obstacle decay so they don't vanish instantly
            enemy_shrink_last_time+=paused_duration #prevent dt spike in enemy animation timer
        glutPostRedisplay()
        return
    if paused:
        glutPostRedisplay()
        return
     # # Move forward (W key)
    if key == b'w':
        dx= math.cos(math.radians(Player_face_angle))
        dy=math.sin(math.radians(Player_face_angle))
        prevx=player_x
        player_x+=dx*30
        if player_min_position>player_x or player_x>player_max_postion or collide_with_tower(player_x,player_y) or obstacle_collision(player_x, player_y):
            player_x=prevx
        prevy=player_y
        player_y+=dy*30
        if player_min_position>player_y or player_y>player_max_postion or collide_with_tower(player_x,player_y) or obstacle_collision(player_x, player_y):
            player_y=prevy


    # # Move backward (S key)
    if key == b's':
        dx= math.cos(math.radians(Player_face_angle))
        dy=math.sin(math.radians(Player_face_angle))
        prevx=player_x
        prevy=player_y
        player_x-=dx*30
        player_y-=dy*30
        if player_min_position>player_x or player_x>player_max_postion or collide_with_tower(player_x,player_y) or obstacle_collision(player_x, player_y):
            player_x=prevx
        if player_min_position>player_y or player_y>player_max_postion or collide_with_tower(player_x,player_y) or obstacle_collision(player_x, player_y):
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
    
    if key == b't':
        if build_mode == "wall" :
             build_mode = "spike"
        else:
            build_mode="wall"
        return
    
    if key == b'e':
        place_obstacle()
        glutPostRedisplay()
        return
    
    if key == b'm':
        if Current_bullet==Max_bullet_limit or Game_Current_point<1:
            glutPostRedisplay()
            return
        
        Game_Current_point-=1
        Current_bullet+=3
        if Current_bullet>Max_bullet_limit:
            Current_bullet=Max_bullet_limit
        glutPostRedisplay()
        return


    # # Toggle cheat vision (V key)
    # if key == b'v':

    # # Reset the game if R key is pressed
    # if key == b'r':
    if key == b'1':
        Increase_Player_HP()
        glutPostRedisplay()
        return

    if key == b'2':
        Increase_Tower_HP()
        glutPostRedisplay()
        return
    
    

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
    
    if paused or Game_over: #block all mouse actions during pause and game over
        glutPostRedisplay()
        return
    
    if button == GLUT_LEFT_BUTTON:
        if not Game_over:
            create_bullet_list()

    elif button == GLUT_RIGHT_BUTTON:
        first_person_mode= not first_person_mode

    glutPostRedisplay()



def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    global enemy_shrink_last_time, enemy_scale_over_time

    now = time.time()
    if enemy_shrink_last_time == 0.0:
        enemy_shrink_last_time = now

    dt = now - enemy_shrink_last_time
    enemy_shrink_last_time = now
    dt = min(max(dt, 0.0), 0.05)

    if not paused and not Game_over :
        enemy_scale_over_time += dt
        bullet_movement(dt)
        enemy_movement(dt)
        enemy_collision()
        bullet_hit_enemy()


        update_Game_wave_by_time()
        update_obstacles()
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
    if not paused:
        Day_Night_Transition()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, window_width,window_height)  # Set viewport size

    setupCamera()  # Configure camera perspective

    #Environment Setup
    draw_outer_full_ground()
    draw_arena()
    draw_obstacles()

    #Characters
    draw_Tower()
    draw_enemy()
    draw_player()
    draw_bullet()

    
    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(window_width, window_height)  # Window size
    glutInitWindowPosition(150, 0)  # Window position
    glutCreateWindow(b"Defend The Tower")  # Create the window

    #Initialize enemy
    spawn_enemy_per_wave()

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()