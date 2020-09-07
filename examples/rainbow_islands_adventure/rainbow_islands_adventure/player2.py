import pygame,sys
from math import radians,degrees,cos,sin,atan2,sqrt
from pygame.locals import *
import rainbow

BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
GREEN=pygame.color.THECOLORS["green"]
SCREEN_WIDTH=640
SCREEN_HEIGHT=480
SCALE=2


def player_get_sprites(image,scale=None):
    player_sprites={}
    image=pygame.image.load(image).convert()
    alpha_color=image.get_at((0,0))
    image.set_colorkey(alpha_color)
    sprites_per_row=8
    sprites_per_column=5
    sprite_width=int(image.get_width()/sprites_per_row)
    sprite_height=sprite_width
    right_sprites=[]
    left_sprites=[]
    for i in range(sprites_per_column):
        for j in range(sprites_per_row):
            right_sprite=image.subsurface(j*sprite_width,i*sprite_height,sprite_width,sprite_height)
            left_sprite=pygame.transform.flip(right_sprite, True, False)
            if scale:
               right_sprite=pygame.transform.scale(right_sprite,(right_sprite.get_width()*scale,right_sprite.get_height()*scale))
               left_sprite=pygame.transform.scale(left_sprite,(left_sprite.get_width()*scale,left_sprite.get_height()*scale))
            right_sprites.append(right_sprite)
            left_sprites.append(left_sprite)
    player_sprites['right_idle']=right_sprites[0]  
    player_sprites['left_idle']=left_sprites[0]
    player_sprites['right_walk']=right_sprites[1:5]
    player_sprites['left_walk']=left_sprites[1:5]
    player_sprites['right_jump']=right_sprites[5:7]
    player_sprites['left_jump']=left_sprites[5:7]    
    player_sprites['right_fall']=right_sprites[11:13]
    player_sprites['left_fall']=left_sprites[11:13]
    player_sprites['right_speed_break']=right_sprites[13]
    player_sprites['left_speed_break']=left_sprites[13]
    player_sprites['left_fall']=left_sprites[11:13]
    player_sprites['dead']=right_sprites[22:34]
    for i in range(len(player_sprites['dead'])):
        player_sprites['dead'][i]=player_sprites['dead'][i].subsurface(0,2,sprite_width*SCALE,sprite_height*SCALE-2)
       
    sprites_lenght={}
    sprites_lenght['idle']=1
    sprites_lenght['walk']=len(player_sprites['right_walk'])
    sprites_lenght['jump']=len(player_sprites['right_jump'])
    sprites_lenght['fall']=len(player_sprites['right_fall'])
    sprites_lenght['speed_break']=1
    sprites_lenght['dead']=len(player_sprites['dead'])
    player_sprites['sprites_lenght']=sprites_lenght
    
    return player_sprites
    
