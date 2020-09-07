import pygame,sys
from math import radians,degrees,cos,sin,atan2,sqrt
from pygame.locals import *
import rainbow,enemies


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
        self.width=self.current_sprite.get_width()
        self.height=self.current_sprite.get_height()
        self.rainbows=[]
        self.mounted_rainbow=None
        self.anim_sequence=[]
        self.anim_sequence_lenght=self.sprites['sprites_lenght']['idle']
        self.anim_time=0
        self.max_anim_time=3
        self.anim_index=0
        self.pos=pos
        self.old_pos=[pos[0],pos[1]]
        self.move_speed=5
        self.jump_speed=5
        self.xvel=0
        self.yvel=0
        self.extra_xvel=0
        self.extra_yvel=0
        self.timer=0
        self.on_ground=True
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
           
        if not self.on_ground:
           self.current_state="fall"
           self.anim_time=0
           self.anim_index=0
           self.max_anim_time=5
           self.anim_sequence=self.sprites[self.direction+'_fall']
           self.current_sprite=self.anim_sequence[0]
           self.anim_sequence_lenght=self.sprites['sprites_lenght']['fall']
    
    def walk(self,):
        if right:
           if self.direction=="right":                
              self.extra_xvel=self.move_speed
              
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
              self.extra_xvel=self.move_speed
              
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
           
        if not self.on_ground:
           self.current_state="fall"
           self.anim_time=0
           self.anim_index=0
           self.max_anim_time=5
           self.anim_sequence=self.sprites[self.direction+'_fall']
           self.current_sprite=self.anim_sequence[0]
           self.anim_sequence_lenght=self.sprites['sprites_lenght']['fall']
   
    def jump(self):
        if up:
           self.extra_yvel=-self.jump_speed
        if right:
           if self.direction=="right":
              self.extra_xvel=self.move_speed
           elif self.direction=="left" and not self.xvel>0:
              self.direction="right"
              self.anim_sequence=self.sprites['right_jump']
        elif left:
           if self.direction=="left":
              self.extra_xvel=self.move_speed
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
           self.xvel-=friction 
           if self.xvel<0:
              self.xvel=0
           
    def fall(self):
        if right:
           if self.direction=="right":
              self.extra_xvel=self.move_speed
           elif self.direction=="left" and not self.xvel>0:
              self.direction="right"
              self.anim_sequence=self.sprites['right_fall']
        elif left:
           if self.direction=="left":                 
              self.extra_xvel=self.move_speed
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
        
        self.yvel+=gravity
        if self.yvel > max_fall_speed:
           self.yvel=max_fall_speed
        if self.on_ground:
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
              self.extra_xvel=self.move_speed
              if self.xvel<15 and run:
                 self.xvel+=1
           elif self.direction=="left":
              self.current_state="speed_break"
              self.current_sprite=self.sprites[self.direction+'_speed_break']
              
        elif left:
           if self.direction=="left":                 
              self.extra_xvel=self.move_speed
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
           
        self.xvel-=friction
        if self.xvel<0:
           self.current_state="walk"
           self.xvel=0
           self.max_anim_time=3
           
        if not self.on_ground:
           self.current_state="fall"
           self.anim_time=0
           self.anim_index=0
           self.max_anim_time=5
           self.anim_sequence=self.sprites[self.direction+'_fall']
           self.current_sprite=self.anim_sequence[0]
           self.anim_sequence_lenght=self.sprites['sprites_lenght']['fall']
     
    def speed_break(self):           
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
           
        if not self.on_ground:
           self.current_state="fall"
           self.anim_time=0
           self.anim_index=0
           self.max_anim_time=5
           self.anim_sequence=self.sprites[self.direction+'_fall']
           self.current_sprite=self.anim_sequence[0]
           self.anim_sequence_lenght=self.sprites['sprites_lenght']['fall']
   
    def death(self):
        if self.timer<30:
           self.yvel+=gravity
           if self.yvel > max_fall_speed:
              self.yvel=max_fall_speed
           self.timer+=1
        elif self.timer<60:
           self.yvel+=gravity
           if self.yvel > max_fall_speed:
              self.yvel=max_fall_speed            
           if self.on_ground:
              self.yvel=0
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
              text=font.render("you lose", True, (250,250,250))
              screen.blit(text,(255,220))
              pygame.display.flip()
              while True:
                 pygame.time.Clock().tick(30)
                 for event in pygame.event.get():
                     if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
              
        if self.anim_time>=self.max_anim_time:
           self.anim_time=0
           self.anim_index+=1
           if self.anim_index>=self.anim_sequence_lenght:
              self.anim_index=0
           self.current_sprite=self.anim_sequence[self.anim_index]
        self.anim_time+=1

    def cast_rainbow(self):
        if not self.rainbows or (self.rainbows and not self.rainbows[-1].current_phase=="start"):
           if len(self.rainbows)<=10 and self.current_state!="death":
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
                 x_new_pos,y_new_pos=rainbow_walk(self,self.mounted_rainbow,rot_speed['right'],32,32)
                 self.extra_xvel=x_new_pos-self.pos[0]
                 self.extra_yvel=y_new_pos-self.pos[1]
                    
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
                 x_new_pos,y_new_pos=rainbow_walk(self,self.mounted_rainbow,rot_speed['left'],32,32)
                 self.extra_xvel=self.pos[0]-x_new_pos
                 self.extra_yvel=y_new_pos-self.pos[1]
                    
                    
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
              
           if self.pos[1]+self.height>self.mounted_rainbow.center[1]+6:
              self.pos[1]=self.mounted_rainbow.center[1]-self.height+6
              self.current_state="walk"
              self.mounted_rainbow=None
                  
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
        self.hit_box_list=Rainbow.hit_box_list
        self.hit_box=self.hit_box_list[0]        
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
           hit_box=self.hit_box_list[self.anim_index]
           if self.direction=="right":
              self.hit_box=[self.pos[0]+hit_box[0],self.pos[1]+hit_box[1],
                            hit_box[2],hit_box[3]]
           elif self.direction=="left":
              self.hit_box=[self.pos[0]+self.width-hit_box[0]-hit_box[2],
                            self.pos[1]+hit_box[1],hit_box[2],hit_box[3]]                      
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

        
class Platform():
    def __init__(self, x, y):
        self.pos=[x,y]
        self.image = pygame.Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#DDDDDD"))
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

      
class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("#0033FF"))


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
    x_new_pos=x*cos(radians(angle))-y*sin(radians(angle))+orbit_pos[0]-center_xoffset
    y_new_pos=x*sin(radians(angle))+y*cos(radians(angle))+orbit_pos[1]-center_yoffset
    return x_new_pos,y_new_pos


