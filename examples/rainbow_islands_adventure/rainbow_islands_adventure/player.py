import pygame,sys
from math import radians,degrees,cos,sin,atan2,sqrt
from pygame.locals import *


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
    player_sprites['dead']=left_sprites[22:34]
    sprites_lenght={}
    sprites_lenght['idle']=0
    sprites_lenght['walk']=len(player_sprites['right_walk'])
    sprites_lenght['jump']=len(player_sprites['right_jump'])
    sprites_lenght['fall']=len(player_sprites['right_fall'])
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
        self.animation=False
        self.anim_index=0
        self.pos=pos
        self.move_speed=5
        self.jump_speed=5
        self.xvel=0
        self.yvel=0
        self.on_ground=True
        self.jump=False
        self.direction="right"
    def update(self,direction):
        pass


def main():
    
    pygame.init()

    #Open Pygame window
    screen = pygame.display.set_mode((640, 480),) #add RESIZABLE or FULLSCREEN
    #Title
    pygame.display.set_caption("rainbow islands")
    #font
    font=pygame.font.SysFont('Arial', 30)

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
                   player.direction="right"
                   if player.on_ground:
                     player.animation=True
                     player.anim_sequence=player.sprites['right_walk']
                     player.anim_sequence_lenght=player.sprites['sprites_lenght']['walk']
                     player.max_anim_time=3
                   elif not player.on_ground:
                     player.anim_sequence=player.sprites['right_jump'] 
                elif event.key == K_LEFT:
                   left=True
                   right=False
                   player.direction="left"
                   if player.on_ground:
                      player.animation=True
                      player.anim_sequence=player.sprites['left_walk']
                      player.anim_sequence_lenght=player.sprites['sprites_lenght']['walk']
                      player.max_anim_time=3
                   elif not player.on_ground:
                      player.anim_sequence=player.sprites['left_jump']                 
                if event.key == K_UP:
                   if player.on_ground:
                      up=True
                      player.on_ground=False
                      player.jump=True
                      player.yvel-=player.jump_speed
                      player.animation=True
                      if player.direction=="right":
                         player.anim_sequence=player.sprites['right_jump']
                         player.current_sprite=player.sprites['right_jump'][0]
                      elif player.direction=="left":
                         player.anim_sequence=player.sprites['left_jump']
                         player.current_sprite=player.sprites['left_jump'][0]
                      player.anim_sequence_lenght=player.sprites['sprites_lenght']['jump']
                      player.max_anim_time=8  
                if event.key == K_t:
                   run=True
                      
            if event.type == KEYUP:
                if event.key == K_UP:
                   up=False
                if event.key == K_RIGHT:
                   if right:
                      right=False
                      if player.on_ground:
                         player.anim_time=0
                         player.anim_index=0
                         player.animation=False
                         player.current_sprite=player.sprites['right_idle']
                elif event.key == K_LEFT:
                   if left:
                      left=False
                      if player.on_ground:
                         player.anim_time=0
                         player.anim_index=0                        
                         player.animation=False
                         player.current_sprite=player.sprites['left_idle']
                if event.key == K_t:
                   run=False
                   if player.on_ground:
                      player.max_anim_time=3
                      
        if up:
           if player.jump:
              player.pos[1]-=player.jump_speed
        if right:
           player.pos[0]+=player.move_speed
        elif left :
           player.pos[0]-=player.move_speed
                    
        if player.pos[0]<0:
           player.pos[0]=0
        elif player.pos[0]+sprite_width>SCREEN_WIDTH:
           player.pos[0]=SCREEN_WIDTH-sprite_width
           
        if not player.on_ground:
           player.pos[1]+=player.yvel
           player.yvel+=gravity
           if player.yvel>0:
              player.jump=False
              player.anim_sequence=player.sprites[player.direction+'_fall']
           if player.yvel > max_fall_speed:
              player.yvel=max_fall_speed
           if player.pos[1]+sprite_height>floor_pos:
              player.pos[1]=floor_pos-sprite_height
              player.yvel=0
              player.on_ground=True
              player.jump=False              
              player.anim_time=0
              player.anim_index=0                     
              if player.direction=="right":
                 player.animation=False
                 player.current_sprite=player.sprites['right_idle']
                 player.anim_sequence_lenght=player.sprites['sprites_lenght']['idle']
              elif player.direction=="left":
                 player.animation=False
                 player.current_sprite=player.sprites['left_idle']
                 player.anim_sequence_lenght=player.sprites['sprites_lenght']['idle']   
              if right:
                 player.animation=True
                 player.anim_sequence=player.sprites['right_walk']
                 player.anim_sequence_lenght=player.sprites['sprites_lenght']['walk']
                 player.max_anim_time=3
              elif left:
                 player.animation=True
                 player.anim_sequence=player.sprites['left_walk']
                 player.anim_sequence_lenght=player.sprites['sprites_lenght']['walk']
                 player.max_anim_time=3

        if player.animation:
          if player.anim_time>=player.max_anim_time:
             player.anim_time=0
             player.anim_index+=1
             if player.anim_index>=player.anim_sequence_lenght:
                player.anim_index=0
             player.current_sprite=player.anim_sequence[player.anim_index]
          player.anim_time+=1
            
        #blit things and refresh screen
        screen.fill(BLACK)
        #screen.blit(image,(0,0))
        #for i in range(5):
            #for j in range(8):
                #pygame.draw.rect(screen, GREEN, [j*sprite_width, i*sprite_height, sprite_width, sprite_height], 5)
        screen.blit(player.current_sprite,player.pos)
        pygame.display.flip()

if __name__ == "__main__":
    main()