class Player():
    def __init__(self,pos):
        self.sprites=player_get_sprites("Arcade - Rainbow Islands - Bubby and Bobby.png",SCALE)
        self.current_sprite=self.sprites['right_idle']
        self.anim_sequence=[]
        self.anim_sequence_lenght=self.sprites['sprites_lenght']['idle']
        self.anim_time=0
        self.max_anim_time=3
        self.anim_index=0
        self.width=self.current_sprite.get_width()
        self.height=self.current_sprite.get_height()
        self.rainbows=[]
        self.mounted_rainbow=None
        self.pos=pos
        self.move_speed=5
        self.jump_speed=5
        self.xvel=0
        self.yvel=0
        self.timer=0
        self.bounding_box=[15,11,35,47]
        self.center=[self.pos[0]+int(self.width/2),self.pos[1]+int(self.height/2)]
        self.radius=32        
        self.direction="right"
        self.current_state="idle"
        self.states={'idle':self.idle, 'walk':self.walk, 'jump':self.jump,'fall':self.fall,
                     'running':self.running, 'speed_break':self.speed_break, 'death':self.death,
                     'rainbow_walk':self.rainbow_walk}
        
    def idle(self):
        if right:
           if self.direction=="right":                 
              self.current_state="walk"
              self.anim_time=0
              self.anim_index=0
              self.max_anim_time=3
              self.anim_sequence=self.sprites['right_walk']
              self.current_sprite=self.anim_sequence[0]
              self.anim_sequence_lenght=self.sprites['sprites_lenght']['walk']
              if run:
                 self.current_state="running"
                 self.max_anim_time=2
           elif self.direction=="left":
              self.direction="right"
              self.current_sprite=self.sprites['right_idle']
        elif left:
           if self.direction=="left":
              self.current_state="walk"
              self.anim_time=0
              self.anim_index=0
              self.max_anim_time=3
              self.anim_sequence=self.sprites['left_walk']
              self.current_sprite=self.anim_sequence[0]
              self.anim_sequence_lenght=self.sprites['sprites_lenght']['walk']
              if run:
                 self.current_state="running"
                 self.max_anim_time=2
           elif self.direction=="right":
              self.direction="left"
              self.current_sprite=self.sprites['left_idle']
        if up:
           self.current_state="jump"
           self.yvel-=self.jump_speed
           self.anim_time=0
           self.anim_index=0
           self.max_anim_time=5
           self.anim_sequence=self.sprites[self.direction+'_jump']
           self.current_sprite=self.anim_sequence[0]
           self.anim_sequence_lenght=self.sprites['sprites_lenght']['jump']
            
    def walk(self,):
        if right:
           if self.direction=="right":                 
              self.pos[0]+=self.move_speed
              
              if self.anim_time>=self.max_anim_time:
                 self.anim_time=0
                 self.anim_index+=1
                 if self.anim_index>=self.anim_sequence_lenght:
                    self.anim_index=0
                 self.current_sprite=self.anim_sequence[self.anim_index]
              self.anim_time+=1

           elif self.direction=="left":
              self.direction="right"
              self.anim_sequence=self.sprites['right_walk']
           if run:
              self.current_state="running"
              self.max_anim_time=2

        elif left:
           if self.direction=="left":                 
              self.pos[0]-=self.move_speed
              
              if self.anim_time>=self.max_anim_time:
                 self.anim_time=0
                 self.anim_index+=1
                 if self.anim_index>=self.anim_sequence_lenght:
                    self.anim_index=0
                 self.current_sprite=self.anim_sequence[self.anim_index]
              self.anim_time+=1
              
           elif self.direction=="right":
              self.direction="left"
              self.anim_sequence=self.sprites['left_walk']
           if run:
              self.current_state="running"
              self.max_anim_time=2
        else:
           self.current_state="idle"
           self.current_sprite=self.sprites[self.direction+'_idle']
            
        if up:
           self.current_state="jump"
           self.yvel-=self.jump_speed
           self.anim_time=0
           self.anim_index=0
           self.max_anim_time=5
           self.anim_sequence=self.sprites[self.direction+'_jump']
           self.current_sprite=self.anim_sequence[0]
           self.anim_sequence_lenght=self.sprites['sprites_lenght']['jump']
           
    def jump(self):        
        if up:
           self.pos[1]-=self.jump_speed
        if right:
           if self.direction=="right":                 
              self.pos[0]+=self.move_speed
           elif self.direction=="left" and not self.xvel>0:
              self.direction="right"
              self.anim_sequence=self.sprites['right_jump']
        elif left:
           if self.direction=="left":                 
              self.pos[0]-=self.move_speed              
           elif self.direction=="right" and not self.xvel>0:
              self.direction="left"
              self.anim_sequence=self.sprites['left_jump']
           
        if self.anim_time>=self.max_anim_time:
           self.anim_time=0
           self.anim_index+=1
           if self.anim_index>=self.anim_sequence_lenght:
              self.anim_index=0
           self.current_sprite=self.anim_sequence[self.anim_index]
        self.anim_time+=1
            
        self.pos[1]+=self.yvel
        self.yvel+=gravity
        if self.yvel > max_fall_speed:
           self.yvel=max_fall_speed
        if self.yvel>0:
           self.current_state="fall"
           self.anim_time=0
           self.anim_index=0
           self.max_anim_time=5
           self.anim_sequence=self.sprites[self.direction+'_fall']
           self.current_sprite=self.anim_sequence[0]
           self.anim_sequence_lenght=self.sprites['sprites_lenght']['fall']

        if self.xvel>0:   
           if self.direction=="right":
              self.pos[0]+=self.xvel
           elif self.direction=="left":
                self.pos[0]-=self.xvel
           self.xvel-=friction
           if self.xvel<0:
              self.xvel=0
                             
    def fall(self):
        if right:
           if self.direction=="right":                 
              self.pos[0]+=self.move_speed
           elif self.direction=="left" and not self.xvel>0:
              self.direction="right"
              self.anim_sequence=self.sprites['right_fall']
        elif left:
           if self.direction=="left":                 
              self.pos[0]-=self.move_speed              
           elif self.direction=="right" and not self.xvel>0:
              self.direction="left"
              self.anim_sequence=self.sprites['left_fall']
              
        if self.anim_time>=self.max_anim_time:
           self.anim_time=0
           self.anim_index+=1
           if self.anim_index>=self.anim_sequence_lenght:
              self.anim_index=0
           self.current_sprite=self.anim_sequence[self.anim_index]
        self.anim_time+=1
        
        self.pos[1]+=self.yvel
        self.yvel+=gravity
        if self.yvel > max_fall_speed:
           self.yvel=max_fall_speed
        if self.pos[1]+sprite_height>floor_pos:
           self.pos[1]=floor_pos-sprite_height
           self.yvel=0
           if self.xvel>0:
              self.current_state="running"
              self.anim_time=0
              self.anim_index=0
              self.max_anim_time=2
              self.anim_sequence=self.sprites[self.direction+'_walk']
              self.current_sprite=self.anim_sequence[0]
              self.anim_sequence_lenght=self.sprites['sprites_lenght']['walk']
           else:
              self.current_state="idle"
              self.current_sprite=self.sprites[self.direction+'_idle']
           
        if self.xvel>0:   
           if self.direction=="right":
              self.pos[0]+=self.xvel
           elif self.direction=="left":
                self.pos[0]-=self.xvel
           self.xvel-=friction
           if self.xvel<0:
              self.xvel=0

    def running(self):
        if self.anim_time>=self.max_anim_time:
           self.anim_time=0
           self.anim_index+=1
           if self.anim_index>=self.anim_sequence_lenght:
              self.anim_index=0
           self.current_sprite=self.anim_sequence[self.anim_index]
        self.anim_time+=1
        
        if right:
           if self.direction=="right":                 
              self.pos[0]+=self.move_speed
              if self.xvel<15 and run:
                 self.xvel+=1
           elif self.direction=="left":
              self.current_state="speed_break"
              self.current_sprite=self.sprites[self.direction+'_speed_break']
              
        elif left:
           if self.direction=="left":                 
              self.pos[0]-=self.move_speed
              if self.xvel<15 and run:
                 self.xvel+=1
           elif self.direction=="right":
              self.current_state="speed_break"
              self.current_sprite=self.sprites[self.direction+'_speed_break']
                            
        if up:
           self.current_state="jump"
           self.yvel-=self.jump_speed
           self.anim_time=0
           self.anim_index=0
           self.max_anim_time=8
           self.anim_sequence=self.sprites[self.direction+'_jump']
           self.current_sprite=self.anim_sequence[0]
           self.anim_sequence_lenght=self.sprites['sprites_lenght']['jump']
           
        if self.direction=="right":
           self.pos[0]+=self.xvel
        elif self.direction=="left":
             self.pos[0]-=self.xvel
        self.xvel-=friction
        if self.xvel<0:
           self.current_state="walk"
           self.xvel=0
           self.max_anim_time=3
           
    def speed_break(self):           
        if self.direction=="right":
           self.pos[0]+=self.xvel
        elif self.direction=="left":
             self.pos[0]-=self.xvel
        self.xvel-=friction+0.3
        if self.xvel<0:
           self.xvel=0
           self.current_state="idle"
           self.current_sprite=self.sprites[self.direction+'_idle']
           
        if up:
           self.current_state="jump"
           self.yvel-=self.jump_speed
           self.anim_time=0
           self.anim_index=0
           self.max_anim_time=8
           self.anim_sequence=self.sprites[self.direction+'_jump']
           self.current_sprite=self.anim_sequence[0]
           self.anim_sequence_lenght=self.sprites['sprites_lenght']['jump']
           
    def death(self):
        if self.timer<30:
           self.pos[1]-=self.jump_speed
           self.timer+=1
        elif self.timer<60:
           self.pos[1]+=self.jump_speed
           if self.pos[1]+sprite_height>floor_pos:
              self.pos[1]=floor_pos-sprite_height
              self.anim_sequence=self.sprites['dead'][3:6]
              self.current_sprite=self.anim_sequence[0]
              self.anim_time=0
              self.anim_index=0
              self.max_anim_time=3
              self.anim_sequence_lenght=3
              self.timer=60
        elif self.timer<70:
           self.timer+=1
           if self.timer>=70:
              self.timer=70
              self.anim_sequence=self.sprites['dead'][6:10]
              self.current_sprite=self.anim_sequence[0]
              self.anim_time=0
              self.anim_index=0
              self.max_anim_time=3
              self.anim_sequence_lenght=4
        elif self.timer<100:
           self.timer+=1
           if self.timer>=100:
              self.timer=100
              self.anim_sequence=self.sprites['dead'][-2:]
              self.current_sprite=self.anim_sequence[0]
              self.anim_time=0
              self.anim_index=0
              self.max_anim_time=3
              self.anim_sequence_lenght=2
        elif self.timer<105:
           self.timer+=1
           if self.timer>=105:
              self.timer=0
              self.current_state="idle"
  
        if self.anim_time>=self.max_anim_time:
           self.anim_time=0
           self.anim_index+=1
           if self.anim_index>=self.anim_sequence_lenght:
              self.anim_index=0
           self.current_sprite=self.anim_sequence[self.anim_index]
        self.anim_time+=1

    def cast_rainbow(self):
        if not self.rainbows or (self.rainbows and not self.rainbows[-1].current_phase=="start"):
           if self.direction=="right":
              self.rainbows.append(Rainbow([self.pos[0]+self.width,self.pos[1]+self.height-(96+6)],"right"))
           elif self.direction=="left":
              self.rainbows.append(Rainbow([self.pos[0]-192,self.pos[1]+self.height-(96+6)],"left"))
              
    def rainbow_walk(self):
        if self.mounted_rainbow.current_phase=="active":
           if right:
              if self.direction=="right":
                 self.anim_sequence=self.sprites['right_walk']
                 self.center=[self.pos[0]+32,self.pos[1]+32]
                 old_y_pos=self.pos[1]
                 rainbow_walk(self,self.mounted_rainbow,rot_speed['right'],32,32)
                 if self.pos[0]+sprite_width>SCREEN_WIDTH:
                    self.pos[1]=old_y_pos
                 if self.pos[1]+self.height>self.mounted_rainbow.center[1]+6:
                    self.pos[1]=self.mounted_rainbow.center[1]-self.height+6
                    self.current_state="walk"
                    self.mounted_rainbow=None
                    if self.pos[1]+self.height<floor_pos:
                       self.current_state="fall"
                       self.anim_time=0
                       self.anim_index=0
                       self.max_anim_time=5
                       self.anim_sequence=self.sprites['right_fall']
                       self.current_sprite=self.anim_sequence[0]
                       self.anim_sequence_lenght=self.sprites['sprites_lenght']['fall']

                    
                 if self.anim_time>=self.max_anim_time:
                    self.anim_time=0
                    self.anim_index+=1
                    if self.anim_index>=self.anim_sequence_lenght:
                       self.anim_index=0
                    self.current_sprite=self.anim_sequence[self.anim_index]
                 self.anim_time+=1

              elif self.direction=="left":
                 self.direction="right"
                 self.current_sprite=self.sprites['right_idle']

           elif left:
              if self.direction=="left":
                 self.anim_sequence=self.sprites['left_walk']
                 self.center=[self.pos[0]+32,self.pos[1]+32]
                 old_y_pos=self.pos[1]
                 rainbow_walk(self,self.mounted_rainbow,rot_speed['left'],32,32)
                 if self.pos[0]<0:
                    self.pos[1]=old_y_pos
                 if self.pos[1]+self.height>self.mounted_rainbow.center[1]+6:
                    self.pos[1]=self.mounted_rainbow.center[1]-self.height+6
                    self.current_state="walk"
                    self.mounted_rainbow=None
                    if self.pos[1]+self.height<floor_pos:
                       self.current_state="fall"
                       self.anim_time=0
                       self.anim_index=0
                       self.max_anim_time=5
                       self.anim_sequence=self.sprites['left_fall']
                       self.current_sprite=self.anim_sequence[0]
                       self.anim_sequence_lenght=self.sprites['sprites_lenght']['fall']
                    
                    
                 if self.anim_time>=self.max_anim_time:
                    self.anim_time=0
                    self.anim_index+=1
                    if self.anim_index>=self.anim_sequence_lenght:
                       self.anim_index=0
                    self.current_sprite=self.anim_sequence[self.anim_index]
                 self.anim_time+=1
                 
              elif self.direction=="right":
                 self.direction="left"
                 self.current_sprite=self.sprites['left_idle']
           else:
              self.anim_time=0
              self.anim_index=0
              self.current_sprite=self.sprites[self.direction+'_idle']
               
           if up:
              self.current_state="jump"
              self.yvel-=self.jump_speed
              self.anim_time=0
              self.anim_index=0
              self.max_anim_time=5
              self.anim_sequence=self.sprites[self.direction+'_jump']
              self.current_sprite=self.anim_sequence[0]
              self.anim_sequence_lenght=self.sprites['sprites_lenght']['jump']
              self.mounted_rainbow=None
        else:
           self.current_state="fall"
           self.anim_time=0
           self.anim_index=0
           self.max_anim_time=5
           self.anim_sequence=self.sprites[self.direction+'_fall']
           self.current_sprite=self.anim_sequence[0]
           self.anim_sequence_lenght=self.sprites['sprites_lenght']['fall']


