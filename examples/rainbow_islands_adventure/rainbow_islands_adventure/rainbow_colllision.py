import pygame,sys
from math import radians,degrees,cos,sin,atan2,sqrt
from pygame.locals import *

#How to calculate Chord Length of a Circle:
#c = 2Rsin(θ/2)
#https://owlcation.com/stem/How-to-Calculate-the-Arc-Length-of-a-Circle-Segment-and-Sector-Area

pygame.init()

BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]

#Open Pygame window
screen = pygame.display.set_mode((640, 480),) #add RESIZABLE or FULLSCREEN
#Title
pygame.display.set_caption("rainbow islands")

circle1_center=[60,100]
circle1_radius=50
move_speed=10
collision_under_center=False

circle2_center=[400,300]
circle2_radius=150
pi=3.14
circle2_circomference=2*pi*circle2_radius
rot_speed=360/circle2_circomference*move_speed
right_rot_speed=rot_speed
left_rot_speed=-rot_speed
move_type=""

push_vector_pos=[0,0]


def circle_collision():
    collision=0
    push_vector=[0,0]
    c1=circle1_center
    c2=circle2_center
    lenght1=sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)
    lenght2=circle1_radius+circle2_radius
    if lenght2>lenght1:
       collision=1
       push_vector_lenght=lenght2-lenght1
       if lenght1==0:
          lenght1=1
       push_vector[0]=int((c1[0]-c2[0])/lenght1*push_vector_lenght)
       push_vector[1]=int((c1[1]-c2[1])/lenght1*push_vector_lenght)
    return collision,push_vector

def circle_collision2():
    collision=0
    push_vector=[0,0]
    push_vector_pos=[0,0]
    c1=circle1_center
    c2=circle2_center
    lenght1=sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)
    lenght2=circle1_radius+circle2_radius
    if lenght2>lenght1:
       collision=1
       push_vector_lenght=lenght2-lenght1
       if lenght1==0:
          lenght1=1
       push_vector_pos[0]=(c1[0]+((c2[0]-c1[0])/lenght1*circle1_radius))
       push_vector_pos[0]=int(push_vector_pos[0])
       push_vector_pos[1]=(c1[1]+((c2[1]-c1[1])/lenght1*circle1_radius))
       push_vector_pos[1]=int(push_vector_pos[1])
       if push_vector_pos[0]>circle2_center[0]:
          push_vector[0]=int(sqrt(circle2_radius**2-(circle2_center[1]-push_vector_pos[1])**2)-(push_vector_pos[0]-circle2_center[0]))
       else:
          push_vector[0]=-int(sqrt(circle2_radius**2-(circle2_center[1]-push_vector_pos[1])**2)-(circle2_center[0]-push_vector_pos[0])) 
       push_vector[1]=-int(sqrt(circle2_radius**2-(circle2_center[0]-push_vector_pos[0])**2)-(circle2_center[1]-push_vector_pos[1]))       
    return collision,push_vector,push_vector_pos

def orbital_rotation(angle):
    """z axis rotation
       x = x*cos(a) - y*sin(a)
       y = x*sin(a) + y*cos(a)"""
    sphere_pos=circle1_center
    orbit_pos=circle2_center
    sphere_pos[0]-=orbit_pos[0]
    sphere_pos[1]-=orbit_pos[1]
    x=sphere_pos[0]
    y=sphere_pos[1]    
    sphere_pos[0]=x*cos(radians(angle))-y*sin(radians(angle))
    sphere_pos[1]=x*sin(radians(angle))+y*cos(radians(angle))
    sphere_pos[0]+=orbit_pos[0]
    sphere_pos[1]+=orbit_pos[1]
    sphere_pos[0]=int(sphere_pos[0])
    sphere_pos[1]=int(sphere_pos[1])

   
pygame.key.set_repeat(400, 30)

while True:
    #loop speed limitation
    #30 frames per second is enought
    pygame.time.Clock().tick(30)
    
    for event in pygame.event.get():    #wait for events
        if event.type == QUIT:
            pygame.quit()
            sys.exit()  
        #keyboard movement commands    
        if event.type == KEYDOWN:
            if event.key == K_UP:
               circle1_center[1]-=move_speed
            elif event.key == K_DOWN:
               circle1_center[1]+=move_speed
               move_type="vertical"
            if event.key == K_LEFT:
               circle1_center[0]-=move_speed
               rot_speed=left_rot_speed
               move_type="horizontal"
            elif event.key == K_RIGHT:
               circle1_center[0]+=move_speed
               rot_speed=right_rot_speed
               move_type="horizontal"
            collision,push_vector,push_vector_pos=circle_collision2()
            if collision:
               if circle1_center[1]<circle2_center[1] and not collision_under_center:
                  if move_type=="horizontal":
                     circle1_center[0]+=push_vector[0]
                     orbital_rotation(rot_speed)
                  elif move_type=="vertical":
                     circle1_center[1]+=push_vector[1]
               else:
                  collision_under_center=True
            else:
               collision_under_center=False
               
               
    #blit things and refresh screen
    screen.fill(BLACK)
    pygame.draw.circle(screen,WHITE,circle1_center,circle1_radius,5)
    pygame.draw.circle(screen,WHITE,circle2_center,circle2_radius,5)
    line_start=[circle2_center[0]-circle2_radius,circle2_center[1]]
    line_end=[circle2_center[0]+circle2_radius,circle2_center[1]]
    pygame.draw.line(screen,WHITE,line_start,line_end,5)
    #pygame.draw.line(screen,WHITE,circle1_center,circle2_center,5)
    #pygame.draw.circle(screen,(255,0,0),push_vector_pos,5,5)
    pygame.display.flip()