def rect_collision(rect1,rect2):
    collision=0
    if rect1[0]+rect1[2]>rect2[0] and rect1[0]<rect2[0]+rect2[2] \
    and rect1[1]+rect1[3]>rect2[1] and rect1[1]<rect2[1]+rect2[3]:
        collision=1
    return collision

    
def main():
    
    pygame.init()

    #global variables
    global up,down,right,left,run,gravity,friction,max_fall_speed,floor_pos,rot_speed,font,screen    

    #Open Pygame window
    screen = pygame.display.set_mode((640, 480),) #add RESIZABLE or FULLSCREEN
    #Title
    pygame.display.set_caption("rainbow islands")
    #font
    font=pygame.font.SysFont('Arial', 30)

    
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
    player=Player([10+40,floor_pos-sprite_height])
    up=down=right=left=run=False
    gravity=0.4
    friction=0.5
    max_fall_speed=20

    camera_box=Rect(170,120,300,240)
    camera_x=camera_box.x-170
    camera_y=camera_box.y-120
    camera_right=camera_x+SCREEN_WIDTH
    camera_bottom=camera_y+SCREEN_HEIGHT

    #we do collision test for x axis and y axis separately for accurate collision detection 
    player_x_axis_collision_rect=[player.bounding_box[0],player.bounding_box[1],
                                    player.bounding_box[2],player.bounding_box[3]]
    player_y_axis_collision_rect=[player.bounding_box[0],player.bounding_box[1],
                                    player.bounding_box[2],player.bounding_box[3]]

    enemy_x_axis_collision_rect=Rect(0,0,40,40)
    enemy_y_axis_collision_rect=Rect(0,0,40,40)

    platforms = []
    exit_blocks=[]
    enemies_group = []
    active_enemies=[]
    x = y = 0
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P",
        "P                         EE               P",
        "P                         EE               P",
        "P                    PPPPPPPPPPP           P",
        "P                                          P",
        "P                                          P",
        "P           e                              P",
        "P    PPPPPPPP                              P",
        "P                             e            P",
        "P                   e      PPPPPPP         P",
        "P                 PPPPPP                   P",
        "P                                          P",
        "P         PPPPPPP                          P",
        "P                         e                P",
        "P                     PPPPPP               P",
        "P                                          P",
        "P   PPPPPPPPPPP                            P",
        "P                  e                       P",
        "P                 PPPPPPPPPPP              P",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P  e                                       P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
            elif col == "E":
                e = ExitBlock(x, y)
                exit_blocks.append(e)
            elif col == "e":
                e=enemies.Template([x,y])
                enemies_group.append(e)
            x += 32
        y += 32
        x = 0
    
    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    floor_pos=total_level_height-32
    
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
                      player.yvel=-12
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

        player.states[player.current_state]() #update player state


        #update camera position
        if player.pos[0]+player.width>camera_box.right:
           camera_box.x+=player.pos[0]+player.width-camera_box.right+1
           camera_x=camera_box.x-170
           camera_right=camera_x+SCREEN_WIDTH
           if camera_right>total_level_width:
              camera_right=total_level_width
              camera_x=camera_right-SCREEN_WIDTH
              camera_box.x=camera_x+170
        elif player.pos[0]<camera_box.left:
           camera_box.x+=player.pos[0]-camera_box.left-1
           camera_x=camera_box.x-170
           camera_right=camera_x+SCREEN_WIDTH
           if camera_x<0:
              camera_x=0
              camera_right=camera_x+SCREEN_WIDTH
              camera_box.x=camera_x+170
        if player.pos[1]+player.height>camera_box.bottom:
           camera_box.y+=player.pos[1]+player.height-camera_box.bottom+1
           camera_y=camera_box.y-120
           camera_bottom=camera_y+SCREEN_HEIGHT
           if camera_bottom>total_level_height:
              camera_bottom=total_level_height
              camera_y=camera_bottom-SCREEN_HEIGHT
              camera_box.y=camera_y+120           
        elif player.pos[1]<camera_box.top:
           camera_box.y+=player.pos[1]-camera_box.top-1
           camera_y=camera_box.y-120
           camera_bottom=camera_y+SCREEN_HEIGHT
           if camera_y<0:
              camera_y=0
              camera_bottom=camera_y+SCREEN_HEIGHT
              camera_box.y=camera_y+120


        active_enemies=[]
        for i in range(len(enemies_group)-1,-1,-1):
            enemy=enemies_group[i]
            if enemy.dead:
               enemy.death(gravity)
               if enemy.pos[1]>camera_bottom:
                  del(enemies_group[i])
               else:
                  active_enemies.append(enemy)
            else:
               if enemy.pos[0]+enemy.width>camera_x and enemy.pos[0]<camera_right \
               and enemy.pos[1]+enemy.height>camera_y and enemy.pos[1]<camera_bottom:
                  active_enemies.append(enemy)
                  enemy.yvel+=gravity
                  enemy.update(level,total_level_width)

                  
        #blit things and refresh screen
        #and do collision test in the same for loop to not repeat it and waste processing time
        screen.fill(BLACK)
        #blit rainbows
        for rainbow in player.rainbows:                    
            screen.blit(rainbow.current_sprite,(rainbow.pos[0]-camera_x,rainbow.pos[1]-camera_y))
        
        #collision test with platforms start here
        player.on_ground=False
        player.xvel+=player.extra_xvel
        #to test if player is on the ground we add +1 to player.extra_yvel
        if player.current_state!="rainbow_walk":
           player.extra_yvel+=1
        player.yvel+=player.extra_yvel
        if player.direction=="left":
           player.xvel*=-1
        player_x_axis_collision_rect[0]=player.pos[0]+15+player.xvel
        player_x_axis_collision_rect[1]=player.pos[1]+11
        player_y_axis_collision_rect[0]=player.pos[0]+15
        player_y_axis_collision_rect[1]=player.pos[1]+11+player.yvel
        
        #test for collision with visible platforms and blit them along the way
        for platform in platforms:
            #blit and test collision with only visible platforms on the screen
            if platform.rect.right>camera_x and platform.rect.left<camera_right \
            and platform.rect.bottom>camera_y and platform.rect.top<camera_bottom:
               screen.blit(platform.image,(platform.pos[0]-camera_x,platform.pos[1]-camera_y))
               #do x-axis collisions
               if rect_collision(player_x_axis_collision_rect,platform.rect):
                  if player.xvel > 0:
                     #x_axis_collision_test_rect.right=platform.rect.left
                     player_x_axis_collision_rect[0]=platform.rect[0]-player_x_axis_collision_rect[2]
                     if player.xvel-player.extra_xvel>0:
                        player.xvel-=1
                     if player.current_state=="rainbow_walk":
                        player_y_axis_collision_rect[1]-=player.yvel
                        player.yvel=0
                        player.extra_yvel=0
                  elif player.xvel < 0:
                     #x_axis_collision_test_rect.left=platform.rect.right
                     player_x_axis_collision_rect[0]=platform.rect[0]+platform.rect[2]
                     if player.xvel+player.extra_xvel<0:
                        player.xvel+=1
                     if player.current_state=="rainbow_walk":
                        player_y_axis_collision_rect[1]-=player.yvel
                        player.yvel=0
                        player.extra_yvel=0
               #do y-axis collisions
               if rect_collision(player_y_axis_collision_rect,platform.rect):
                  if player.yvel > 0:
                     #y_axis_collision_test_rect.y=platform.rect.top-y_axis_collision_test_rect.height
                     player_y_axis_collision_rect[1]=platform.rect[1]-player_y_axis_collision_rect[3]
                     player.on_ground=True
                     if player.current_state=="rainbow_walk":
                        player.current_state="walk"
                        player.mounted_rainbow=None
                  elif player.yvel < 0:
                     #y_axis_collision_test_rect.top=platform.rect.bottom
                     player_y_axis_collision_rect[1]=platform.rect[1]+platform.rect[3]
                     if player.current_state=="rainbow_walk":
                        player_x_axis_collision_rect[0]-=player.xvel
                        player.xvel=0
                        player.extra_xvel=0
               #test for collision betweens visible platforms and visible enemies
               for enemy in active_enemies:
                   #do y-axis collisions
                   if enemy.yvel > 0:
                      enemy_y_axis_collision_rect[0]=enemy.pos[0]
                      enemy_y_axis_collision_rect[1]=enemy.pos[1]+enemy.yvel
                      if enemy_y_axis_collision_rect.colliderect(platform.rect):
                         enemy_y_axis_collision_rect[1]=platform.rect[1]-enemy_y_axis_collision_rect[3]
                         enemy.pos[1]=enemy_y_axis_collision_rect[1]
                         enemy.yvel=0
        
        #resets variables
        if player.direction=="left":
           player.xvel*=-1                                 
        player.yvel-=player.extra_yvel
        player.xvel-=player.extra_xvel
        player.extra_xvel=0
        player.extra_yvel=0
        #update player position
        player.pos[0]=player_x_axis_collision_rect[0]-15
        player.pos[1]=player_y_axis_collision_rect[1]-11


        #test for collision with rainbows
        for i in range(len(player.rainbows)-1,-1,-1):
            rainbow=player.rainbows[i]
            if rainbow.dead:
               del(player.rainbows[i])
            else:
               rainbow.phases[rainbow.current_phase]()
               if rainbow.current_phase=="active" and player.current_state!="death":
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
                  if rainbow.current_phase=="start":
                     #test for collision betweens rainbows and visible enemies
                     for enemy in active_enemies:
                         enemy.bounding_box[0]=enemy.pos[0]
                         enemy.bounding_box[1]=enemy.pos[1]
                         if rect_collision(rainbow.hit_box,enemy.bounding_box):
                            if not enemy.dead:
                               enemy.sprite=pygame.transform.flip(enemy.sprite, True, True)
                               if rainbow.direction=="right":
                                  enemy.xvel=5
                               elif rainbow.direction=="left":
                                  enemy.xvel=-5
                               enemy.extra_yvel=-10
                               if enemy.bounding_box[1]>rainbow.hit_box[1]:
                                  enemy.pos[1]-=20
                                  enemy.extra_yvel-=10
                               enemy.yvel=0  
                               enemy.extra_yvel=-20
                               enemy.dead=True


        #blit visible enemies and test collision with player
        player.bounding_box[0]=player_x_axis_collision_rect[0]
        player.bounding_box[1]=player_y_axis_collision_rect[1]
        for enemy in active_enemies:
            screen.blit(enemy.sprite,(enemy.pos[0]-camera_x,enemy.pos[1]-camera_y))
            enemy.bounding_box[0]=enemy.pos[0]
            enemy.bounding_box[1]=enemy.pos[1]
            if enemy.bounding_box.colliderect(player.bounding_box):
               if player.current_state!="death" and not enemy.dead:
                  player.yvel=-12
                  player.current_state="death"
                  player.anim_time=0
                  player.anim_index=0
                  player.max_anim_time=3
                  player.anim_sequence=player.sprites['dead'][0:3]
                  player.current_sprite=player.anim_sequence[0]
                  player.anim_sequence_lenght=3
                  player.timer=0
                  
        #blit exit blocks and test collision with them          
        for block in exit_blocks:
            screen.blit(block.image,(block.pos[0]-camera_x,block.pos[1]-camera_y))
            if rect_collision(player.bounding_box,block.rect):
               if player.on_ground and player.current_state=="idle":
                  for block in exit_blocks:
                      screen.blit(block.image,(block.pos[0]-camera_x,block.pos[1]-camera_y))
                  screen.blit(player.current_sprite,(player.pos[0]-camera_x,player.pos[1]-camera_y))
                  text=font.render("you win", True, (250,250,250))
                  screen.blit(text,(255,220))
                  pygame.display.flip()
                  while True:
                     pygame.time.Clock().tick(30)
                     for event in pygame.event.get():
                         if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                            
        #blit the player                      
        screen.blit(player.current_sprite,(player.pos[0]-camera_x,player.pos[1]-camera_y))
        #pygame.draw.rect(screen, GREEN, [camera_box[0]-camera_x,camera_box[1]-camera_y,camera_box[2],camera_box[3]],5)
        pygame.display.flip()

if __name__ == "__main__":
    main()