class Rainbow():
    sprites={}
    right_rainbow_images,rainbow_vanish_images,hit_box_list=rainbow.make_rainbow_images()
    left_rainbow_images=[]
    for rainbow_image in right_rainbow_images:
        image=pygame.transform.flip(rainbow_image, True, False)
        left_rainbow_images.append(image)
    sprites['right']=right_rainbow_images
    sprites['left']=left_rainbow_images
    sprites['vanish']=rainbow_vanish_images
    
    def __init__(self,pos,direction):
        self.pos=pos
        self.direction=direction
        self.sprites=Rainbow.sprites
        self.current_phase="start"
        self.phases={'start':self.start,'active':self.active, 'vanish':self.vanish}
        self.width=self.sprites['right'][-1].get_width()
        self.height=self.sprites['right'][-1].get_height()
        self.radius=self.height-10
        self.center=[self.pos[0]+self.height,self.pos[1]+self.height]
        self.collision_under_center=False
        self.dead=False
        self.life_time=0
        self.max_life_time=500
        self.anim_time=0
        self.max_anim_time=1
        self.anim_index=0
        self.anim_sequence=self.sprites[direction]
        self.current_sprite=self.anim_sequence[0]
        self.start_sequence_lenght=len(self.sprites['right'])
        self.vanish_sequence_lenght=len(self.sprites['vanish'])
        
    def start(self):
        if self.anim_time>=self.max_anim_time:
           self.anim_time=0
           self.anim_index+=1
           if self.anim_index>=self.start_sequence_lenght:
              self.anim_index=self.start_sequence_lenght-1
              self.current_phase="active"     
           self.current_sprite=self.anim_sequence[self.anim_index]
        self.anim_time+=1

    def active(self):
        self.life_time+=1
        if self.life_time>=self.max_life_time:
           self.anim_time=0
           self.anim_index=0
           self.current_phase="vanish"
           self.anim_sequence=self.sprites["vanish"]
           self.current_sprite=self.anim_sequence[0]

    def vanish(self):
        if self.anim_time>=self.max_anim_time:
           self.anim_time=0
           self.anim_index+=1
           if self.anim_index>=self.vanish_sequence_lenght:
              self.anim_index=self.vanish_sequence_lenght-1
              self.dead=True
           self.current_sprite=self.anim_sequence[self.anim_index]
        self.anim_time+=1


