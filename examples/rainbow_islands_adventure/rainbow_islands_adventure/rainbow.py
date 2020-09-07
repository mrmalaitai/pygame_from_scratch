import pygame,sys
from math import radians,degrees,cos,sin,atan2,sqrt
from pygame.locals import *


BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
YELLOW=pygame.color.THECOLORS["yellow"]
ORANGE=pygame.color.THECOLORS["orange"]


def orbital_rotation(orbit_pos,sphere_pos,angle):
    """x = x*cos(a) - y*sin(a)
       y = x*sin(a) + y*cos(a)"""
    sphere_pos[0]-=orbit_pos[0]
    sphere_pos[1]-=orbit_pos[1]
    x=sphere_pos[0]
    y=sphere_pos[1]    
    sphere_pos[0]=x*cos(radians(angle))-y*sin(radians(angle))
    sphere_pos[1]=x*sin(radians(angle))+y*cos(radians(angle))
    sphere_pos[0]+=orbit_pos[0]
    sphere_pos[1]+=orbit_pos[1]

def draw_filled_star(surface,color1,rect,thickness=1,color2=YELLOW): 
    x=rect[0]
    y=rect[1]
    width=rect[2]
    height=rect[3]
    half_width=int(rect[2]/2)
    half_height=int(rect[3]/2)
    x_offset=int(half_width/3)
    y_offset=int(half_height/3)
    point1=[x+half_width, y+y_offset]
    point2=[x+x_offset,y+height]
    point3=[x+width, y+half_height]
    point4=[x, y+half_height]
    point5=[x+width-x_offset, y+height]
    pointlist=[point1,point2,point3,point4,point5]
    pygame.draw.lines(surface, color1, True, pointlist,thickness)
    if width>5:
        rect=[x+thickness,y+thickness,width-thickness*2,height-thickness*2]
        draw_filled_star(surface,color2,rect,thickness,color2)
        
def rotate_center(surface,surface_pos,surface_angle,rot_angle):
    surface_angle+=rot_angle
    surface_rot_pos=[0,0]
    rot_image=pygame.transform.rotate(surface,surface_angle)
    dx=(surface.get_width()/2)-(rot_image.get_width()/2)
    dy=(surface.get_height()/2)-(rot_image.get_height()/2)
    surface_rot_pos[0]=surface_pos[0]+dx
    surface_rot_pos[1]=surface_pos[1]+dy
    return rot_image,surface_rot_pos
           
def make_rainbow_images():
    rot_num=16
    rot_speed=180/rot_num
    rainbow_scale=3
    rainbow_width=(256/4)*rainbow_scale
    rainbow_height=(256/4)/2*rainbow_scale
    rainbow_radius=int(rainbow_width/2)
    rainbow_colors=[pygame.color.THECOLORS[color] for color in ("red","orange","yellow","green","blue","purple")]
    rainbow_image=pygame.Surface((rainbow_width,rainbow_height))#.convert()
    alpha_color=rainbow_image.get_at((0,0))
    rainbow_image.set_colorkey(alpha_color)
    rainbow_images=[]
    rainbow_vanish_images=[]
    polygon_points=[[96, 96], [-104, 96], [-104, -104], [296, -104], [296,96]]
    sphere_pos=polygon_points[1]
    orbit_pos=polygon_points[0]
    rotated_angle=180
    star_pos=[(orbit_pos[0]-rainbow_radius)+20,orbit_pos[1]]
    hit_box_pos=[(orbit_pos[0]-rainbow_radius)+15,orbit_pos[1],35,35]
    star_image=pygame.Surface((35,35))
    star_image.set_colorkey(alpha_color)
    draw_filled_star(star_image,ORANGE,[0,0,35,35],5)
    star_pos_list=[]
    star_image_list=[]
    rainbow_hit_box_list=[]
    star_image_angle=90
    
    
    color_pos_offset=0
    for color in rainbow_colors:
        pygame.draw.circle(rainbow_image,color,orbit_pos,rainbow_radius-color_pos_offset,5)
        color_pos_offset+=5
        rainbow_vanish_images.append(rainbow_image.copy())
    rainbow_vanish_images.reverse()
    
    for i in range(rot_num):
        orbital_rotation(orbit_pos,sphere_pos,rot_speed)
        orbital_rotation(orbit_pos,star_pos,rot_speed)
        orbital_rotation(orbit_pos,hit_box_pos,rot_speed)
        rot_star_image,pos=rotate_center(star_image,star_pos,-star_image_angle,rot_speed)
        star_image_angle+=rot_speed
        star_pos_list.append([pos[0]-17, pos[1]-17])
        rainbow_hit_box_list.append([hit_box_pos[0]-17,hit_box_pos[1]-17,35,35])#rainbow_radius-(hit_box_pos[1]-17)])
        star_image_list.append(rot_star_image)
        rotated_angle=degrees(atan2(sphere_pos[1]-orbit_pos[1],sphere_pos[0]-orbit_pos[0]))
        for j in range(len(polygon_points)-1,1,-1):
            sphere=polygon_points[j]
            angle=degrees(atan2(sphere[1]-orbit_pos[1],sphere[0]-orbit_pos[0]))
            if angle<rotated_angle:
               if len(polygon_points)>3:
                  del(polygon_points[j])
        image=rainbow_image.copy()
        pygame.draw.polygon(image, BLACK, polygon_points, 0)
        rainbow_images.append(image)
    for i in range(0,len(rainbow_images)-1,1):
        rainbow_images[i].blit(star_image_list[i],(star_pos_list[i][0], star_pos_list[i][1]))
    return rainbow_images,rainbow_vanish_images,rainbow_hit_box_list