def rainbow_collision(entity,rainbow):
    collision=0
    push_vector=[0,0]
    push_vector_pos=[0,0]
    c1=circle1_center=entity.center
    c2=circle2_center=rainbow.center
    circle1_radius=entity.radius
    circle2_radius=rainbow.radius
    lenght1=sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)
    lenght2=circle1_radius+circle2_radius
    if lenght2>lenght1:
       collision=1
       push_vector_lenght=lenght2-lenght1
       if lenght1==0:
          lenght1=1
       push_vector_pos[0]=(c1[0]+((c2[0]-c1[0])/lenght1*circle1_radius))
       push_vector_pos[1]=(c1[1]+((c2[1]-c1[1])/lenght1*circle1_radius))
       if push_vector_pos[0]>circle2_center[0]:
          push_vector[0]=(sqrt(circle2_radius**2-(circle2_center[1]-push_vector_pos[1])**2)-(push_vector_pos[0]-circle2_center[0]))+1
       else:
          push_vector[0]=-(sqrt(circle2_radius**2-(circle2_center[1]-push_vector_pos[1])**2)-(circle2_center[0]-push_vector_pos[0]))-1 
       push_vector[1]=-(sqrt(circle2_radius**2-(circle2_center[0]-push_vector_pos[0])**2)-(circle2_center[1]-push_vector_pos[1]))-1
    return collision,push_vector


def rainbow_walk(entity,rainbow,angle,center_xoffset,center_yoffset):
    """z axis rotation
       x = x*cos(a) - y*sin(a)
       y = x*sin(a) + y*cos(a)"""
    sphere_pos=entity.center
    orbit_pos=rainbow.center
    x=sphere_pos[0]-orbit_pos[0]
    y=sphere_pos[1]-orbit_pos[1]   
    entity.pos[0]=x*cos(radians(angle))-y*sin(radians(angle))+orbit_pos[0]-center_xoffset
    entity.pos[1]=x*sin(radians(angle))+y*cos(radians(angle))+orbit_pos[1]-center_yoffset


def main():
    
    pygame.init()

    #Open Pygame window
    screen = pygame.display.set_mode((640, 480),) #add RESIZABLE or FULLSCREEN
    #Title
    pygame.display.set_caption("rainbow islands")
    #font
    font=pygame.font.SysFont('Arial', 30)

    global up,down,right,left,run,gravity,friction,max_fall_speed,floor_pos,sprite_width,sprite_height,rot_speed

    pi=3.14
    move_speed=5
    rainbow_radius=96-10
    circle_circomference=2*pi*rainbow_radius
    rot_speed=360/circle_circomference*move_speed
    rot_speed={'right':rot_speed, 'left':-rot_speed}    
    
    image=pygame.image.load("Arcade - Rainbow Islands - Bubby and Bobby.png")
    image=pygame.transform.scale(image,(image.get_width()*SCALE,image.get_height()*SCALE))
    sprites_per_row=8
    sprite_width=int(image.get_width()/sprites_per_row)
    sprite_height=sprite_width

    floor_pos=SCREEN_HEIGHT-40
    player=Player([10,floor_pos-sprite_height])
    up=down=right=left=run=False
    gravity=0.4
    friction=0.5
    max_fall_speed=50
    
    #pygame.key.set_repeat(400, 30)

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
                if event.key == K_RIGHT:
                   right=True
                   left=False
                elif event.key == K_LEFT:
                   left=True
                   right=False
                if event.key == K_UP:
                   up=True
                if event.key == K_t:
                   run=True
                if event.key == K_r:
                   player.cast_rainbow()                                   
                if event.key == K_d:
                   if player.current_state!="death":
                      player.current_state="death"
                      player.anim_time=0
                      player.anim_index=0
                      player.max_anim_time=3
                      player.anim_sequence=player.sprites['dead'][0:3]
                      player.current_sprite=player.anim_sequence[0]
                      player.anim_sequence_lenght=3
                      player.timer=0
                      
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                   right=False
                elif event.key == K_LEFT:
                   left=False
                if event.key == K_UP:
                   up=False
                if event.key == K_t:
                   run=False
                      
        player.states[player.current_state]()
        
        if player.pos[0]<0:
           player.pos[0]=0
           if player.xvel>0:
              player.xvel-=1
        elif player.pos[0]+sprite_width>SCREEN_WIDTH:
           player.pos[0]=SCREEN_WIDTH-sprite_width
           if player.xvel>0:
              player.xvel-=1


        #test collision with rainbows
        for i in range(len(player.rainbows)-1,-1,-1):
            rainbow=player.rainbows[i]
            if rainbow.dead:
               del(player.rainbows[i])
            else:
               rainbow.phases[rainbow.current_phase]()
               if rainbow.current_phase=="active":
                  player.center=[player.pos[0]+32,player.pos[1]+32]
                  rainbow.center=[rainbow.pos[0]+rainbow.height,rainbow.pos[1]+rainbow.height]
                  collision,push_vector=rainbow_collision(player,rainbow)
                  if collision:
                     if player.center[1]+25<rainbow.center[1] and not rainbow.collision_under_center:
                        if rainbow!=player.mounted_rainbow:
                           if player.pos[1]+player.height-rainbow.center[1]>=0:
                              player.pos[0]+=push_vector[0]
                           else:
                              player.pos[1]+=push_vector[1]
                           player.yvel=0
                           player.xvel=0
                           player.anim_time=0
                           player.anim_index=0
                           player.max_anim_time=3
                           player.current_state="rainbow_walk"
                           player.current_sprite=player.sprites[player.direction+'_idle']
                           player.anim_sequence_lenght=player.sprites['sprites_lenght']['walk']
                           player.mounted_rainbow=rainbow
                     else:
                        rainbow.collision_under_center=True
                  else:
                     rainbow.collision_under_center=False
               else:
                  rainbow.collision_under_center=True

            
        #blit things and refresh screen
        screen.fill(BLACK)
        #screen.blit(image,(0,0))
        #for i in range(5):
            #for j in range(8):
                #pygame.draw.rect(screen, GREEN, [j*sprite_width, i*sprite_height, sprite_width, sprite_height], 5)
        for rainbow in player.rainbows:
            screen.blit(rainbow.current_sprite,rainbow.pos)       
        screen.blit(player.current_sprite,player.pos)
        pygame.display.flip()

if __name__ == "__main__":
    main()