def main():
    
    pygame.init()

    #Open Pygame window
    screen = pygame.display.set_mode((640, 480),) #add RESIZABLE or FULLSCREEN
    #Title
    pygame.display.set_caption("rainbow islands")
    #font
    font=pygame.font.SysFont('Arial', 30)

    polygon_points=[[320, 300], [120, 300], [120, 100], [520, 100], [520,300]]
    radius=200
    pi=3.14
    rot_num=16
    rot_speed=180/rot_num
    rot_time=0
    max_rot_time=1
    rotations=0
    rotated_angle=180
    sphere_pos=polygon_points[1]
    orbit_pos=polygon_points[0]

    rainbow_scale=3
    rainbow_width=(256/4)*rainbow_scale
    rainbow_height=(256/4)/2*rainbow_scale
    rainbow_radius=int(rainbow_width/2)
    rainbow_colors=[pygame.color.THECOLORS[color] for color in ("red","orange","yellow","green","blue","purple")]
        
    rainbow_image=pygame.Surface((rainbow_width,rainbow_height)).convert()
    alpha_color=rainbow_image.get_at((0,0))
    rainbow_image.set_colorkey(alpha_color)
    rainbow_images=[]
    rainbow_images_index=0
    rainbow_vanish_images=[]
    rainbow_vanish_images_index=0
    rainbow_vanish=False
    rainbow_vanish_time=0
    rainbow_vanish_max_time=1
  
    rainbow_images,rainbow_vanish_images,rainbow_hit_box_list=make_rainbow_images()
    
       
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
                if event.key == K_SPACE:
                   polygon_points=[[320, 300], [120, 300], [120, 100], [520, 100], [520,300]]
                   sphere_pos=polygon_points[1]
                   orbit_pos=polygon_points[0]
                   rotated_angle=180
                   rotations=0
                   rot_time=0
                   star_pos=[(orbit_pos[0]-rainbow_radius)+15,orbit_pos[1]]
                if event.key == K_RIGHT:
                   rainbow_images_index+=1
                   if rainbow_images_index>=len(rainbow_images):
                      rainbow_images_index=0
                if event.key == K_UP:
                   rainbow_vanish=True

                   
        if rotations<=rot_num:         
           if rot_time<max_rot_time:
              rot_time+=1
           else:
              orbital_rotation(orbit_pos,sphere_pos,rot_speed)
              rotations+=1
              rot_time=0
              #rotated_angle-=rot_speed
              rotated_angle=degrees(atan2(sphere_pos[1]-orbit_pos[1],sphere_pos[0]-orbit_pos[0]))
              for i in range(len(polygon_points)-1,1,-1):
                  sphere=polygon_points[i]
                  angle=degrees(atan2(sphere[1]-orbit_pos[1],sphere[0]-orbit_pos[0]))
                  if angle<rotated_angle:
                     if len(polygon_points)>3:
                        del(polygon_points[i])
            
        #blit things and refresh screen
        screen.fill(BLACK)
        color_pos_offset=0
        for color in rainbow_colors:
            pygame.draw.circle(screen,color,orbit_pos,rainbow_radius-color_pos_offset,5)
            color_pos_offset+=5
        pygame.draw.polygon(screen, WHITE, polygon_points, 0)
        pygame.draw.rect(screen, (0,255,0), [224, 204, rainbow_width, rainbow_height], 5)
        for point in polygon_points:
            pygame.draw.circle(screen,(255,0,0),(int(point[0]),int(point[1])),5,5)
        screen.blit(rainbow_images[rotations%len(rainbow_images)],(10,374))
        screen.blit(rainbow_images[rainbow_images_index],(438,374))
        
        if rainbow_vanish:
           screen.blit(rainbow_vanish_images[rainbow_vanish_images_index],(224,10))
           if rainbow_vanish_time>=rainbow_vanish_max_time:
              rainbow_vanish_time=0
              rainbow_vanish_images_index+=1
              if rainbow_vanish_images_index>=len(rainbow_vanish_images):
                 rainbow_vanish_images_index=0
                 rainbow_vanish=False
           else:
              rainbow_vanish_time+=1
        text=font.render(str(rotations), True, (250,250,250))
        screen.blit(text,(0,0))
        pygame.display.flip()

if __name__ == "__main__":
    main()
